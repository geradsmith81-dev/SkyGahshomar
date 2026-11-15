"""Syntax and smoke check of the browser components (face_light_live.JS, locator.JS) with the quickjs package.

Each JS string is (1) compiled as an ES module with stub browser globals, and (2) run as a script with a stub DOM
through the 'no compass', 'lamp', iPhone (permission button) and Android (absolute orientation) branches.
Usage: python tools/js_check.py   (pip install quickjs)
"""
import json
import os
import sys

import quickjs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUB = """var window={matchMedia:function(){return {matches:false}},addEventListener:function(){},self:1,top:1,location:{href:'x'}};
globalThis.window=window; var navigator={}; globalThis.navigator=navigator; var screen={orientation:{angle:0}};
globalThis.screen=screen; var sessionStorage={getItem:function(){return null},setItem:function(){}};
function requestAnimationFrame(f){}; function setTimeout(f,t){};
function el(){return {style:{},classList:{toggle:function(){}},addEventListener:function(){},appendChild:function(){},
  append:function(){},textContent:'',className:'',isConnected:true}}
var document={createElement:function(){return el()}};
var pe={querySelector:function(){return el()}, appendChild:function(){}, innerHTML:''};
"""
CASES = {
    "no_device": "__main({data:{html:'<div></div>',bearing:248,decl:-0.03,what:'the Sun',lamp:false,label:'Mumbai',auto:false},parentElement:pe,setTriggerValue:function(){}});",
    "lamp": "__main({data:{html:'x',bearing:0,decl:0,what:'a lamp',lamp:true},parentElement:pe,setTriggerValue:function(){}});",
    "ios_touch": "window.matchMedia=function(){return {matches:true}}; window.DeviceOrientationEvent={requestPermission:function(){return {then:function(){return {catch:function(){}}}}}}; __main({data:{html:'x',bearing:120,decl:1.2,what:'the Moon',lamp:false,auto:true},parentElement:pe,setTriggerValue:function(){}});",
    "android_touch": "window.matchMedia=function(){return {matches:true}}; window.DeviceOrientationEvent=function(){}; window.ondeviceorientationabsolute=null; __main({data:{html:'y',bearing:200,decl:-3,what:'the Sun',lamp:false,auto:true},parentElement:pe,setTriggerValue:function(){}});",
}


def js_of(module: str) -> str:
    src = open(os.path.join(ROOT, module + ".py"), encoding="utf-8").read()
    return src.split('JS = r"""', 1)[1].split('"""', 1)[0]


def main() -> int:
    out, bad = {}, 0
    for mod in ("face_light_live", "locator"):
        code = js_of(mod)
        r = {}
        try:
            c = quickjs.Context()
            c.eval(STUB)
            c.module(code)
            r["module"] = "ok"
        except Exception as e:
            r["module"] = f"ERR {e}"
        for name, call in CASES.items():
            try:
                c = quickjs.Context()
                c.eval(STUB + code.replace("export default function", "globalThis.__main = function"))
                c.eval(call)
                r[name] = "ok"
            except Exception as e:
                r[name] = f"ERR {e}"
        bad += sum(1 for v in r.values() if v != "ok")
        out[mod] = r
    print(json.dumps(out, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
