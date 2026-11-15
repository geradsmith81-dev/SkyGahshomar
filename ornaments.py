"""Decorative SVG ornaments after Achaemenid art (Persia, 6th-4th centuries BCE).

* Faravahar - the winged figure in a ring as carved over the Behistun inscription of Darius I (c. 520 BCE) and
  on the doorways and royal tombs of Persepolis and Naqsh-e Rostam: a winged ring with long feathered wings in
  three registers, a feathered tail below, two scrolling streamers, and a bearded man in a cylindrical crown
  rising from the ring, one hand raised and the other holding a ring. Who the figure represents (Ahura Mazda,
  the royal fravashi or the king's 'glory', khvarenah) is debated; its modern name and use as the emblem of
  Zoroastrianism (as 'Farohar' or 'Faravahar') are modern. It is drawn here from simple geometry, facing left as
  at Behistun; nothing is traced from photographs or from existing drawings.
* rosette - the twelve-petalled rosette that runs in bands along the stairways and doorways of the Apadana
  and other palaces at Persepolis (also on the glazed bricks of Susa).
* lotus-and-bud - the frieze of open lotus flowers and closed buds on linked stems, as on the Apadana stairs.
* capital - a double-protome column capital: two kneeling foreparts of bulls (or of griffins, the 'homa'
  capitals) set back to back, with the roof beam in the saddle between their necks, as at Persepolis.
* glazed-brick palette - turquoise, ochre-yellow, white and brown glazes of the Susa friezes (the 'Archers'
  and the winged-disc and sphinx panels); lapis; gold (the Oxus Treasure); Persepolis grey limestone.
* Gah icons - the five watches of the Zoroastrian day (Havan, Rapithwin or Second Havan, Uziran,
  Aiwisruthrem, Ushahin) as sunrise, noon, afternoon, sunset and night.
* fire altar - the stepped Achaemenid fire altar of the royal tomb reliefs at Naqsh-e Rostam.
* the Moon - drawn only as the astronomical Moon (lit part and earthshine), for the Mah Niyayesh days.
"""
from __future__ import annotations

import base64
import math

GOLD = "#ecc566"        # gold (Oxus Treasure)
GOLD_DEEP = "#a8792a"   # gold in shade
OCHRE = "#d49a36"       # yellow-ochre glaze (Susa bricks)
TURQUOISE = "#2aa6a1"   # turquoise glaze
TURQ_LIGHT = "#56c7c0"
LAPIS = "#2c4e9e"       # lapis lazuli
BRICK_WHITE = "#efe5cc"  # white glaze
GLAZE_BROWN = "#6b4423"  # brown glaze (outlines of the glazed figures)
LIMESTONE = "#cdbf9f"   # Persepolis limestone
BLACKSTONE = "#2b2f36"  # the dark grey 'black' stone of Persepolis
FIRE = "#e8742f"
FIRE_CORE = "#f7c948"
CARNELIAN = "#b5412c"
NACRE = "#efe9f4"       # the lit Moon
IVORY = "#f5eedf"
NIGHT = "#0e1420"
CARD = "#18212f"
EARTHSHINE = "#26324a"

FV_BOX = (0, 30, 240, 118)   # viewBox of the Faravahar drawing (x, y, w, h)


def _svg(w, h, body, vw=None, vh=None, extra="", vx=0, vy=0) -> str:
    vw = w if vw is None else vw
    vh = h if vh is None else vh
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{vx:g} {vy:g} {vw:g} {vh:g}' width='{w:g}' "
            f"height='{h:g}'{extra}>{body}</svg>")


def _pts(points, nd=2) -> str:
    return " ".join(f"{x:.{nd}f},{y:.{nd}f}" for x, y in points)


def data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


# --------------------------------------------------------------------------------------------- Faravahar
def _wing_left(fills, line, detail=True, sw=0.9) -> str:
    """The left wing: three registers of feathers from the ring (x=108) out to x=6, rising toward the tip.
    Register k runs from the ring to t_end[k]; the stepped ends give the up-swept outline of the wing tip."""
    def x(t):
        return 108 - 102 * t

    def y_top(t):
        return 72 - 9 * t - 16 * t ** 4

    def th(t):
        return 10.5 - 3.6 * t

    t_end = (1.0, 0.92, 0.83)
    out = []
    for k in range(3):
        te = t_end[k]
        ts = [te * i / 24 for i in range(25)]
        top = [(x(t), y_top(t) + k * th(t)) for t in ts]
        bot = [(x(t), y_top(t) + (k + 1) * th(t)) for t in reversed(ts)]
        (xt, yt), (xb, yb) = top[-1], bot[0]
        bulge = x(te) - 0.55 * th(te)
        d = (f"M{top[0][0]:.2f},{top[0][1]:.2f} " + " ".join(f"L{a:.2f},{b:.2f}" for a, b in top[1:])
             + f" C{bulge:.2f},{yt:.2f} {bulge:.2f},{yb:.2f} {xb:.2f},{yb:.2f} "
             + " ".join(f"L{a:.2f},{b:.2f}" for a, b in bot[1:]) + " Z")
        out.append(f"<path d='{d}' fill='{fills[k]}' stroke='{line}' stroke-width='{sw:g}' stroke-linejoin='round'/>")
        if detail:   # feather divisions across the register
            t = 0.07
            while t < te - 0.03:
                y0, y1 = y_top(t) + k * th(t), y_top(t) + (k + 1) * th(t)
                out.append(f"<line x1='{x(t) + 0.7:.2f}' y1='{y0 + 0.4:.2f}' x2='{x(t) - 0.7:.2f}' y2='{y1 - 0.4:.2f}' "
                           f"stroke='{line}' stroke-width='{sw * 0.9:.2f}'/>")
                t += 0.052
    return "".join(out)


def _tail(fills, line, detail=True, sw=0.9) -> str:
    """The tail: a fan of three registers below the ring, the lowest the widest, its end scalloped."""
    regs = ((99, 112, 11, 15), (112, 125, 15, 20), (125, 139, 20, 27))
    out = []
    for k, (ya, yb, wa, wb) in enumerate(regs):
        if k < 2:
            d = f"M{120 - wa},{ya} L{120 + wa},{ya} L{120 + wb},{yb} L{120 - wb},{yb} Z"
        else:   # scalloped feather ends
            n = 6
            d = f"M{120 - wa},{ya} L{120 + wa},{ya} L{120 + wb},{yb}"
            for i in range(n):
                xa = 120 + wb - 2 * wb * i / n
                xb = 120 + wb - 2 * wb * (i + 1) / n
                d += f" Q{(xa + xb) / 2:.2f},{yb + 6:.2f} {xb:.2f},{yb}"
            d += " Z"
        out.append(f"<path d='{d}' fill='{fills[k]}' stroke='{line}' stroke-width='{sw:g}' stroke-linejoin='round'/>")
        if detail:
            n = 4 + 2 * k
            for i in range(1, n):
                f = i / n
                out.append(f"<line x1='{120 - wa + 2 * wa * f:.2f}' y1='{ya + 0.5}' x2='{120 - wb + 2 * wb * f:.2f}' "
                           f"y2='{yb - 0.5 + (4 if k == 2 else 0)}' stroke='{line}' stroke-width='{sw * 0.9:.2f}'/>")
    return "".join(out)


def _streamer_left(color, line, sw=0.9) -> str:
    """One of the two streamers that hang from the ring and end in an outward scroll."""
    spiral = []
    cx, cy = 89.5, 121.5
    for i in range(40):
        t = i / 39
        r = 5.2 * (1 - 0.75 * t)
        a = -math.pi * 0.15 + 2 * math.pi * 1.15 * t
        spiral.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    d = f"M112,96 C104,100 97,104 {spiral[0][0]:.2f},{spiral[0][1]:.2f}"
    p = _pts(spiral)
    return (f"<path d='{d}' fill='none' stroke='{line}' stroke-width='5' stroke-linecap='round'/>"
            f"<polyline points='{p}' fill='none' stroke='{line}' stroke-width='5' stroke-linecap='round' stroke-linejoin='round'/>"
            f"<path d='{d}' fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round'/>"
            f"<polyline points='{p}' fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>")


def _figure(color, line, detail=True, sw=0.9) -> str:
    """The bearded figure rising from the ring, facing left: cylindrical crown, square beard, hair gathered
    at the nape, a wide pleated sleeve; the front hand raised, the other holding a small ring."""
    s = f"stroke='{line}' stroke-width='{sw:g}' stroke-linejoin='round'"
    out = []
    # body (its lower edge is hidden by the ring)
    out.append(f"<path d='M110.5,62 L129.5,62 L127.5,77 L112.5,77 Z' fill='{color}' {s}/>")
    # back arm and the hand holding a ring
    out.append(f"<path d='M114,66 L103.5,71 L102.5,68.6 L112.5,63.5 Z' fill='{color}' {s}/>")
    out.append(f"<circle cx='98.6' cy='69.4' r='3.5' fill='none' stroke='{line}' stroke-width='{2.6 + sw:.2f}'/>")
    out.append(f"<circle cx='98.6' cy='69.4' r='3.5' fill='none' stroke='{color}' stroke-width='1.9'/>")
    # front arm raised, with its wide sleeve hanging
    out.append(f"<path d='M113,62.5 L104,64 L100.5,56.5 L103,55.5 L106,61 L114,59.5 Z' fill='{color}' {s}/>")
    out.append(f"<path d='M113.5,62.5 L104.5,64.5 L105.5,76 L114.5,73.5 Z' fill='{color}' {s}/>")
    out.append(f"<ellipse cx='101.2' cy='54.6' rx='2.1' ry='2.6' fill='{color}' {s}/>")
    # neck, hair, head, beard, crown
    out.append(f"<rect x='117' y='54.5' width='5.5' height='8' fill='{color}' {s}/>")
    out.append(f"<ellipse cx='124.6' cy='54.2' rx='3.6' ry='4.4' fill='{color}' {s}/>")
    out.append(f"<path d='M114.6,44 L124.8,44 C125.6,48 125,52.5 122.5,54.6 L116.5,54.6 L115.2,52.4 L113.2,51.2 "
               f"L114.4,49.6 L114.2,47.4 Z' fill='{color}' {s}/>")
    out.append(f"<path d='M114.6,52.2 L121.8,53 L121.8,61.2 L115.6,61.2 Z' fill='{color}' {s}/>")
    out.append(f"<path d='M114.2,35.5 L125.2,35.5 L124.8,44.6 L114.6,44.6 Z' fill='{color}' {s}/>")
    if detail:
        out.append(f"<circle cx='117' cy='47.3' r='0.8' fill='{line}'/>")
        out.append(f"<line x1='114.4' y1='41.8' x2='125' y2='41.8' stroke='{line}' stroke-width='{sw:g}'/>")
        for yy in (55.5, 57.6, 59.6):   # curls of the beard
            out.append(f"<line x1='115.2' y1='{yy}' x2='121.6' y2='{yy}' stroke='{line}' stroke-width='{sw * 0.8:.2f}'/>")
        for xx in (115.5, 119.5, 123.5):   # pleats of the robe
            out.append(f"<line x1='{xx}' y1='64' x2='{xx + 0.4}' y2='76' stroke='{line}' stroke-width='{sw * 0.8:.2f}'/>")
        for yy in (67.0, 70.5):   # pleats of the sleeve
            out.append(f"<line x1='105' y1='{yy}' x2='113.8' y2='{yy - 1.8}' stroke='{line}' stroke-width='{sw * 0.8:.2f}'/>")
    return "".join(out)


def faravahar(color=GOLD, line=NIGHT, style="gold", detail=True) -> str:
    """The Faravahar's SVG body in its own coordinates (see FV_BOX). style 'gold' is all gold; 'glaze' gives
    the wing and tail registers the Susa glazed-brick colours (turquoise, ochre, lapis)."""
    sw = 0.9 if detail else 1.6
    fills = (TURQUOISE, OCHRE, LAPIS) if style == "glaze" else (color, color, color)
    half = _wing_left(fills, line, detail, sw) + _streamer_left(color, line, sw)
    out = [half, f"<g transform='translate(240 0) scale(-1 1)'>{half}</g>",
           _tail(fills, line, detail, sw), _figure(color, line, detail, sw)]
    # the ring (an annulus; its hole is left open)
    out.append(f"<path d='M106,86 A14,14 0 1 0 134,86 A14,14 0 1 0 106,86 Z M111,86 A9,9 0 1 1 129,86 "
               f"A9,9 0 1 1 111,86 Z' fill='{color}' fill-rule='evenodd' stroke='{line}' stroke-width='{sw:g}'/>")
    if detail:
        out.append(f"<circle cx='120' cy='86' r='11.5' fill='none' stroke='{line}' stroke-width='0.6' stroke-opacity='0.7'/>")
    return "".join(out)


def faravahar_svg(width=96, color=GOLD, line=NIGHT, style="gold", detail=None, label=True) -> str:
    """The Faravahar emblem as a standalone SVG, `width` pixels wide (height follows the 240 x 118 box).
    detail=None chooses the simplified drawing below 40 px."""
    vx, vy, vw, vh = FV_BOX
    if detail is None:
        detail = width >= 40
    extra = " role='img' aria-label='Faravahar'" if label else " role='presentation'"
    return _svg(width, width * vh / vw, faravahar(color, line, style, detail), vw, vh, extra, vx, vy)


# --------------------------------------------------------------------------------------------- rosette
def rosette12(cx, cy, R, petal=GOLD, center=TURQUOISE, ring=GOLD, line=NIGHT) -> str:
    """The Persepolis twelve-petalled rosette: pointed petals round a central boss, in a ring."""
    ri, w = 0.27 * R, 0.21 * R
    tip = 0.86 * R
    out = []
    for k in range(12):
        d = (f"M0,{-ri:.2f} C{w:.2f},{-ri - 0.15 * R:.2f} {w * 0.95:.2f},{-tip + 0.25 * R:.2f} 0,{-tip:.2f} "
             f"C{-w * 0.95:.2f},{-tip + 0.25 * R:.2f} {-w:.2f},{-ri - 0.15 * R:.2f} 0,{-ri:.2f} Z")
        out.append(f"<path d='{d}' transform='translate({cx:.2f} {cy:.2f}) rotate({30 * k})' fill='{petal}' "
                   f"stroke='{line}' stroke-width='{max(R * 0.035, 0.4):.2f}'/>")
    out.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{R * 0.26:.2f}' fill='{center}' stroke='{line}' "
               f"stroke-width='{max(R * 0.04, 0.4):.2f}'/>")
    out.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{R * 0.1:.2f}' fill='{petal}'/>")
    out.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{R * 0.95:.2f}' fill='none' stroke='{ring}' "
               f"stroke-width='{R * 0.09:.2f}'/>")
    return "".join(out)


def rosette_svg(size=28, petal=GOLD, center=TURQUOISE, ring=GOLD) -> str:
    return _svg(size, size, rosette12(50, 50, 48, petal, center, ring), 100, 100, " role='presentation'")


def rosette_band_tile_svg(h=34, petal=GOLD, center=TURQUOISE) -> str:
    """One 40 x 34 repeat of the rosette band (repeat-x): a rosette between two rules, small turquoise
    lozenges at the joins."""
    w = 40
    out = [f"<line x1='0' y1='1.3' x2='{w}' y2='1.3' stroke='{GOLD}' stroke-width='1.3'/>",
           f"<line x1='0' y1='32.7' x2='{w}' y2='32.7' stroke='{GOLD}' stroke-width='1.3'/>",
           rosette12(20, 17, 13.6, petal, center, GOLD)]
    for x in (0, w):
        out.append(f"<rect x='{x - 3.2}' y='{17 - 3.2}' width='6.4' height='6.4' fill='{TURQ_LIGHT}' "
                   f"transform='rotate(45 {x} 17)'/>")
    return _svg(w * h / 34, h, "".join(out), w, 34, " role='presentation'")


# --------------------------------------------------------------------------------------------- lotus and bud
def _lotus(x, color, line) -> str:
    s = f"stroke='{line}' stroke-width='0.8' stroke-linejoin='round'"
    return (f"<path d='M{x - 1},31 L{x - 1},20 L{x + 1},20 L{x + 1},31 Z' fill='{color}'/>"
            # two outer sepals curling outward
            f"<path d='M{x},21 C{x - 4},18 {x - 9},14 {x - 11},9 C{x - 12.5},12 {x - 10},14 {x - 8.5},13.5 "
            f"C{x - 7},17 {x - 3},20 {x},22 Z' fill='{color}' {s}/>"
            f"<path d='M{x},21 C{x + 4},18 {x + 9},14 {x + 11},9 C{x + 12.5},12 {x + 10},14 {x + 8.5},13.5 "
            f"C{x + 7},17 {x + 3},20 {x},22 Z' fill='{color}' {s}/>"
            # inner petals and the central petal
            f"<path d='M{x},21 C{x - 5},17 {x - 6},11 {x - 5},6.5 C{x - 2.5},10 {x - 1},15 {x},21 Z' fill='{color}' {s}/>"
            f"<path d='M{x},21 C{x + 5},17 {x + 6},11 {x + 5},6.5 C{x + 2.5},10 {x + 1},15 {x},21 Z' fill='{color}' {s}/>"
            f"<path d='M{x},21 C{x - 3},15 {x - 2.6},8 {x},3.5 C{x + 2.6},8 {x + 3},15 {x},21 Z' fill='{color}' {s}/>")


def _bud(x, color, sepal, line) -> str:
    s = f"stroke='{line}' stroke-width='0.8' stroke-linejoin='round'"
    return (f"<path d='M{x - 1},31 L{x - 1},21 L{x + 1},21 L{x + 1},31 Z' fill='{sepal}'/>"
            f"<path d='M{x},22 C{x - 6},19.5 {x - 5},12 {x},7.5 C{x + 5},12 {x + 6},19.5 {x},22 Z' fill='{color}' {s}/>"
            f"<path d='M{x},22.5 C{x - 4},21.5 {x - 6},18.5 {x - 6.5},15.5 C{x - 4},17 {x - 2},19 {x},20 Z' fill='{sepal}' {s}/>"
            f"<path d='M{x},22.5 C{x + 4},21.5 {x + 6},18.5 {x + 6.5},15.5 C{x + 4},17 {x + 2},19 {x},20 Z' fill='{sepal}' {s}/>")


def lotus_frieze_tile_svg(h=34, lotus=GOLD, bud=TURQ_LIGHT, line=NIGHT) -> str:
    """One 60 x 34 repeat (repeat-x) of the lotus-and-bud frieze: an open lotus and a closed bud on stems
    joined by looping arcs."""
    w = 60
    out = [f"<line x1='0' y1='33' x2='{w}' y2='33' stroke='{GOLD}' stroke-width='1.3'/>"]
    for xa in (-15, 15, 45):    # arcs joining each stem to the next (cut by the tile edges, seamless)
        out.append(f"<path d='M{xa},26 Q{xa + 15},35 {xa + 30},26' fill='none' stroke='{GOLD_DEEP}' stroke-width='1.6'/>")
    out.append(_lotus(15, lotus, line))
    out.append(_bud(45, bud, lotus, line))
    return _svg(w * h / 34, h, "".join(out), w, 34, " role='presentation'")


# --------------------------------------------------------------------------------------------- capitals
def _protome_right(kind, color, line) -> str:
    """A kneeling forepart facing right, its back against x=0 (the saddle of the capital). 'bull' or 'griffin'."""
    s = f"stroke='{line}' stroke-width='0.9' stroke-linejoin='round'"
    if kind == "griffin":
        head = ("C32,7 36,6 38,9 L39,1 L42.5,8 L45,3.5 L46.5,10.5 C52,10.5 57.5,14 58,20 L55.5,25.5 L54,21.5 "
                "C52,22.5 49.5,23.5 47,23.5 C45,24.5 43.5,24.5 42,24")
        extra = f"<circle cx='49' cy='15' r='1.1' fill='{line}'/>"
    else:
        head = ("C32,6 36,8 40,12 L52,16 C56,17 58.5,20 57.5,24 L50,26.5 C46,26.5 44,24.5 42,24")
        extra = (f"<path d='M38.5,11 C39.5,3 45,-2.5 51,0.5 C46.5,1.5 43.5,5 42.5,11.5 Z' fill='{color}' {s}/>"
                 f"<path d='M38.5,13 L30.5,9.5 L35.5,16 Z' fill='{color}' {s}/>"
                 f"<circle cx='47.5' cy='17.5' r='1.1' fill='{line}'/>")
    body = (f"M0,10 L26,6 {head} C40,28 38,32 36,34 L36,40 L44,40 L44,43 L29,43 L27.5,36 "
            f"C22,36 16,38 12,40 L12,43 L0,43 Z")
    deco = (f"<path d='M30,10 C33,17 34,24 33,31' fill='none' stroke='{line}' stroke-width='0.9'/>"
            f"<path d='M26,9 C29,16 30,24 29,32' fill='none' stroke='{line}' stroke-width='0.7'/>")
    for yy in (27, 31, 35):   # curls of the chest
        deco += f"<circle cx='{36 - (yy - 27) * 0.25:.2f}' cy='{yy}' r='1.4' fill='none' stroke='{line}' stroke-width='0.7'/>"
    return f"<path d='{body}' fill='{color}' {s}/>" + extra + deco


def capital(cx, top, s=1.0, kind="bull", color=GOLD, line=NIGHT) -> str:
    """A double-protome capital (two foreparts back to back), with the roof beam end in the saddle, on a block
    with two volutes and a fluted shaft. Drawn in a box 124 wide and 72 high whose top centre is (cx, top)."""
    half = _protome_right(kind, color, line)
    beam = f"<rect x='-7' y='1.5' width='14' height='8.5' fill='{GOLD_DEEP}' stroke='{line}' stroke-width='0.9'/>"
    block = (f"<rect x='-34' y='43' width='68' height='5' fill='{color}' stroke='{line}' stroke-width='0.9'/>"
             f"<rect x='-20' y='48' width='40' height='9' fill='{color}' stroke='{line}' stroke-width='0.9'/>")
    for sx in (-1, 1):
        sp = []
        for i in range(36):
            t = i / 35
            r = 4.6 * (1 - 0.8 * t)
            a = 2 * math.pi * 1.1 * t
            sp.append((sx * (21 + r * math.cos(a)), 53 + r * math.sin(a) * sx))
        block += f"<circle cx='{sx * 21}' cy='53' r='5.2' fill='{color}' stroke='{line}' stroke-width='0.9'/>"
        block += f"<polyline points='{_pts(sp)}' fill='none' stroke='{line}' stroke-width='0.9'/>"
    block += f"<rect x='-11' y='57' width='22' height='15' fill='{color}' stroke='{line}' stroke-width='0.9'/>"
    for xx in (-6.5, -2.2, 2.2, 6.5):
        block += f"<line x1='{xx}' y1='58' x2='{xx}' y2='72' stroke='{line}' stroke-width='0.8'/>"
    return (f"<g transform='translate({cx:.2f} {top:.2f}) scale({s:g})'>{beam}{half}"
            f"<g transform='scale(-1 1)'>{half}</g>{block}</g>")


def capital_svg(width=124, kind="bull", color=GOLD, line=NIGHT) -> str:
    return _svg(width, width * 76 / 124, capital(62, 3, 1.0, kind, color, line), 124, 76,
                f" role='img' aria-label='Persepolis {kind} capital'")


def divider_svg(width=360, kind="bull") -> str:
    """A horizontal divider: a small capital in the middle, gold rules to each side ending in rosettes."""
    h = 40
    c = width / 2
    out = []
    for y, sw in ((18, 1.4), (22, 0.8)):
        out.append(f"<line x1='14' y1='{y}' x2='{c - 34}' y2='{y}' stroke='{GOLD}' stroke-width='{sw}'/>")
        out.append(f"<line x1='{c + 34}' y1='{y}' x2='{width - 14}' y2='{y}' stroke='{GOLD}' stroke-width='{sw}'/>")
    out.append(rosette12(9, 20, 8, GOLD, TURQUOISE, GOLD))
    out.append(rosette12(width - 9, 20, 8, GOLD, TURQUOISE, GOLD))
    out.append(capital(c, 1.5, 0.5, kind))
    return _svg(width, h, "".join(out), width, h, " role='presentation'")


# --------------------------------------------------------------------------------------------- Gah icons
def _sun(cx, cy, r, color=GOLD, rays=OCHRE, n=12, half=False) -> str:
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        if half and math.sin(a) > 0.01:
            continue
        x1, y1 = cx + r * 1.32 * math.cos(a), cy + r * 1.32 * math.sin(a)
        x2, y2 = cx + r * 1.78 * math.cos(a), cy + r * 1.78 * math.sin(a)
        out.append(f"<line x1='{x1:.2f}' y1='{y1:.2f}' x2='{x2:.2f}' y2='{y2:.2f}' stroke='{rays}' "
                   f"stroke-width='{r * 0.24:.2f}' stroke-linecap='round'/>")
    if half:
        out.append(f"<path d='M{cx - r:.2f},{cy:.2f} A{r:.2f},{r:.2f} 0 0 1 {cx + r:.2f},{cy:.2f} Z' fill='{color}'/>")
    else:
        out.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{r:.2f}' fill='{color}'/>")
    return "".join(out)


def _star(cx, cy, r, color=IVORY) -> str:
    p = []
    for k in range(8):
        rr = r if k % 2 == 0 else r * 0.32
        a = math.pi / 4 * k - math.pi / 2
        p.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return f"<polygon points='{_pts(p)}' fill='{color}'/>"


def _arrow(cx, y, up, color) -> str:
    d = -1 if up else 1
    return (f"<path d='M{cx - 7},{y} L{cx},{y + 7 * d} L{cx + 7},{y}' fill='none' stroke='{color}' "
            f"stroke-width='4' stroke-linecap='round' stroke-linejoin='round'/>")


GAH_ICON = {   # gah key -> picture
    "havan": "sunrise", "rapithwin": "noon", "second_havan": "noon", "uziran": "afternoon",
    "aiwisruthrem": "sunset", "ushahin": "night",
}


def gah_icon_svg(key: str, size: int = 32) -> str:
    """An icon for a Gah (watch of the day). key: a gah key or one of sunrise, noon, afternoon, sunset, night."""
    pic = GAH_ICON.get(key, key)
    horizon = f"<line x1='6' y1='74' x2='94' y2='74' stroke='{TURQ_LIGHT}' stroke-width='5' stroke-linecap='round'/>"
    ground = f"<line x1='20' y1='86' x2='80' y2='86' stroke='{TURQUOISE}' stroke-width='4' stroke-linecap='round'/>"
    if pic == "sunrise":
        body = _sun(50, 70, 20, half=True) + horizon + ground + _arrow(50, 22, True, IVORY)
    elif pic == "noon":
        body = _sun(50, 42, 19) + horizon
    elif pic == "afternoon":
        body = _sun(66, 50, 16) + horizon + (f"<path d='M14,60 Q40,22 82,30' fill='none' stroke='{GOLD_DEEP}' "
                                             f"stroke-width='3' stroke-dasharray='5 5'/>")
    elif pic == "sunset":
        body = (_sun(50, 72, 20, color=OCHRE, rays=CARNELIAN, half=True) + horizon + ground
                + _arrow(50, 15, False, IVORY) + _star(82, 20, 8))
    elif pic == "night":
        body = (moon_body(44, 48, 28, 0.25, False, 0.0, NACRE, EARTHSHINE, dark_opacity=0.0)
                + _star(78, 22, 9) + _star(82, 62, 6) + _star(20, 18, 5))
    else:
        raise KeyError(key)
    return _svg(size, size, body, 100, 100, f" role='img' aria-label='{pic}'")


# --------------------------------------------------------------------------------------------- fire altar
def fire_altar_svg(size: int = 24, stone=LIMESTONE, line=NIGHT) -> str:
    """The stepped Achaemenid fire altar (Naqsh-e Rostam tomb reliefs) with its flame."""
    s = f"stroke='{line}' stroke-width='2' stroke-linejoin='round'"
    steps = ""
    for x0, x1, y0, y1 in ((22, 78, 89, 96), (29, 71, 82, 89), (36, 64, 75, 82),   # base
                           (36, 64, 41, 48), (29, 71, 34, 41), (22, 78, 27, 34)):  # top
        steps += f"<rect x='{x0}' y='{y0}' width='{x1 - x0}' height='{y1 - y0}' fill='{stone}' {s}/>"
    shaft = f"<rect x='42' y='48' width='16' height='27' fill='{stone}' {s}/>"
    flame = (f"<path d='M50,2 C58,12 66,16 64,25 L36,25 C34,16 40,14 44,8 C45,13 47,15 49,15 C47,10 48,6 50,2 Z' "
             f"fill='{FIRE}'/>"
             f"<path d='M50,10 C55,16 58,20 57,25 L43,25 C42,20 46,17 50,10 Z' fill='{FIRE_CORE}'/>")
    return _svg(size, size, flame + steps + shaft, 100, 100, " role='img' aria-label='fire altar'")


# --------------------------------------------------------------------------------------------- the Moon
def moon_body(cx, cy, r, illum, waxing=True, tilt=0.0, lit=NACRE, dark=EARTHSHINE, rim=None,
              dark_opacity=1.0) -> str:
    """The Moon's disc: the dark part (earthshine) and the lit part. illum 0..1 is the lit fraction.
    waxing=True puts the lit limb on the right (northern hemisphere, Moon upright); tilt turns the lit limb
    clockwise by that many degrees."""
    k = min(max(float(illum), 0.0), 1.0)
    out = [f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{r:.2f}' fill='{dark}' fill-opacity='{dark_opacity:g}'/>"]
    if k > 0.003:
        rx = r * abs(1 - 2 * k)
        sweep = 0 if k < 0.5 else 1
        d = (f"M{cx:.2f},{cy - r:.2f} A{r:.2f},{r:.2f} 0 0 1 {cx:.2f},{cy + r:.2f} "
             f"A{rx:.2f},{r:.2f} 0 0 {sweep} {cx:.2f},{cy - r:.2f} Z")
        tf = f"rotate({tilt:.2f} {cx:.2f} {cy:.2f})"
        if not waxing:
            tf += f" translate({2 * cx:.2f} 0) scale(-1 1)"
        out.append(f"<path d='{d}' fill='{lit}' transform='{tf}'/>")
    if rim:
        out.append(f"<circle cx='{cx:.2f}' cy='{cy:.2f}' r='{r:.2f}' fill='none' stroke='{rim}' "
                   f"stroke-width='{max(r * 0.04, 0.6):.2f}'/>")
    return "".join(out)


def moon_phase_svg(illum: float, waxing: bool = True, size: int = 40, tilt: float = 0.0,
                   lit: str = NACRE, dark: str = EARTHSHINE, rim: str | None = "#5b6a94") -> str:
    """The Moon as it looks: lit fraction illum (0..1), lit limb on the right when waxing."""
    pct = round(100 * min(max(illum, 0.0), 1.0))
    return _svg(size, size, moon_body(50, 50, 46, illum, waxing, tilt, lit, dark, rim), 100, 100,
                extra=f" role='img' aria-label='Moon {pct}% lit, {'waxing' if waxing else 'waning'}'")


def moon_glyph_svg(phase: str, size: int = 22) -> str:
    """Named glyphs for the Mah Niyayesh days: 'new', 'first_quarter', 'full', 'last_quarter'."""
    illum, wax = {"new": (0.0, True), "first_quarter": (0.5, True), "full": (1.0, True),
                  "last_quarter": (0.5, False)}[phase]
    return moon_phase_svg(illum, wax, size)


# --------------------------------------------------------------------------------------------- app icons
def _glow_defs(gid="glow", opacity=0.9) -> str:
    return (f"<defs><radialGradient id='{gid}' cx='0.5' cy='0.5' r='0.5'>"
            f"<stop offset='0' stop-color='{LAPIS}' stop-opacity='{opacity}'/>"
            f"<stop offset='0.55' stop-color='{LAPIS}' stop-opacity='{opacity / 2:.2f}'/>"
            f"<stop offset='1' stop-color='{LAPIS}' stop-opacity='0'/></radialGradient></defs>")


def _fv_at(cx, cy, scale, style="gold", detail=True) -> str:
    """The Faravahar placed with the centre of its box at (cx, cy)."""
    vx, vy, vw, vh = FV_BOX
    x0 = cx - (vx + vw / 2) * scale
    y0 = cy - (vy + vh / 2) * scale
    return f"<g transform='translate({x0:.2f} {y0:.2f}) scale({scale:g})'>{faravahar(GOLD, NIGHT, style, detail)}</g>"


def icon_svg(size: int = 512, maskable: bool = False, rounded: bool = False) -> str:
    """The app icon: the Faravahar in gold over a night sky, above a band of turquoise glazed brick with three
    Persepolis rosettes. maskable=True puts all the art inside the central circle of radius 40% (the safe zone
    of a maskable icon) on a full-bleed field."""
    S = 512
    bg = (f"<rect width='{S}' height='{S}' rx='96' fill='{NIGHT}'/>" if rounded
          else f"<rect width='{S}' height='{S}' fill='{NIGHT}'/>")
    if not maskable:
        art = ["<circle cx='256' cy='200' r='250' fill='url(#glow)'/>",
               _fv_at(256, 214, 1.95),
               f"<rect x='0' y='402' width='{S}' height='74' fill='{TURQUOISE}'/>",
               f"<line x1='0' y1='402' x2='{S}' y2='402' stroke='{GOLD}' stroke-width='5'/>",
               f"<line x1='0' y1='476' x2='{S}' y2='476' stroke='{GOLD}' stroke-width='5'/>"]
        for x in (106, 256, 406):
            art.append(rosette12(x, 439, 30, BRICK_WHITE, OCHRE, OCHRE, GLAZE_BROWN))
        for x in (31, 181, 331, 481):
            art.append(f"<rect x='{x - 8}' y='431' width='16' height='16' fill='{OCHRE}' transform='rotate(45 {x} 439)'/>")
        body = "".join(art)
    else:
        art = ["<circle cx='256' cy='240' r='170' fill='url(#glow)'/>",
               _fv_at(256, 236, 1.48),
               f"<rect x='150' y='334' width='212' height='44' rx='4' fill='{TURQUOISE}' stroke='{GOLD}' stroke-width='3'/>"]
        for x in (200, 256, 312):
            art.append(rosette12(x, 356, 18, BRICK_WHITE, OCHRE, OCHRE, GLAZE_BROWN))
        body = "".join(art)
    return _svg(size, size, _glow_defs() + bg + body, S, S)


def icon_small_svg(size: int = 32) -> str:
    """A simpler drawing for 16-48 px (favicon, small ICO sizes): the Faravahar without hatching, enlarged
    so that the figure, ring and tail fill the square (the wing tips run off the edges), on the night field."""
    S = 512
    body = (f"<rect width='{S}' height='{S}' fill='{NIGHT}'/>"
            "<circle cx='256' cy='230' r='300' fill='url(#glow)'/>"
            + _fv_at(256, 268, 3.6, detail=False))
    return _svg(size, size, _glow_defs() + body, S, S)



# --------------------------------------------------------------------------------------------- 'face the light' compass
# Added at app assembly (Nov 2026), after Sky Taqwim's qibla compass: a dial with N, E, S, W and a Persepolis
# rosette at the centre, and an arrow carrying the light to face (the Sun, or the Moon in its phase). Both are
# drawn in the same 160 x 160 frame so that the arrow can sit on the dial and be turned.
def compass_dial_svg(size: int = 160) -> str:
    c, R = 80, 74
    out = [f"<circle cx='{c}' cy='{c}' r='{R}' fill='{CARD}' stroke='{GOLD}' stroke-width='2.2'/>",
           f"<circle cx='{c}' cy='{c}' r='{R - 5}' fill='none' stroke='{GOLD}' stroke-width='0.8' stroke-opacity='0.6'/>"]
    for deg in range(0, 360, 15):
        L = 9 if deg % 90 == 0 else (6 if deg % 45 == 0 else 3.5)
        a = math.radians(deg - 90)
        x1, y1 = c + (R - 5) * math.cos(a), c + (R - 5) * math.sin(a)
        x2, y2 = c + (R - 5 - L) * math.cos(a), c + (R - 5 - L) * math.sin(a)
        out.append(f"<line x1='{x1:.2f}' y1='{y1:.2f}' x2='{x2:.2f}' y2='{y2:.2f}' stroke='{GOLD}' "
                   f"stroke-width='{1.6 if L > 5 else 1}'/>")
    for lab, deg in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        a = math.radians(deg - 90)
        x, y = c + 53 * math.cos(a), c + 53 * math.sin(a) + 5
        col = GOLD if lab == "N" else IVORY
        out.append(f"<text x='{x:.1f}' y='{y:.1f}' text-anchor='middle' font-family='Segoe UI, Helvetica, Arial, "
                   f"sans-serif' font-size='14' font-weight='700' fill='{col}'>{lab}</text>")
    out.append(rosette12(c, c, 15, petal=GOLD_DEEP, center=TURQUOISE, ring=GOLD_DEEP))
    return _svg(size, size, "".join(out), 160, 160, extra=" role='presentation'")


def light_arrow_svg(size: int = 160, light: str = "sun", illum: float = 1.0, waxing: bool = True) -> str:
    """A gold arrow pointing to the top of the drawing with the light to face at its tip: the Sun, or the
    Moon drawn in its present phase. light='lamp' gives no arrow (an empty, transparent layer)."""
    c = 80
    if light == "lamp":
        return _svg(size, size, "", 160, 160, extra=" role='presentation'")
    if light == "moon":
        tip = moon_body(c, 17, 11, illum, waxing, rim=GOLD)
    else:
        tip = _sun(c, 17, 7.5, color=GOLD, rays=FIRE_CORE)
    arrow = (f"<polygon points='{c},33 {c - 12},55 {c - 4.5},53 {c - 4.5},{c + 26} {c + 4.5},{c + 26} {c + 4.5},53 "
             f"{c + 12},55' fill='{GOLD}' stroke='{NIGHT}' stroke-width='1.1' stroke-linejoin='round'/>")
    hub = f"<circle cx='{c}' cy='{c}' r='4.2' fill='{NIGHT}' stroke='{GOLD}' stroke-width='1.6'/>"
    return _svg(size, size, arrow + tip + hub, 160, 160, extra=" role='presentation'")
