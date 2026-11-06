"""Render preview images of the themes (mock VS Code window) for the README / extension page."""
import json, os, subprocess, sys, re, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MONO = "DejaVu Sans Mono, monospace"
SANS = "Roboto, DejaVu Sans, sans-serif"

CODE = [
    [("from", "ctl"), (" dataclasses ", "var"), ("import", "ctl"), (" dataclass", "var")],
    [],
    [("@dataclass", "deco")],
    [("class", "kw"), (" ", ""), ("Service", "tydecl"), (":", "op")],
    [("    ", ""), ('"""A container in the Nova Roma homelab."""', "cmt")],
    [("    name", "prop"), (": ", "op"), ("str", "bt")],
    [("    port", "prop"), (": ", "op"), ("int", "bt"), (" = ", "op"), ("8080", "num")],
    [],
    [("    ", ""), ("def", "kw"), (" ", ""), ("url", "fndecl"), ("(", "op"), ("self", "self"), (") -> ", "op"), ("str", "bt"), (":", "op")],
    [("        ", ""), ("return", "ctl"), (' f"https://api.novaroma-homelab.uk/', "str"), ("{", "kw"), ("self", "self"), (".", "op"), ("name", "prop"), ("}", "kw"), ('"', "str")],
    [],
    [("SEASONS", "const"), (" = ", "op"), ("[", "op"), ('"Frühling"', "str"), (", ", "op"), ('"Sommer"', "str"), (", ", "op"), ('"Herbst"', "str"), (", ", "op"), ('"Winter"', "str"), ("]", "op")],
    [("for", "ctl"), (" i", "var"), (", ", "op"), ("season ", "var"), ("in", "ctl"), (" ", ""), ("enumerate", "fn"), ("(", "op"), ("SEASONS", "const"), (", ", "op"), ("start", "param"), ("=", "op"), ("1", "num"), ("):", "op")],
    [("    ", ""), ("print", "fn"), ("(", "op"), ("i", "var"), (", ", "op"), ("season", "var"), (", ", "op"), ("True", "num"), (")", "op"), ("  # ready", "cmt")],
]

TREE = [  # (depth, kind, name, icon key, git)
    (0, "root", "NOVAROMA-HOMELAB", "_root_open", None),
    (1, "dir", ".vscode", "folder_vscode", None),
    (1, "diro", "src", "folder_src_open", None),
    (2, "file", "service.py", "file_python", "M"),
    (2, "file", "api.cs", "file_csharp", None),
    (2, "file", "schema.sql", "file_sql", "U"),
    (1, "dir", "docs", "folder_docs", None),
    (1, "dir", "tests", "folder_tests", None),
    (1, "file", "compose.yaml", "file_docker", None),
    (1, "file", ".env", "file_env", None),
    (1, "file", "README.md", "file_readme", None),
    (1, "file", "pyproject.toml", "file_package", None),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def token_style(theme):
    """Resolve our roles to colours/styles straight from the generated theme JSON."""
    tc = {t["name"]: t["settings"] for t in theme["tokenColors"]}
    c = theme["colors"]
    m = {
        "kw": tc["Keywords & storage"], "ctl": tc["Control flow"], "op": tc["Operators & punctuation"],
        "str": tc["Strings"], "num": tc["Numbers & constants"], "const": tc["Numbers & constants"],
        "cmt": tc["Comment"], "fndecl": tc["Function declarations"], "fn": tc["Function calls"],
        "tydecl": tc["Types & classes"], "bt": tc["Built-in types"], "var": tc["Variables"],
        "prop": tc["Properties & keys"], "param": tc["Parameters"], "self": tc["Self / this"],
        "deco": tc["Decorators & attributes"], "": {"foreground": c["editor.foreground"]},
    }
    return m


def icon_svg(key, variant):
    with open(f"{ROOT}/icons/{variant}/{key}.svg") as f:
        s = f.read()
    return re.sub(r"^<svg[^>]*>|</svg>$", "", s)


def window_svg(theme, W=760, H=430):
    c = theme["colors"]
    dark = theme["type"] == "dark"
    iv = "dark" if dark else "light"
    st = token_style(theme)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<defs><clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs><g clip-path="url(#win)">')
    out.append(f'<rect width="{W}" height="{H}" fill="{c["editor.background"]}"/>')
    tb, ab, sb, tabs, stb = 30, 44, 200, 34, 24
    # title bar
    out.append(f'<rect width="{W}" height="{tb}" fill="{c["titleBar.activeBackground"]}"/>')
    for i, col in enumerate(["#d02267", "#e8a63d", "#4f6b3e"]):
        out.append(f'<circle cx="{16 + i * 18}" cy="15" r="5.5" fill="{col}" opacity="0.85"/>')
    out.append(f'<rect x="{W/2-120}" y="6" width="240" height="18" rx="9" fill="{c["commandCenter.background"][:7]}" '
               f'fill-opacity="{int(c["commandCenter.background"][7:9] or "ff", 16)/255:.2f}" stroke="{c["commandCenter.border"][:7]}" stroke-opacity="0.4"/>')
    out.append(f'<text x="{W/2}" y="19" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{c["titleBar.activeForeground"]}">novaroma-homelab</text>')
    # activity bar
    out.append(f'<rect y="{tb}" width="{ab}" height="{H-tb-stb}" fill="{c["activityBar.background"]}"/>')
    for i in range(4):
        y = tb + 14 + i * 42
        colr = c["activityBar.foreground"] if i == 0 else c["activityBar.inactiveForeground"][:7]
        op = 1 if i == 0 else 0.6
        out.append(f'<rect x="13" y="{y}" width="18" height="18" rx="4" fill="none" stroke="{colr}" stroke-opacity="{op}" stroke-width="2"/>')
        if i == 0:
            out.append(f'<rect x="0" y="{y-6}" width="2.5" height="30" fill="{c["activityBar.activeBorder"]}"/>')
    out.append(f'<circle cx="31" cy="{tb+14+42+3}" r="6" fill="{c["activityBarBadge.background"]}"/>'
               f'<text x="31" y="{tb+14+42+6.5}" text-anchor="middle" font-family="{SANS}" font-size="8" font-weight="700" fill="{c["activityBarBadge.foreground"]}">3</text>')
    # side bar
    out.append(f'<rect x="{ab}" y="{tb}" width="{sb}" height="{H-tb-stb}" fill="{c["sideBar.background"]}"/>')
    out.append(f'<text x="{ab+14}" y="{tb+20}" font-family="{SANS}" font-size="10" font-weight="700" letter-spacing="0.8" fill="{c["sideBarTitle.foreground"]}">EXPLORER</text>')
    y = tb + 34
    for depth, kind, name, key, git in TREE:
        x = ab + 10 + depth * 12
        if name == "service.py":
            sel = c["list.activeSelectionBackground"]
            out.append(f'<rect x="{ab}" y="{y-2}" width="{sb}" height="20" fill="{sel[:7]}" fill-opacity="{(int(sel[7:9],16)/255 if len(sel)==9 else 1):.2f}"/>')
            fg = c["list.activeSelectionForeground"]
        else:
            fg = c["sideBar.foreground"]
        if git == "M" and name != "service.py":
            fg = c["gitDecoration.modifiedResourceForeground"]
        if git == "U":
            fg = c["gitDecoration.untrackedResourceForeground"]
        arrow = "" if kind == "file" else ("▾" if kind in ("diro", "root") else "▸")
        if arrow:
            out.append(f'<text x="{x}" y="{y+12}" font-family="{SANS}" font-size="9" fill="{c["sideBar.foreground"]}">{arrow}</text>')
        ix = x + 10
        out.append(f'<svg x="{ix}" y="{y}" width="16" height="16" viewBox="0 0 32 32">{icon_svg(key, iv)}</svg>')
        weight = "700" if kind == "root" else "400"
        size = "10" if kind == "root" else "11.5"
        out.append(f'<text x="{ix+21}" y="{y+12}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" fill="{fg}">{esc(name)}</text>')
        if git:
            out.append(f'<text x="{ab+sb-14}" y="{y+12}" text-anchor="end" font-family="{SANS}" font-size="10" fill="{fg}">{git}</text>')
        y += 22
    # tabs
    ex = ab + sb
    out.append(f'<rect x="{ex}" y="{tb}" width="{W-ex}" height="{tabs}" fill="{c["editorGroupHeader.tabsBackground"]}"/>')
    tab_defs = [("service.py", "file_python", True), ("api.cs", "file_csharp", False), ("README.md", "file_readme", False)]
    tx = ex
    for name, key, active in tab_defs:
        w = 116
        if active:
            out.append(f'<rect x="{tx}" y="{tb}" width="{w}" height="{tabs}" fill="{c["tab.activeBackground"]}"/>')
            out.append(f'<rect x="{tx}" y="{tb}" width="{w}" height="2" fill="{c["tab.activeBorderTop"]}"/>')
            fg = c["tab.activeForeground"]
        else:
            fg = c["tab.inactiveForeground"]
        f, op = fg[:7], (int(fg[7:9], 16) / 255 if len(fg) == 9 else 1)
        out.append(f'<svg x="{tx+12}" y="{tb+9}" width="16" height="16" viewBox="0 0 32 32">{icon_svg(key, iv)}</svg>')
        out.append(f'<text x="{tx+33}" y="{tb+21}" font-family="{SANS}" font-size="11.5" fill="{f}" fill-opacity="{op:.2f}">{name}</text>')
        tx += w
    # editor
    ey = tb + tabs + 10
    lh = 19
    ln_x = ex + 30
    cx0 = ex + 46
    cur = 8
    for i, line in enumerate(CODE):
        yy = ey + i * lh
        if i == cur:
            lhc = c["editor.lineHighlightBackground"]
            out.append(f'<rect x="{ex}" y="{yy}" width="{W-ex}" height="{lh}" fill="{lhc[:7]}" fill-opacity="{int(lhc[7:9],16)/255:.2f}"/>')
        lnc = c["editorLineNumber.activeForeground"] if i == cur else c["editorLineNumber.foreground"]
        out.append(f'<text x="{ln_x}" y="{yy+14}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{lnc[:7]}">{i+1}</text>')
        parts = []
        for text, role in line:
            s = st[role]
            attrs = f'fill="{s.get("foreground", c["editor.foreground"])}"'
            fs = s.get("fontStyle", "")
            if "bold" in fs:
                attrs += ' font-weight="700"'
            if "italic" in fs:
                attrs += ' font-style="italic"'
            parts.append(f'<tspan {attrs}>{esc(text)}</tspan>')
        out.append(f'<text x="{cx0}" y="{yy+14}" font-family="{MONO}" font-size="12" xml:space="preserve">{"".join(parts)}</text>')
    # selection + cursor on line 9 ("url")
    sy = ey + cur * lh
    sel = c["editor.selectionBackground"]
    out.append(f'<rect x="{cx0 + 8*7.22}" y="{sy+1}" width="{3*7.22}" height="{lh-2}" fill="{sel[:7]}" fill-opacity="{int(sel[7:9],16)/255:.2f}"/>')
    out.append(f'<rect x="{cx0 + 11*7.22}" y="{sy+2}" width="2" height="{lh-4}" fill="{c["editorCursor.foreground"]}"/>')
    # status bar
    out.append(f'<rect y="{H-stb}" width="{W}" height="{stb}" fill="{c["statusBar.background"]}"/>')
    sf = c["statusBar.foreground"]
    out.append(f'<text x="12" y="{H-8}" font-family="{SANS}" font-size="11" fill="{sf}">⑂ main   ✓ 0  ⚠ 0</text>')
    out.append(f'<text x="{W-12}" y="{H-8}" text-anchor="end" font-family="{SANS}" font-size="11" fill="{sf}">'
               f'{esc(theme["name"].replace("Novaroma ", ""))}   Python   UTF-8</text>')
    out.append("</g>")
    out.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#00000022"/>')
    out.append("</svg>")
    return "\n".join(o for o in out if o)


def render(svg_text, out_png, width):
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
        f.write(svg_text)
        p = f.name
    subprocess.run(["rsvg-convert", "-w", str(width), p, "-o", out_png], check=True)
    os.unlink(p)


def main():
    out = f"{ROOT}/images"
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    themes = {}
    for fn in sorted(os.listdir(f"{ROOT}/themes")):
        t = json.load(open(f"{ROOT}/themes/{fn}", encoding="utf-8"))
        themes[t["name"]] = t
    order = ["Standard", "Frühling", "Sommer", "Herbst", "Winter"]
    variants = ["Light", "Light Swapped", "Dark", "Dark Swapped"]
    shots = {}
    for name, t in themes.items():
        p = f"{tmp}/{name}.png"
        render(window_svg(t), p, 760)
        shots[name] = p

    # hero: Herbst Light + Herbst Dark
    a, b = Image.open(shots["Novaroma Herbst Light"]), Image.open(shots["Novaroma Herbst Dark"])
    hero = Image.new("RGB", (a.width * 2 + 72, a.height + 48), "#eee3c9")
    hero.paste(a, (24, 24), a.convert("RGBA")); hero.paste(b, (a.width + 48, 24), b.convert("RGBA"))
    hero.save(f"{out}/hero.png", optimize=True)

    # one image per season: 4 variants in a 2x2 grid with labels
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    for sname in order:
        cell_w, cell_h = 760, 430
        g = Image.new("RGB", (cell_w * 2 + 72, (cell_h + 40) * 2 + 40), "#eee3c9")
        d = ImageDraw.Draw(g)
        for i, v in enumerate(variants):
            im = Image.open(shots[f"Novaroma {sname} {v}"]).convert("RGBA")
            x, y = 24 + (i % 2) * (cell_w + 24), 24 + (i // 2) * (cell_h + 40)
            d.text((x, y), v, fill="#5e282c", font=font)
            g.paste(im, (x, y + 32), im)
        slug = sname.lower().replace("ü", "ue")
        g = g.resize((g.width // 2 * 2 * 3 // 4, g.height * 3 // 4), Image.LANCZOS)
        g.save(f"{out}/season-{slug}.png", optimize=True)

    # icon sheet
    keys = ["_root_open", "_folder", "_folder_open", "folder_src", "folder_git", "folder_vscode", "folder_docs",
            "folder_tests", "folder_assets", "folder_scripts", "folder_build", "folder_data", "folder_school",
            "file_python", "file_notebook", "file_csharp", "file_cpp", "file_js", "file_ts", "file_html", "file_css",
            "file_json", "file_yaml", "file_toml", "file_sql", "file_csv", "file_markdown", "file_readme",
            "file_license", "file_text", "file_pdf", "file_word", "file_image", "file_svg", "file_audio",
            "file_archive", "file_shell", "file_docker", "file_git", "file_env", "file_lock", "file_package"]
    per, size, pad = 14, 40, 14
    rows = (len(keys) + per - 1) // per
    grounds = [("Light", "light", "#eee3c9"), ("Light Swapped", "light", "#5e282c"),
               ("Dark", "dark", "#6e3338"), ("Dark Swapped", "dark", "#eee3c9")]
    W = per * (size + pad) + pad
    band = rows * (size + pad) + pad
    sheet = Image.new("RGB", (W, band * len(grounds)), "#fff")
    for gi, (_, iv, gcol) in enumerate(grounds):
        ImageDraw.Draw(sheet).rectangle([0, gi * band, W, (gi + 1) * band], fill=gcol)
        for k, key in enumerate(keys):
            p = f"{tmp}/{iv}{key}.png"
            subprocess.run(["rsvg-convert", "-w", str(size), f"{ROOT}/icons/{iv}/{key}.svg", "-o", p], check=True)
            ic = Image.open(p).convert("RGBA")
            sheet.paste(ic, (pad + (k % per) * (size + pad), gi * band + pad + (k // per) * (size + pad)), ic)
    sheet.save(f"{out}/icons.png", optimize=True)
    print("previews written to", out)


if __name__ == "__main__":
    main()
