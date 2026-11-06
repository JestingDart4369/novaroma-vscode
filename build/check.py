"""Contrast check on the generated themes, with alpha colours composited over their real ground."""
import json, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from tokens import ratio

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def rgb(h):
    h = h.lstrip("#")
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)], a


def over(top, ground):
    (t, a), (g, _) = rgb(top), rgb(ground)
    return "#" + "".join(f"{round(t[i] * a + g[i] * (1 - a)):02x}" for i in range(3))


# (foreground key, background key or None=editor, ground for alpha background, minimum)
PAIRS = [
    ("sideBar.foreground", "sideBar.background", None, 4.5),
    ("tab.activeForeground", "tab.activeBackground", None, 4.5),
    ("tab.inactiveForeground", "tab.inactiveBackground", None, 4.5),
    ("activityBar.foreground", "activityBar.background", None, 3.0),
    ("activityBar.activeBorder", "activityBar.background", None, 3.0),
    ("list.highlightForeground", "sideBar.background", None, 3.0),
    ("gitDecoration.modifiedResourceForeground", "sideBar.background", None, 4.5),
    ("gitDecoration.untrackedResourceForeground", "sideBar.background", None, 4.5),
    ("gitDecoration.deletedResourceForeground", "sideBar.background", None, 4.5),
    ("gitDecoration.renamedResourceForeground", "sideBar.background", None, 4.5),
    ("list.activeSelectionForeground", "list.activeSelectionBackground", "sideBar.background", 4.5),
    ("list.activeSelectionForeground", "list.activeSelectionBackground", "editor.background", 4.5),
    ("list.hoverForeground", "list.hoverBackground", "sideBar.background", 4.5),
    ("statusBar.foreground", "statusBar.background", None, 4.5),
    ("activityBarBadge.foreground", "activityBarBadge.background", None, 4.5),
    ("badge.foreground", "badge.background", None, 4.5),
    ("button.foreground", "button.background", None, 4.5),
    ("titleBar.activeForeground", "titleBar.activeBackground", None, 4.5),
    ("editor.foreground", "editor.background", None, 4.5),
    ("editorLineNumber.foreground", "editor.background", None, 3.0),
    ("editorLineNumber.activeForeground", "editor.background", None, 4.5),
    ("panelTitle.activeForeground", "panel.background", None, 4.5),
]


def main():
    fails = 0
    for fn in sorted(glob.glob(f"{ROOT}/themes/*.json")):
        t = json.load(open(fn, encoding="utf-8"))
        c = t["colors"]
        bg = c["editor.background"]
        for fg_k, bg_k, ground_k, minimum in PAIRS:
            ground = c[ground_k] if ground_k else bg
            b = c[bg_k]
            if len(b) == 9:
                b = over(b, ground)
            f = c[fg_k]
            if len(f) == 9:
                f = over(f, b)
            r = ratio(f, b)
            if r < minimum:
                fails += 1
                print(f"{t['name']:34s} {fg_k} on {bg_k}{' over ' + ground_k if ground_k else ''}: {r:.2f} < {minimum}")
        for tc in t["tokenColors"]:
            fgc = tc["settings"].get("foreground")
            if fgc and ratio(fgc, bg) < 4.5:
                fails += 1
                print(f"{t['name']:34s} token {tc['name']}: {ratio(fgc, bg):.2f}")
    print("failures:", fails)


if __name__ == "__main__":
    main()
