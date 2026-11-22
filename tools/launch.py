"""Start Sky Gahshomar on this computer.

Run by "Start app.bat" with pythonw.exe, so no console window appears. It:
  1. checks the program files against MANIFEST.sha256 and warns if any are missing or changed;
  2. keeps user data in %LOCALAPPDATA%\\SkyGahshomar (moving an old "cache" folder there once);
  3. opens the copy that is already running instead of starting a second one;
  4. runs the Streamlit server for this computer only (127.0.0.1), logging to
     %LOCALAPPDATA%\\SkyGahshomar\\logs\\skygahshomar.log, and stops it when the app window is closed;
  5. with --share (from "Share on this network.bat", in a visible window) listens on the local
     network instead and asks visitors from other devices for a one-time password.

  python tools\\launch.py --make-shortcut   puts the Sky Gahshomar icon on the Desktop and in the Start menu.
"""
import argparse
import ctypes
import hashlib
import json
import logging
import os
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import desktop as dk  # noqa: E402

# ---- settings for this app ------------------------------------------------------------------
APP = 'Sky Gahshomar'
SLUG = 'skygahshomar'
PORT = 8513
PREFIX = 'SKYGAHSHOMAR'
SCRIPT = 'app.py'
ICON = r'assets\gahshomar_icon.ico'
SHORTCUT = 'Sky Gahshomar.lnk'
OLD_SHORTCUTS = []
SHARE_ALLOWED = True
WINDOW_SIZE = '1360,960'
# environment variable -> folder under %LOCALAPPDATA%\SkyGahshomar (created at start, cleared by "Clear stored data")
DATA_DIRS = {}
# folders in the program folder that older versions used; moved once into the data folder
MOVE_OLD = []
# ----------------------------------------------------------------------------------------------

URL = f'http://localhost:{PORT}'
MANIFEST = 'MANIFEST.sha256'
log = logging.getLogger(SLUG + '.launch')


# ------------------------------------------------------------------------------------------
# small Windows helpers
# ------------------------------------------------------------------------------------------
MB_OK, MB_YESNO, MB_ICONWARNING, MB_ICONERROR, MB_ICONINFO, MB_DEFBUTTON2 = 0, 4, 0x30, 0x10, 0x40, 0x100
IDYES = 6


def message(text, flags=MB_OK | MB_ICONINFO):
    log.info('Message shown: %s', text.replace('\n', ' / '))
    try:
        return ctypes.windll.user32.MessageBoxW(0, text, APP, flags | 0x10000)   # MB_SETFOREGROUND
    except Exception:
        print(text)
        return 0


def pid_alive(pid):
    try:
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, int(pid))            # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        ok = k.GetExitCodeProcess(h, ctypes.byref(code))
        k.CloseHandle(h)
        return bool(ok) and code.value == 259                  # STILL_ACTIVE
    except Exception:
        return False


def tidy_console():
    """Visible (sharing) window only: stop click-to-freeze (QuickEdit) and show colours properly."""
    try:
        k = ctypes.windll.kernel32
        h_in, h_out = k.GetStdHandle(-10), k.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        if k.GetConsoleMode(h_in, ctypes.byref(mode)):
            k.SetConsoleMode(h_in, (mode.value | 0x0080) & ~0x0040)    # extended flags on, QuickEdit off
        if k.GetConsoleMode(h_out, ctypes.byref(mode)):
            k.SetConsoleMode(h_out, mode.value | 0x0004)               # virtual-terminal colours
    except Exception:
        pass


# ------------------------------------------------------------------------------------------
# 1. program-file check
# ------------------------------------------------------------------------------------------
def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check_files():
    """Return a list of problems ('missing: x', 'changed: y'); empty when every file matches."""
    mf = os.path.join(HERE, MANIFEST)
    if not os.path.exists(mf):
        return [f'missing: {MANIFEST} (the list of program files)']
    problems = []
    with open(mf, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            digest, rel = line.split(None, 1)
            rel = rel.lstrip('*')
            p = os.path.join(HERE, *rel.split('/'))
            if not os.path.exists(p):
                problems.append(f'missing: {rel}')
            elif sha256(p) != digest.lower():
                problems.append(f'changed: {rel}')
    return problems


# ------------------------------------------------------------------------------------------
# 2. user data
# ------------------------------------------------------------------------------------------
def prepare_data_dir():
    data = dk.data_dir()
    os.makedirs(os.path.join(data, 'logs'), exist_ok=True)
    for rel in MOVE_OLD:
        old, new = os.path.join(HERE, rel), os.path.join(data, rel)
        if os.path.isdir(old) and not os.path.exists(new):
            try:
                shutil.move(old, new)      # one-time move of stored data out of the program folder
            except Exception:
                log.exception('Could not move %s to %s', old, new)
    for parts in DATA_DIRS.values():
        os.makedirs(os.path.join(data, *parts), exist_ok=True)
    return data


def start_logging(data, echo):
    logs = os.path.join(data, 'logs')
    cur = os.path.join(logs, SLUG + '.log')
    for i in (3, 2, 1):                     # keep the last four runs
        src = cur if i == 1 else os.path.join(logs, f'{SLUG}.{i - 1}.log')
        dst = os.path.join(logs, f'{SLUG}.{i}.log')
        try:
            if os.path.exists(src):
                os.replace(src, dst)
        except OSError:
            pass
    stream = open(cur, 'a', encoding='utf-8', buffering=1, errors='replace')
    if not echo:                            # pythonw.exe has no console: send everything to the log
        sys.stdout = sys.stderr = stream
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    return cur


# ------------------------------------------------------------------------------------------
# 3. one copy at a time
# ------------------------------------------------------------------------------------------
_LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # never send local checks to a proxy


def healthy(timeout=1.0):
    try:
        with _LOCAL.open(f'http://127.0.0.1:{PORT}/_stcore/health', timeout=timeout) as r:
            return r.status == 200 and r.read().strip() == b'ok'
    except Exception:
        return False


def port_in_use():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', PORT)) == 0


def running_state():
    try:
        with open(dk.state_file(), encoding='utf-8') as f:
            st = json.load(f)
        return st if pid_alive(st.get('pid', 0)) else None
    except Exception:
        return None


def open_window():
    edge = None
    for base in (os.environ.get('ProgramFiles(x86)'), os.environ.get('ProgramFiles')):
        if base:
            p = os.path.join(base, 'Microsoft', 'Edge', 'Application', 'msedge.exe')
            if os.path.exists(p):
                edge = p
                break
    try:
        if edge:
            subprocess.Popen([edge, f'--app={URL}', f'--window-size={WINDOW_SIZE}'], close_fds=True)
        else:
            import webbrowser
            webbrowser.open(URL)
    except Exception:
        log.exception('Could not open the app window')


# ------------------------------------------------------------------------------------------
# desktop icon (no PowerShell script file, so no execution-policy override is needed)
# ------------------------------------------------------------------------------------------
def _shortcut_ps():
    old = ''.join(f"Remove-Item -LiteralPath (Join-Path $dir '{n}') -ErrorAction SilentlyContinue; "
                  for n in OLD_SHORTCUTS)
    return (
        "$here = $env:DK_HERE; $ws = New-Object -ComObject WScript.Shell; "
        "$targets = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs')); "
        "$od = Join-Path $env:USERPROFILE 'OneDrive\\Desktop'; "
        "if ((Test-Path $od) -and ($targets -notcontains $od)) { $targets += $od }; "
        "foreach ($dir in $targets) { " + old +
        f"$s = $ws.CreateShortcut((Join-Path $dir '{SHORTCUT}')); "
        "$s.TargetPath = $env:ComSpec; "
        "$s.Arguments = '/c ' + [char]34 + (Join-Path $here 'Start app.bat') + [char]34; "
        "$s.WorkingDirectory = $here; "
        f"$s.IconLocation = (Join-Path $here '{ICON}'); "
        "$s.WindowStyle = 7; $s.Save() }"
    )


def make_shortcut():
    env = dict(os.environ, DK_HERE=HERE)
    r = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', _shortcut_ps()],
                       env=env, capture_output=True, text=True, creationflags=0x08000000)
    if r.returncode != 0:
        print(r.stderr.strip())
    return r.returncode


# ------------------------------------------------------------------------------------------
# 5. sharing on the local network
# ------------------------------------------------------------------------------------------
def local_addresses():
    found = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('192.0.2.1', 9))      # picks the outgoing interface; sends nothing
            found.append(s.getsockname()[0])
    except Exception:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if not ip.startswith('127.') and ip not in found:
                found.append(ip)
    except Exception:
        pass
    return found


def new_password():
    abc = 'abcdefghjkmnpqrstuvwxyz23456789'
    s = ''.join(secrets.choice(abc) for _ in range(10))
    return s[:5] + '-' + s[5:]


# ------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--share', action='store_true')
    ap.add_argument('--make-shortcut', action='store_true')
    a = ap.parse_args()
    if a.make_shortcut:
        sys.exit(make_shortcut())
    if a.share and not SHARE_ALLOWED:
        message(f'{APP} cannot be shared on the network. It only runs for the person at this computer.',
                MB_OK | MB_ICONWARNING)
        sys.exit(1)

    if a.share:
        tidy_console()
    data = prepare_data_dir()
    logfile = start_logging(data, echo=a.share)
    log.info('%s launcher started from %s (share=%s)', APP, HERE, a.share)

    problems = check_files()
    if problems:
        shown = '\n'.join(problems[:12]) + ('\n...' if len(problems) > 12 else '')
        ans = message(f"Some of {APP}'s program files are missing or have been changed:\n\n"
                      f'{shown}\n\nThe safest fix is to download {APP} again and unzip a fresh copy.\n\n'
                      f'Start {APP} anyway?', MB_YESNO | MB_ICONWARNING | MB_DEFBUTTON2)
        if ans != IDYES:
            sys.exit(1)

    if healthy():
        st = running_state()
        if st and st.get('port') == PORT:
            if a.share and not st.get('share'):
                message(f'{APP} is already running for this computer only.\n\nUse "Quit {APP}" at '
                        'the bottom of its page, then start "Share on this network" again.')
            else:
                open_window()
            sys.exit(0)
        message(f'Another program is already using port {PORT}, so {APP} cannot start.\n\n'
                'Close the other program (for example another app from the same series) and try again.',
                MB_OK | MB_ICONERROR)
        sys.exit(1)
    if port_in_use():
        message(f'Another program is already using port {PORT}, so {APP} cannot start.',
                MB_OK | MB_ICONERROR)
        sys.exit(1)

    os.environ[PREFIX + '_DESKTOP'] = '1'
    clear = []
    for var, parts in DATA_DIRS.items():
        os.environ[var] = os.path.join(data, *parts)
        clear.append(os.environ[var])
    os.environ[PREFIX + '_CLEAR_DIRS'] = os.pathsep.join(clear)
    address = '127.0.0.1'
    if a.share:
        pw = new_password()
        os.environ[PREFIX + '_SHARE_PASSWORD'] = pw
        address = '0.0.0.0'
        addrs = local_addresses()
        print(f'\n  {APP.upper()} IS SHARED ON THIS NETWORK\n')
        print('  On a phone, tablet or another computer on the same Wi-Fi, open:')
        for ip in addrs or ["(this computer's network address)"]:
            print(f'      http://{ip}:{PORT}')
        print(f'\n  Password:  {pw}      (new each time; anyone with it can use the app)\n')
        print('  If Windows Firewall asks, allow Python on PRIVATE networks only.')
        print('  Do not share on public Wi-Fi (cafes, hotels, conferences).')
        print('  CLOSE THIS WINDOW TO STOP SHARING AND STOP THE APP.\n', flush=True)
    else:
        os.environ.pop(PREFIX + '_SHARE_PASSWORD', None)

    os.makedirs(data, exist_ok=True)
    with open(dk.state_file(), 'w', encoding='utf-8') as f:
        json.dump(dict(pid=os.getpid(), port=PORT, share=a.share, started=time.time(), folder=HERE), f)

    def open_when_ready():
        for _ in range(240):
            if healthy(0.5):
                open_window()
                return
            time.sleep(0.5)
        message(f'{APP} did not start.\n\nDetails are in:\n{logfile}', MB_OK | MB_ICONERROR)
        dk.shutdown('server did not start', 1)

    threading.Thread(target=open_when_ready, name=SLUG + '-open', daemon=True).start()
    if not a.share:
        dk.start_idle_watch()

    os.chdir(HERE)
    flags = ['--server.port', str(PORT), '--server.address', address, '--server.headless', 'true',
             '--server.fileWatcherType', 'none', '--server.runOnSave', 'false',
             '--global.developmentMode', 'false', '--client.toolbarMode', 'minimal']
    if a.share:
        # The banner above replaces Streamlit's, which would also look up this network's public
        # internet address from an outside service: neither needed nor wanted.
        flags += ['--client.showErrorDetails', 'none', '--logger.hideWelcomeMessage', 'true']
    sys.argv = ['streamlit', 'run', os.path.join(HERE, SCRIPT)] + flags
    try:
        from streamlit.web import cli
        cli.main()
    except SystemExit as e:
        log.info('Streamlit exited with %s', e.code)
        if e.code not in (0, None):
            message(f'{APP} stopped because of an error.\n\nDetails are in:\n{logfile}', MB_OK | MB_ICONERROR)
        dk.shutdown('server exited', e.code if isinstance(e.code, int) else 1)
    except BaseException:
        log.exception('%s stopped because of an error', APP)
        message(f'{APP} stopped because of an error.\n\nDetails are in:\n{logfile}', MB_OK | MB_ICONERROR)
        dk.shutdown('error', 1)
    dk.shutdown('server stopped')


if __name__ == '__main__':
    main()
