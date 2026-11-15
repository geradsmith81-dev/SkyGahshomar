"""The live 'Face the light' compass (Today page), adapted from Sky Taqwim's qibla_live.py.

Zoroastrians pray standing, facing a source of light (gahs.FACING_LIGHT): the Sun by day, the Moon when it is up
at night, otherwise a lamp or a fire. sky_layer.face_the_light() gives the Sun's and the Moon's altitude and
azimuth from JPL DE440s and which light to face; this card draws a compass dial (N, E, S, W) and a gold arrow
carrying that light, and a small browser component turns them with the phone:

* the phone's compass gives its heading from MAGNETIC north (iPhone/iPad: webkitCompassHeading after the user
  taps the button and allows "Motion & Orientation"; Android: the absolute device-orientation event,
  heading = 360 - alpha + screen.orientation.angle);
* the magnetic declination of the place (World Magnetic Model WMM2025, via pygeomag) turns that into a heading
  from TRUE north, the reference of the JPL azimuth;
* the dial is turned by -heading and the arrow by (azimuth - heading), so the arrow points at the light however
  the phone is turned. Within 5 degrees the card says the user is facing it.

When neither light is up the card shows the fire altar and says to face a lamp or fire (no arrow). Computers have
no compass: the dial then stays with north at the top and the arrow at the azimuth. Nothing leaves the browser.
The layout is written on the elements themselves and the stylesheet (theme.COMPASS_CSS) is also injected
page-wide by theme.apply(), because a components.v2 css= was not applied on Streamlit Community Cloud.
"""
from __future__ import annotations

import html
import os
from datetime import datetime, timezone

import streamlit as st

import ornaments as orn
from theme import COMPASS_CSS as CSS

HERE = os.path.dirname(os.path.abspath(__file__))

try:   # World Magnetic Model 2025 (NOAA/BGS, public domain) through pygeomag (MIT)
    from pygeomag import GeoMag
    try:
        _GM = GeoMag(coefficients_file="wmm/WMM_2025.COF")      # the copy inside the pygeomag package
        _GM.calculate(glat=0.0, glon=0.0, alt=0, time=2026.0, allow_date_outside_lifespan=True)
    except Exception:   # fall back to the copy shipped with the app (an absolute path is used as given)
        _GM = GeoMag(coefficients_file=os.path.join(HERE, "wmm", "WMM_2025.COF"))
except Exception:   # pragma: no cover - the compass still works, only uncorrected for declination
    _GM = None


def declination(lat: float, lon: float, when: datetime | None = None) -> float | None:
    """Magnetic declination in degrees (east positive) from WMM2025, or None if the model is unavailable."""
    if _GM is None:
        return None
    t = when or datetime.now(timezone.utc)
    year = t.year + (t.timetuple().tm_yday - 0.5) / (366 if t.year % 4 == 0 else 365)
    try:
        return float(_GM.calculate(glat=float(lat), glon=float(lon), alt=0, time=year,
                                   allow_date_outside_lifespan=True).d)
    except Exception:
        return None


JS = r"""
const G = (window.__skygahshomarLight = window.__skygahshomarLight || {
  heading: null, shown: null, beta: 0, gamma: 0, acc: null, got: false, started: false, loop: false,
  view: null, facing: false
});

function norm180(a) { return ((a % 360) + 540) % 360 - 180; }
function screenAngle() {
  if (screen.orientation && typeof screen.orientation.angle === 'number') return screen.orientation.angle;
  if (typeof window.orientation === 'number') return window.orientation;
  return 0;
}

function onIOS(e) {          // iPhone / iPad: heading of the top of the device from magnetic north
  if (typeof e.webkitCompassHeading !== 'number' || isNaN(e.webkitCompassHeading)) return;
  G.heading = e.webkitCompassHeading + screenAngle();
  G.acc = (typeof e.webkitCompassAccuracy === 'number') ? e.webkitCompassAccuracy : null;
  G.beta = e.beta || 0; G.gamma = e.gamma || 0; G.got = true;
}
function onAbs(e) {          // Android: absolute orientation, alpha counter-clockwise from magnetic north
  if (e.alpha === null || e.alpha === undefined) return;
  G.heading = (360 - e.alpha) + screenAngle();
  G.beta = e.beta || 0; G.gamma = e.gamma || 0; G.got = true;
}
function onRel(e) { if (e.absolute === true) onAbs(e); }

function status(text, cls) {
  const V = G.view; if (!V || !V.status) return;
  if (V.status.textContent !== text) V.status.textContent = text;
  V.status.className = 'gs-ql-status' + (cls ? ' ' + cls : '');
}

function frame() {
  const V = G.view;
  if (V && V.dial && V.dial.isConnected && G.heading !== null) {
    const target = G.heading + (V.decl || 0);                       // true heading of the top of the phone
    if (G.shown === null) G.shown = target;
    G.shown += norm180(target - G.shown) * 0.25;                    // smooth, and never spin the long way round
    const h = G.shown;
    V.dial.style.transform = 'rotate(' + (-h).toFixed(2) + 'deg)';
    V.arrow.style.transform = 'rotate(' + (V.bearing - h).toFixed(2) + 'deg)';
    const rel = norm180(V.bearing - h);
    const flat = Math.abs(G.beta) < 35 && Math.abs(G.gamma) < 35;
    const facing = flat && Math.abs(rel) <= 5;
    V.stage.classList.toggle('gs-ql-on', facing);
    if (facing && !G.facing && navigator.vibrate) { try { navigator.vibrate(40); } catch (err) {} }
    G.facing = facing;
    if (!flat) status('Hold the phone flat, screen up, for a true reading.', 'gs-ql-warn');
    else if (G.acc !== null && (G.acc < 0 || G.acc > 25)) status('The compass needs calibrating: move the phone in a figure of eight, then hold it flat.', 'gs-ql-warn');
    else if (facing) status('You are facing ' + V.what + '.', 'gs-ql-good');
    else {
      const turn = Math.round(Math.abs(rel));
      status('Turn ' + turn + '\u00b0 to the ' + (rel > 0 ? 'right' : 'left') + ' to face ' + V.what + ' (the arrow shows the way).', '');
    }
  }
  requestAnimationFrame(frame);
}

function start(manual) {
  if (G.started) return;
  G.started = true;
  if ('ondeviceorientationabsolute' in window) window.addEventListener('deviceorientationabsolute', onAbs, true);
  else window.addEventListener('deviceorientation', onRel, true);
  window.addEventListener('deviceorientation', onIOS, true);
  if (!G.loop) { G.loop = true; requestAnimationFrame(frame); }
  status('Reading the compass... hold the phone flat.', '');
  setTimeout(function () {
    if (G.got) return;
    G.started = false;
    const V = G.view; if (!V) return;
    status('No compass reading from this device. The dial shows the direction with north at the top.', 'gs-ql-warn');
    if (window.self !== window.top && V.tab) V.tab.style.display = 'inline-block';
    if (V.btn) V.btn.style.display = manual ? 'inline-block' : 'none';
  }, 3000);
}

function askAndStart() {     // iPhone / iPad must ask, from a tap
  const D = window.DeviceOrientationEvent;
  if (D && typeof D.requestPermission === 'function') {
    D.requestPermission().then(function (r) {
      if (r === 'granted') { G.view.btn.style.display = 'none'; start(true); }
      else status('Compass not allowed. Close and reopen the app, then tap the button again and choose Allow. If iOS does not ask again: Settings > Apps > Safari > Advanced > Website Data, delete streamlit.app, and try again.', 'gs-ql-warn');
    }).catch(function () { status('The compass could not be started on this device.', 'gs-ql-warn'); });
  } else { G.view.btn.style.display = 'none'; start(true); }
}

export default function (component) {
  const { data, parentElement } = component;
  let V = parentElement.__skygahshomarLight;
  const key = (data && data.html) || '';
  if (!V || V.key !== key) {
    parentElement.innerHTML = key;
    V = { key: key,
          stage: parentElement.querySelector('.gs-ql-stage'),
          dial: parentElement.querySelector('.gs-ql-dial'),
          arrow: parentElement.querySelector('.gs-ql-arrow'),
          status: parentElement.querySelector('.gs-ql-status'),
          btn: parentElement.querySelector('.gs-ql-btn'),
          tab: parentElement.querySelector('.gs-ql-tab') };
    parentElement.__skygahshomarLight = V;
    if (V.btn) V.btn.addEventListener('click', askAndStart);
    if (V.tab) V.tab.href = window.location.href;
  }
  V.bearing = Number(data && data.bearing) || 0;
  V.decl = Number(data && data.decl) || 0;
  V.what = (data && data.what) || 'the light';
  V.lamp = !!(data && data.lamp);
  G.view = V; G.shown = null;
  if (V.lamp) { if (V.btn) V.btn.style.display = 'none'; status('Neither the Sun nor the Moon is up: face a lamp or a fire.', ''); return; }
  if (G.heading === null) {            // not turning yet: the static drawing (north up)
    V.dial.style.transform = 'rotate(0deg)';
    V.arrow.style.transform = 'rotate(' + V.bearing.toFixed(2) + 'deg)';
  }
  const D = window.DeviceOrientationEvent;
  const touch = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  if (G.got) { if (V.btn) V.btn.style.display = 'none'; if (!G.loop) { G.loop = true; requestAnimationFrame(frame); } return; }
  if (!D) { status('This browser has no compass. The dial shows the direction with north at the top.', ''); if (V.btn) V.btn.style.display = 'none'; return; }
  if (typeof D.requestPermission === 'function') {          // iPhone / iPad (and Safari on Mac)
    if (touch) { V.btn.style.display = 'inline-block'; status('Tap the button, allow Motion & Orientation, and hold the phone flat.', ''); }
    else { V.btn.style.display = 'none'; status('On a phone or tablet the arrow turns with the device, like a compass.', ''); }
  } else if (touch) {                                       // Android: no permission needed
    if (V.btn) V.btn.style.display = 'none';
    start(false);
  } else {
    if (V.btn) V.btn.style.display = 'none';
    status('On a phone or tablet the arrow turns with the device, like a compass.', '');
  }
}
"""

_COMPONENT = st.components.v2.component("skygahshomar_light", js=JS, css=CSS, isolate_styles=False)

_WRAP = "position:relative;padding-top:14px;flex:0 0 auto;"
_LUBBER = ("position:absolute;top:0;left:50%;transform:translateX(-50%);width:0;height:0;"
           "border-left:9px solid transparent;border-right:9px solid transparent;border-top:13px solid #b5412c;")
_STAGE = "position:relative;border-radius:50%;"
_LAYER = "position:absolute;top:0;left:0;width:100%;height:100%;transform-origin:50% 50%;line-height:0;"
_INFO = "flex:1 1 13rem;min-width:12rem;"
_ROW = "display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;"

POINT_WORDS = {"N": "north", "NNE": "north-north-east", "NE": "north-east", "ENE": "east-north-east", "E": "east",
               "ESE": "east-south-east", "SE": "south-east", "SSE": "south-south-east", "S": "south",
               "SSW": "south-south-west", "SW": "south-west", "WSW": "west-south-west", "W": "west",
               "WNW": "west-north-west", "NW": "north-west", "NNW": "north-north-west"}


def _html(ftl: dict, place: str, decl: float | None, size: int, title_html: str, waxing: bool) -> str:
    face = ftl["face"]
    sun, moon = ftl["sun"], ftl["moon"]
    where = f" from {html.escape(place)}" if place else ""
    if face == "lamp":
        what = "a lamp or a fire"
        main = (f"<div class='gs-ql-deg'>Face a lamp or a fire</div>"
                f"<div class='gs-ql-text'>Neither the Sun ({sun['alt']:.0f}° altitude) nor the Moon "
                f"({moon['alt']:.0f}°) is above the horizon{where}. Zoroastrians then pray facing a lamp or a "
                f"fire.</div>")
        arrow = orn.light_arrow_svg(size, "lamp")
        centre = (f"<div style='position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);line-height:0'>"
                  f"{orn.fire_altar_svg(int(size * 0.42))}</div>")
    else:
        body = sun if face == "sun" else moon
        b = float(body["az"]) % 360.0
        word = POINT_WORDS.get(body["point"], body["point"])
        what = "the Sun" if face == "sun" else "the Moon"
        extra = "" if face == "sun" else f" ({moon['illumination'] * 100:.0f}% lit)"
        main = (f"<div class='gs-ql-deg'>Face {what}: {b:.1f}°</div>"
                f"<div class='gs-ql-text'>{what[0].upper() + what[1:]}{extra}{where}: {b:.1f}° from true north, "
                f"toward the {word}, {body['alt']:.0f}° above the horizon (JPL DE440s, refraction included).</div>")
        arrow = orn.light_arrow_svg(size, face, moon.get("illumination", 1.0), waxing)
        centre = ""
    if face == "lamp":
        dec = ""
    elif decl is None:
        dec = ("<div class='gs-ql-text'>A magnetic compass differs from true north by the local declination (not "
               "available here, so the live arrow is not corrected for it).</div>")
    else:
        side = "east" if decl >= 0 else "west"
        dec = (f"<div class='gs-ql-text'>Magnetic north here is {abs(decl):.1f}° {side} of true north (World "
               f"Magnetic Model 2025); the live arrow allows for it.</div>")
    dial = orn.compass_dial_svg(size)
    b0 = float(ftl["bearing"]) % 360.0 if ftl.get("bearing") is not None else 0.0   # static drawing (no JS)
    return (f"<div class='gs-card gs-ql-card'><h3>{title_html}</h3><div class='gs-ql' style='{_ROW}'>"
            f"<div class='gs-ql-wrap' style='{_WRAP}'>"
            f"<div class='gs-ql-lubber' title='The top of your phone' style='{_LUBBER}'></div>"
            f"<div class='gs-ql-stage' style='{_STAGE}width:{size}px;height:{size}px'>"
            f"<div class='gs-ql-dial' style='{_LAYER}'>{dial}</div>"
            f"<div class='gs-ql-arrow' style='{_LAYER}transform:rotate({b0:.2f}deg)'>{arrow}</div>{centre}</div></div>"
            f"<div class='gs-ql-info' style='{_INFO}'>{main}{dec}"
            f"<button type='button' class='gs-ql-btn' style='display:none'>Turn on the live compass</button>"
            f"<div class='gs-ql-status' aria-live='polite'></div>"
            f"<a class='gs-ql-tab' target='_blank' rel='noopener' style='display:none'>Open the app in its own tab "
            f"for the compass</a></div></div></div>"), what


def markup(ftl: dict, place: str, lat: float, lon: float, title_html: str, size: int = 170,
           waxing: bool = True) -> tuple[str, float | None, str]:
    """(html, declination, what) without the component: for static previews and tests."""
    decl = declination(lat, lon)
    h, what = _html(ftl, place, decl, size, title_html, waxing)
    return h, decl, what


def show(ftl: dict, place: str, lat: float, lon: float, title_html: str, size: int = 170, waxing: bool = True,
         key: str = "light_live"):
    h, decl, what = markup(ftl, place, lat, lon, title_html, size, waxing)
    bearing = float(ftl["bearing"]) % 360.0 if ftl.get("bearing") is not None else 0.0
    return _COMPONENT(data={"html": h, "bearing": bearing, "decl": decl or 0.0, "what": what,
                            "lamp": ftl["face"] == "lamp"}, key=key, width="stretch", height="content")
