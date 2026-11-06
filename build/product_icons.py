"""Novaroma product icon theme: VS Code's UI icons redrawn in the Nova Roma line style.

Icons are drawn as rounded 2px strokes on a 24px grid, flattened to filled outlines with picosvg,
and built into a woff font with fontTools. Keys are codicon ids, so every place in VS Code
that uses that codicon gets the Novaroma version.
"""
import json, math, os, subprocess, tempfile
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib.removeOverlaps import removeOverlaps
from picosvg.svg import SVG

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = f"{ROOT}/product-icons"


def S(d):            # stroked path
    return ("s", d)


def F(d):            # filled path
    return ("f", d)


def circ(cx, cy, r):
    return f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0z"


def rect(x, y, w, h, r):
    return (f"M{x + r} {y}H{x + w - r}A{r} {r} 0 0 1 {x + w} {y + r}V{y + h - r}A{r} {r} 0 0 1 {x + w - r} {y + h}"
            f"H{x + r}A{r} {r} 0 0 1 {x} {y + h - r}V{y + r}A{r} {r} 0 0 1 {x + r} {y}z")


def gear(cx=12, cy=12, ro=9, ri=7, teeth=8):
    pts = []
    for i in range(teeth * 4):
        a = math.pi * 2 * i / (teeth * 4) - math.pi / 2
        r = ro if (i % 4) in (0, 1) else ri
        pts.append(f"{cx + r * math.cos(a):.2f} {cy + r * math.sin(a):.2f}")
    return "M" + "L".join(pts) + "z"


BELL = "M18 16.5V11a6 6 0 0 0-12 0v5.5L4.5 19h15zM10 21.5h4"
LIGHT_RECT = rect(3, 4, 18, 16, 2.5)

ICONS = {
    # activity bar
    "files": [S("M9 2.5h6.5l4.5 4.5v9.5"), S("M4 8a2 2 0 0 1 2-2h6l4.5 4.5V20a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"), S("M12 6v4.5h4.5")],
    "search": [S(circ(10.5, 10.5, 6.5)), S("M15.5 15.5L21 21")],
    "source-control": [S(circ(6, 5, 2.2)), S(circ(6, 19, 2.2)), S(circ(18, 7, 2.2)), S("M6 7.2v9.6M18 9.2v.8a4 4 0 0 1-4 4h-4a4 4 0 0 0-4 2.8")],
    "debug-alt": [S("M5 4v14l11-7z"), S(circ(18, 18, 3))],
    "extensions": [S(rect(3, 13, 8, 8, 1.8)), S(rect(13, 13, 8, 8, 1.8)), S(rect(3, 3, 8, 8, 1.8)), S(rect(14, 2, 7, 7, 1.8))],
    "account": [S(circ(12, 8, 4)), S("M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7")],
    "settings-gear": [S(gear()), S(circ(12, 12, 3))],
    "gear": [S(gear()), S(circ(12, 12, 3))],
    "beaker": [S("M8.5 3h7M10 3v6.2L4.6 18.4A2 2 0 0 0 6.3 21.5h11.4a2 2 0 0 0 1.7-3.1L14 9.2V3M7.2 15h9.6")],
    "remote-explorer": [S(rect(3, 4, 18, 12, 2.5)), S("M8 20.5h8M12 16v4.5")],
    "remote": [S("M4 12l4-4M4 12l4 4M20 12l-4-4M20 12l-4 4")],
    # navigation
    "chevron-right": [S("M9.5 6l6 6-6 6")],
    "chevron-left": [S("M14.5 6l-6 6 6 6")],
    "chevron-down": [S("M6 9.5l6 6 6-6")],
    "chevron-up": [S("M6 14.5l6-6 6 6")],
    "triangle-right": [F("M9 5.5l7.5 6.5L9 18.5z")],
    "triangle-down": [F("M5.5 9L12 16.5 18.5 9z")],
    "arrow-right": [S("M4.5 12h15M13.5 6l6 6-6 6")],
    "arrow-left": [S("M19.5 12h-15M10.5 6l-6 6 6 6")],
    "arrow-up": [S("M12 19.5v-15M6 10.5l6-6 6 6")],
    "arrow-down": [S("M12 4.5v15M6 13.5l6 6 6-6")],
    "arrow-swap": [S("M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4")],
    # editor & view actions
    "close": [S("M6 6l12 12M18 6L6 18")],
    "add": [S("M12 5v14M5 12h14")],
    "remove": [S("M5 12h14")],
    "check": [S("M5 12.5l4.5 4.5L19 7")],
    "check-all": [S("M2.5 12.5L7 17 16.5 7M12 17l9.5-10")],
    "pass": [S(circ(12, 12, 9)), S("M8 12.3l2.8 2.8L16.2 9.5")],
    "ellipsis": [F(circ(6, 12, 1.7)), F(circ(12, 12, 1.7)), F(circ(18, 12, 1.7))],
    "kebab-vertical": [F(circ(12, 6, 1.7)), F(circ(12, 12, 1.7)), F(circ(12, 18, 1.7))],
    "menu": [S("M4 6h16M4 12h16M4 18h16")],
    "split-horizontal": [S(LIGHT_RECT), S("M12 4v16")],
    "split-vertical": [S(LIGHT_RECT), S("M3 12h18")],
    "refresh": [S("M20 12a8 8 0 1 1-2.4-5.7"), S("M20 3.5v4.8h-4.8")],
    "collapse-all": [S("M7.5 3H18a3 3 0 0 1 3 3v10.5"), S(rect(3, 7, 14, 14, 2.5)), S("M7 14h6")],
    "expand-all": [S("M7.5 3H18a3 3 0 0 1 3 3v10.5"), S(rect(3, 7, 14, 14, 2.5)), S("M7 14h6M10 11v6")],
    "new-file": [S("M12 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6l5 5v4"), S("M13 3v5h5"), S("M18 15v6M15 18h6")],
    "new-folder": [S("M11 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h4l2.2 2.5H19a2 2 0 0 1 2 2V12"), S("M18 15v6M15 18h6")],
    "filter": [S("M3.5 5h17l-6.5 8v6l-4 2v-8z")],
    "edit": [S("M4 20l1-4.5L15.5 5a2.1 2.1 0 0 1 3 0l.5.5a2.1 2.1 0 0 1 0 3L8.5 19z"), S("M14 6.5l3.5 3.5")],
    "trash": [S("M4 7h16M9 7V4.5h6V7M6.5 7l1 13a1.5 1.5 0 0 0 1.5 1.5h6a1.5 1.5 0 0 0 1.5-1.5l1-13M10 11v6M14 11v6")],
    "copy": [S(rect(8, 8, 13, 13, 2.5)), S("M16 8V5.5A2.5 2.5 0 0 0 13.5 3h-8A2.5 2.5 0 0 0 3 5.5v8A2.5 2.5 0 0 0 5.5 16H8")],
    "link-external": [S("M14 4h6v6M20 4l-9 9M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4")],
    "pin": [S("M8.5 3h7M10 3v5.5L6.5 13h11L14 8.5V3M12 13v8")],
    "pinned": [F("M10 3v5.5L6.5 13h11L14 8.5V3z"), S("M8.5 3h7M10 3v5.5L6.5 13h11L14 8.5V3M12 13v8")],
    "circle-filled": [F(circ(12, 12, 5))],
    "circle-large-outline": [S(circ(12, 12, 8.5))],
    "circle-large-filled": [F(circ(12, 12, 9.5))],
    "clear-all": [S("M4 6h10M4 11h7M4 16h5M14 13l6 6M20 13l-6 6")],
    "history": [S("M4 12a8 8 0 1 0 2.4-5.7"), S("M4 3.5v4.8h4.8"), S("M12 8v4.5l3 2")],
    "discard": [S("M8 4L3.5 8.5 8 13M3.5 8.5H14a6 6 0 0 1 0 12h-3")],
    "list-tree": [S("M4 5h6M8 12h6M8 19h6M6 5v14H8M6 12h2"), S("M14 5h6")],
    "list-flat": [S("M4 6h16M4 12h16M4 18h16")],
    "go-to-file": [S("M12 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6l5 5v4"), S("M13 3v5h5"), S("M15 18h6M18.5 15.5L21 18l-2.5 2.5")],
    "save": [S("M5 3h11l4 4v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 1-2z"), S("M8 3v5h7V3M8 21v-6h8v6")],
    # notifications & status
    "bell": [S(BELL)],
    "bell-dot": [S(BELL), F(circ(18.5, 5, 3.2))],
    "bell-slash": [S(BELL), S("M3 3l18 18")],
    "sync": [S("M4 11a8 8 0 0 1 14-4.5M18.5 3v4h-4M20 13a8 8 0 0 1-14 4.5M5.5 21v-4h4")],
    "git-branch": [S(circ(6, 6, 2.2)), S(circ(6, 18, 2.2)), S(circ(18, 6, 2.2)), S("M6 8.2v7.6M18 8.2c0 5.3-6.5 4-11 8.3")],
    "git-commit": [S(circ(12, 12, 3.5)), S("M3 12h5.5M15.5 12H21")],
    "git-pull-request": [S(circ(6, 6, 2.2)), S(circ(6, 18, 2.2)), S(circ(18, 18, 2.2)),
                         S("M6 8.2v7.6M18 15.8V9a3 3 0 0 0-3-3h-4M13 3.5L10.5 6 13 8.5")],
    "error": [S(circ(12, 12, 9)), S("M9 9l6 6M15 9l-6 6")],
    "warning": [S("M12 3.5L21.5 20h-19z"), S("M12 10v4.5"), F(circ(12, 17.3, 1.2))],
    "info": [S(circ(12, 12, 9)), S("M12 11v6"), F(circ(12, 7.6, 1.2))],
    "lightbulb": [S("M9 17h6M10 20.5h4M9 17c0-2-3-3.5-3-7a6 6 0 0 1 12 0c0 3.5-3 5-3 7")],
    "lightbulb-autofix": [S("M9 17h6M10 20.5h4M9 17c0-2-3-3.5-3-7a6 6 0 0 1 12 0c0 3.5-3 5-3 7"), F(circ(19.5, 4.5, 2.2))],
    # run & debug
    "play": [S("M7 4.5v15l12-7.5z")],
    "debug-start": [S("M7 4.5v15l12-7.5z")],
    "run-all": [S("M4 4.5v15l10-7.5z"), S("M15 4.5l7 7.5-7 7.5")],
    "debug-continue": [S("M5 5v14M9 5l10 7-10 7z")],
    "debug-pause": [S("M8 5v14M16 5v14")],
    "debug-stop": [S(rect(5, 5, 14, 14, 2.5))],
    "debug-restart": [S("M4 12a8 8 0 1 0 2.4-5.7"), S("M4 3.5v4.8h4.8")],
    "debug-step-over": [S("M4 13a8 8 0 0 1 15.5-3"), S("M20.2 5v5h-5"), F(circ(12, 19, 1.9))],
    "debug-step-into": [S("M12 3v10M8 9l4 4 4-4"), F(circ(12, 19.5, 1.9))],
    "debug-step-out": [S("M12 13V3M8 7l4-4 4 4"), F(circ(12, 19.5, 1.9))],
    "debug-disconnect": [S("M7 7l10 10M17 7L7 17"), S(circ(12, 12, 9))],
    "debug-breakpoint": [F(circ(12, 12, 5.5))],
    "terminal": [S(LIGHT_RECT), S("M7 9l3 3-3 3M12.5 15H17")],
    "output": [S(LIGHT_RECT), S("M7 9h10M7 12.5h10M7 16h6")],
    # layout toggles (on = region filled, off = outline only)
    "layout-sidebar-left": [S(LIGHT_RECT), F(rect(4, 5, 5, 14, 1.5)), S("M9 4v16")],
    "layout-sidebar-left-off": [S(LIGHT_RECT), S("M9 4v16")],
    "layout-sidebar-right": [S(LIGHT_RECT), F(rect(15, 5, 5, 14, 1.5)), S("M15 4v16")],
    "layout-sidebar-right-off": [S(LIGHT_RECT), S("M15 4v16")],
    "layout-panel": [S(LIGHT_RECT), F(rect(4, 14, 16, 5, 1.5)), S("M3 14h18")],
    "layout-panel-off": [S(LIGHT_RECT), S("M3 14h18")],
    "layout": [S(LIGHT_RECT), S("M9 4v16M9 13h12")],
    # used by the Novaroma extension itself
    "symbol-color": [S("M12 3a9 9 0 1 0 0 18c1.6 0 2.2-1.1 2.2-2.1S13 17.3 13 16.3s1-1.8 2.2-1.8h2.4A3.4 3.4 0 0 0 21 11.1C21 6.6 17 3 12 3z"),
                     F(circ(7.5, 11.5, 1.4)), F(circ(10, 7.2, 1.4)), F(circ(14.8, 7.2, 1.4))],
    "color-mode": [S(circ(12, 12, 9)), F("M12 3a9 9 0 0 1 0 18z")],
    "calendar": [S(rect(3, 5, 18, 16, 2.5)), S("M3 10h18M8 3v4M16 3v4")],
    "eye": [S("M2.5 12S6 5 12 5s9.5 7 9.5 7-3.5 7-9.5 7S2.5 12 2.5 12z"), S(circ(12, 12, 3))],
    "device-camera-video": [S(rect(3, 6, 12, 12, 2.5)), S("M15 10.5l6-3.5v10l-6-3.5")],
    "screen-normal": [S("M9 3v6H3M15 3v6h6M9 21v-6H3M15 21v-6h6")],
    "home": [S("M3.5 11L12 4l8.5 7M6 9.5V20h4.5v-5h3v5H18V9.5")],
    "star-empty": [S("M12 3l2.7 5.6 6.1.8-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1L3.2 9.4l6.1-.8z")],
    "star-full": [F("M12 3l2.7 5.6 6.1.8-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1L3.2 9.4l6.1-.8z")],
}


def icon_svg(parts, stroke="#000", sw=2):
    body = []
    for kind, d in parts:
        if kind == "s":
            body.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
                        f'stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            body.append(f'<path d="{d}" fill="{stroke}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">{"".join(body)}</svg>'


def build():
    os.makedirs(f"{OUT}/svg", exist_ok=True)
    upm, asc, desc = 1024, 960, -64
    k = upm / 24
    order, glyphs, cmap, defs = [".notdef"], {}, {}, {}
    pen = TTGlyphPen(None)
    glyphs[".notdef"] = pen.glyph()
    for i, (cid, parts) in enumerate(ICONS.items()):
        raw = icon_svg(parts)
        with open(f"{OUT}/svg/{cid}.svg", "w") as f:
            f.write(raw)
        pico = SVG.fromstring(raw).topicosvg()           # strokes -> filled outlines
        gname = "nr_" + cid.replace("-", "_")
        pen = TTGlyphPen(None)
        tp = TransformPen(Cu2QuPen(pen, max_err=0.5, reverse_direction=True), (k, 0, 0, -k, 0, asc))
        for shape in pico.shapes():
            parse_path(shape.as_path().d, tp)
        glyphs[gname] = pen.glyph()
        code = 0xE100 + i
        order.append(gname)
        cmap[code] = gname
        defs[cid] = {"fontCharacter": "\\" + f"{code:04X}"}

    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({g: (upm, 0) for g in order})
    fb.setupHorizontalHeader(ascent=asc, descent=desc)
    fb.setupNameTable({"familyName": "Novaroma Product Icons", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=asc, sTypoDescender=desc, sTypoLineGap=0, usWinAscent=asc, usWinDescent=-desc)
    fb.setupPost()
    removeOverlaps(fb.font)                                # union overlapping outlines, fix winding
    fb.font.flavor = "woff"
    fb.font.save(f"{OUT}/novaroma-product-icons.woff")

    theme = {
        "fonts": [{"id": "novaroma-product", "src": [{"path": "./novaroma-product-icons.woff", "format": "woff"}],
                   "weight": "normal", "style": "normal"}],
        "iconDefinitions": defs,
    }
    with open(f"{OUT}/novaroma-product-icon-theme.json", "w") as f:
        json.dump(theme, f, indent=2)
    return len(defs)


if __name__ == "__main__":
    print(build(), "product icons")
