"""Novaroma file icon theme: outlined documents and folders in the Nova Roma line style.

Every icon has a filled ground (cream in light, dark burgundy in dark) inside a 2px outline,
so it stays visible on cream, burgundy and dark chrome alike.
"""
import json, os
from tokens import INK_LIGHT, INK_DARK

V = {
    "light": {"fill": "#eee3c9", "line": "#5e282c", "ink": INK_LIGHT},
    "dark": {"fill": "#6e3338", "line": "#eee3c9", "ink": INK_DARK},
}
FONT = "Roboto, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

DOC = ("M8 3H19L26 10V27Q26 29 24 29H8Q6 29 6 27V5Q6 3 8 3Z", "M19 3.5V8Q19 10 21 10H25.5")
FOLDER = "M3.5 9Q3.5 7 5.5 7H11.5L14.5 10H26.5Q28.5 10 28.5 12V24Q28.5 26 26.5 26H5.5Q3.5 26 3.5 24Z"
FOLDER_OPEN_BACK = "M3.5 25V9Q3.5 7 5.5 7H11.5L14.5 10H25.5Q27.5 10 27.5 12V14H9.4Q7.9 14 7.4 15.4L3.8 25.2"
FOLDER_OPEN_FRONT = "M3.8 25.2L7.4 15.4Q7.9 14 9.4 14H28.4Q30.2 14 29.6 15.7L26.5 24.6Q26 26 24.5 26H5Q3.4 26 3.8 25.2Z"


# ---- glyphs, drawn in a 12x12 box --------------------------------------------------------
def g_lines(c):      return f'<path d="M2 3H10M2 6H10M2 9H7" stroke="{c}" stroke-width="1.6" stroke-linecap="round" fill="none"/>'
def g_code(c):       return f'<path d="M4.2 2.5L1 6L4.2 9.5M7.8 2.5L11 6L7.8 9.5" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
def g_braces(c):     return (f'<path d="M4.5 1.5Q2.6 1.5 2.6 3.4V4.8Q2.6 6 1.4 6Q2.6 6 2.6 7.2V8.6Q2.6 10.5 4.5 10.5'
                             f'M7.5 1.5Q9.4 1.5 9.4 3.4V4.8Q9.4 6 10.6 6Q9.4 6 9.4 7.2V8.6Q9.4 10.5 7.5 10.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none"/>')
def g_hash(c):       return f'<path d="M4.6 1.5L3.4 10.5M8.6 1.5L7.4 10.5M1.5 4.2H10.8M1.2 7.8H10.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none"/>'
def g_db(c):         return (f'<ellipse cx="6" cy="2.8" rx="4.3" ry="1.6" stroke="{c}" stroke-width="1.4" fill="none"/>'
                             f'<path d="M1.7 2.8V9.2Q1.7 10.8 6 10.8Q10.3 10.8 10.3 9.2V2.8M1.7 6Q1.7 7.6 6 7.6Q10.3 7.6 10.3 6" stroke="{c}" stroke-width="1.4" fill="none"/>')
def g_table(c):      return f'<rect x="1.2" y="1.8" width="9.6" height="8.4" rx="1.4" stroke="{c}" stroke-width="1.4" fill="none"/><path d="M1.2 4.9H10.8M1.2 7.5H10.8M5 1.8V10.2" stroke="{c}" stroke-width="1.2" fill="none"/>'
def g_image(c):      return f'<rect x="1" y="1.8" width="10" height="8.4" rx="1.4" stroke="{c}" stroke-width="1.4" fill="none"/><path d="M1.6 9.4L4.6 6L6.8 8.2L8.2 6.8L10.4 9.2" stroke="{c}" stroke-width="1.3" stroke-linejoin="round" fill="none"/><circle cx="8.2" cy="4.3" r="1" fill="{c}"/>'
def g_play(c):       return f'<path d="M3.2 1.8L10 6L3.2 10.2Z" stroke="{c}" stroke-width="1.5" stroke-linejoin="round" fill="none"/>'
def g_note(c):       return f'<path d="M4.4 9.2V2.2L10 1.2V8.2" stroke="{c}" stroke-width="1.4" fill="none"/><circle cx="3" cy="9.3" r="1.6" stroke="{c}" stroke-width="1.3" fill="none"/><circle cx="8.6" cy="8.3" r="1.6" stroke="{c}" stroke-width="1.3" fill="none"/>'
def g_zip(c):        return f'<path d="M6 1V11M4.4 2.5H6M6 4H7.6M4.4 5.5H6M6 7H7.6" stroke="{c}" stroke-width="1.3" stroke-linecap="round" fill="none"/><rect x="4.3" y="8" width="3.4" height="3" rx="0.8" stroke="{c}" stroke-width="1.3" fill="none"/>'
def g_term(c):       return f'<path d="M1.8 3L5 6L1.8 9M6.6 9.5H10.4" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
def g_branch(c):     return f'<circle cx="3.2" cy="2.6" r="1.5" stroke="{c}" stroke-width="1.3" fill="none"/><circle cx="3.2" cy="9.4" r="1.5" stroke="{c}" stroke-width="1.3" fill="none"/><circle cx="8.8" cy="4.2" r="1.5" stroke="{c}" stroke-width="1.3" fill="none"/><path d="M3.2 4.1V7.9M8.8 5.7Q8.8 7.4 6.2 7.6Q3.6 7.8 3.4 7.9" stroke="{c}" stroke-width="1.3" fill="none"/>'
def g_key(c):        return f'<circle cx="3.8" cy="6" r="2.4" stroke="{c}" stroke-width="1.4" fill="none"/><path d="M6.2 6H11M9.4 6V8.2M11 6V7.6" stroke="{c}" stroke-width="1.4" stroke-linecap="round" fill="none"/>'
def g_lock(c):       return f'<rect x="2" y="5.2" width="8" height="5.8" rx="1.3" stroke="{c}" stroke-width="1.4" fill="none"/><path d="M3.9 5.2V3.6Q3.9 1.2 6 1.2Q8.1 1.2 8.1 3.6V5.2" stroke="{c}" stroke-width="1.4" fill="none"/>'
def g_gear(c):
    import math
    pts = []
    for i in range(16):
        a = math.pi * 2 * i / 16
        rr = 5.2 if i % 2 == 0 else 3.9
        pts.append(f"{6 + rr * math.cos(a):.2f} {6 + rr * math.sin(a):.2f}")
    return f'<path d="M{"L".join(pts)}Z" stroke="{c}" stroke-width="1.2" stroke-linejoin="round" fill="none"/><circle cx="6" cy="6" r="1.6" stroke="{c}" stroke-width="1.3" fill="none"/>'
def g_box(c):        return f'<path d="M6 1.2L10.6 3.6V8.4L6 10.8L1.4 8.4V3.6Z M1.4 3.6L6 6L10.6 3.6M6 6V10.8" stroke="{c}" stroke-width="1.3" stroke-linejoin="round" fill="none"/>'
def g_check(c):      return f'<path d="M1.8 6.4L4.6 9.2L10.2 2.8" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
def g_info(c):       return f'<circle cx="6" cy="6" r="5" stroke="{c}" stroke-width="1.4" fill="none"/><path d="M6 5.4V9" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/><circle cx="6" cy="3.3" r="0.9" fill="{c}"/>'
def g_law(c):        return f'<path d="M6 1.4V10.6M3 10.6H9M2 3.2H10M2 3.2L0.8 7H3.2ZM10 3.2L8.8 7H11.2Z" stroke="{c}" stroke-width="1.2" stroke-linejoin="round" stroke-linecap="round" fill="none"/>'
def g_arrow(c):      return f'<path d="M6 10.5V2M2.6 5.2L6 1.8L9.4 5.2M1.5 10.5H10.5" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
def g_globe(c):      return f'<circle cx="6" cy="6" r="4.8" stroke="{c}" stroke-width="1.3" fill="none"/><path d="M1.2 6H10.8M6 1.2Q3.6 6 6 10.8Q8.4 6 6 1.2" stroke="{c}" stroke-width="1.2" fill="none"/>'
def g_star(c):       return f'<path d="M6 1.2L7.4 4.4L10.8 4.7L8.2 7L9 10.4L6 8.6L3 10.4L3.8 7L1.2 4.7L4.6 4.4Z" stroke="{c}" stroke-width="1.2" stroke-linejoin="round" fill="none"/>'
def g_pen(c):        return f'<path d="M2 10L2.6 7.6L8.4 1.8L10.2 3.6L4.4 9.4Z M7.4 2.8L9.2 4.6" stroke="{c}" stroke-width="1.3" stroke-linejoin="round" fill="none"/>'
def g_none(c):       return ""


def label(text, c, size):
    return (f'<text x="16" y="{size}" text-anchor="middle" font-family="{FONT}" font-weight="700" '
            f'font-size="{8.6 if len(text) <= 2 else 7.2 if len(text) == 3 else 6.2}" letter-spacing="-0.2" fill="{c}">{text}</text>')


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">{body}</svg>'


def doc_icon(v, glyph=None, color="main", text=None):
    P = V[v]
    c = P["ink"][color]
    body = (f'<path d="{DOC[0]}" fill="{P["fill"]}" stroke="{P["line"]}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="{DOC[1]}" fill="none" stroke="{P["line"]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    if text:
        body += label(text, c, 23.6)
    elif glyph:
        body += f'<g transform="translate(10 14) scale(1)">{glyph(c)}</g>'
    return svg(body)


def folder_icon(v, glyph=None, color="main", open_=False, root=False):
    P = V[v]
    c = P["ink"][color]
    lw = "2.4" if root else "2"
    if not open_:
        body = f'<path d="{FOLDER}" fill="{P["fill"]}" stroke="{P["line"]}" stroke-width="{lw}" stroke-linejoin="round"/>'
        gx, gy, sc = 10.5, 12.6, 0.92
    else:
        body = (f'<path d="{FOLDER_OPEN_BACK}Z" fill="{P["fill"]}" fill-opacity="0.55" stroke="{P["line"]}" stroke-width="{lw}" stroke-linejoin="round" stroke-linecap="round"/>'
                f'<path d="{FOLDER_OPEN_FRONT}" fill="{P["fill"]}" stroke="{P["line"]}" stroke-width="{lw}" stroke-linejoin="round"/>')
        gx, gy, sc = 11.6, 15.2, 0.8
    if root:
        # a single season dot marks the workspace root
        body += f'<circle cx="{25 if not open_ else 25.6}" cy="{8.6 if not open_ else 9}" r="2.6" fill="{P["ink"]["olive"]}" stroke="{P["line"]}" stroke-width="1.4"/>'
    if glyph:
        body += f'<g transform="translate({gx} {gy}) scale({sc})">{glyph(c)}</g>'
    return svg(body)


# ---- file types ----------------------------------------------------------------------------
# id: (glyph, colour, label, extensions, file names, language ids)
FILES = {
    "python":   (None, "blue", "Py", ["py", "pyw", "pyi", "pyc"], [], ["python"]),
    "notebook": (None, "gold", "Nb", ["ipynb"], [], ["jupyter"]),
    "csharp":   (None, "pink", "C#", ["cs", "csx"], [], ["csharp"]),
    "dotnet":   (g_gear, "pink", None, ["csproj", "sln", "props", "targets", "slnx"], [], []),
    "cpp":      (None, "amber", "C++", ["cpp", "cc", "cxx", "hpp", "hh", "hxx", "ino"], [], ["cpp"]),
    "c":        (None, "amber", "C", ["c", "h"], [], ["c"]),
    "java":     (None, "ember", "Jv", ["java", "jar", "class"], [], ["java"]),
    "js":       (None, "gold", "JS", ["js", "mjs", "cjs", "jsx"], [], ["javascript", "javascriptreact"]),
    "ts":       (None, "blue", "TS", ["ts", "mts", "cts", "tsx"], [], ["typescript", "typescriptreact"]),
    "dts":      (None, "slate", "D.TS", ["d.ts"], [], []),
    "html":     (g_code, "ember", None, ["html", "htm", "xhtml", "jinja", "j2", "vue", "svelte"], [], ["html", "jinja"]),
    "css":      (g_hash, "blue", None, ["css", "scss", "sass", "less"], [], ["css", "scss", "less"]),
    "json":     (g_braces, "gold", None, ["json", "jsonc", "json5", "webmanifest"], [], ["json", "jsonc"]),
    "yaml":     (g_lines, "green", "YML", ["yml", "yaml"], [], ["yaml"]),
    "toml":     (g_gear, "muted", None, ["toml", "ini", "cfg", "conf", "properties", "editorconfig"], [".editorconfig"], ["toml", "ini", "properties"]),
    "xml":      (g_code, "slate", None, ["xml", "xsd", "xsl", "plist", "resx", "xaml"], [], ["xml"]),
    "sql":      (g_db, "amber", None, ["sql", "db", "sqlite", "sqlite3", "ddl", "dml", "mdb", "accdb"], [], ["sql"]),
    "csv":      (g_table, "green", None, ["csv", "tsv", "xlsx", "xls", "xlsm", "ods", "numbers"], [], ["csv"]),
    "markdown": (None, "main", "MD", ["md", "markdown", "mdx", "rmd"], [], ["markdown"]),
    "readme":   (g_info, "main", None, [], ["readme.md", "readme", "readme.txt", "readme.rst"], []),
    "license":  (g_law, "main", None, ["license"], ["license", "license.md", "license.txt", "copying"], []),
    "changelog": (g_star, "main", None, [], ["changelog.md", "changelog", "history.md"], []),
    "text":     (g_lines, "muted", None, ["txt", "log", "rst", "rtf", "out"], [], ["plaintext", "log"]),
    "pdf":      (None, "pink", "PDF", ["pdf"], [], []),
    "word":     (None, "blue", "DOC", ["doc", "docx", "dotx", "odt", "pages"], [], []),
    "slides":   (None, "ember", "PPT", ["ppt", "pptx", "potx", "odp", "key"], [], []),
    "image":    (g_image, "green", None, ["png", "jpg", "jpeg", "gif", "webp", "bmp", "ico", "tif", "tiff", "heic", "avif"], [], []),
    "svg":      (g_pen, "gold", None, ["svg"], [], []),
    "font":     (None, "main", "Aa", ["ttf", "otf", "woff", "woff2"], [], []),
    "video":    (g_play, "pink", None, ["mp4", "mov", "mkv", "webm", "avi"], [], []),
    "audio":    (g_note, "pink", None, ["mp3", "wav", "flac", "ogg", "m4a", "mid", "midi", "musicxml", "mscz"], [], []),
    "archive":  (g_zip, "muted", None, ["zip", "tar", "gz", "tgz", "7z", "rar", "bz2", "xz", "vsix", "whl"], [], []),
    "shell":    (g_term, "green", None, ["sh", "bash", "zsh", "fish", "ps1", "psm1", "bat", "cmd"], [], ["shellscript", "powershell", "bat"]),
    "docker":   (g_box, "blue", None, ["dockerfile"], ["dockerfile", "containerfile", "docker-compose.yml", "docker-compose.yaml",
                                                      "compose.yml", "compose.yaml", ".dockerignore"], ["dockerfile", "dockercompose"]),
    "git":      (g_branch, "ember", None, [], [".gitignore", ".gitattributes", ".gitmodules", ".gitkeep", ".git-blame-ignore-revs"], ["ignore"]),
    "env":      (g_key, "gold", None, ["env", "pem", "key", "crt", "cer", "pub", "gpg", "asc"], [".env", ".env.local", ".env.example", ".envrc"], ["dotenv"]),
    "lock":     (g_lock, "muted", None, ["lock"], ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "uv.lock",
                                                    "pipfile.lock", "cargo.lock", "composer.lock"], []),
    "package":  (g_box, "olive", None, [], ["package.json", "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg",
                                             "pipfile", "cargo.toml", "go.mod", "gemfile"], ["pip-requirements"]),
    "config":   (g_gear, "main", None, [], ["tsconfig.json", "jsconfig.json", ".prettierrc", ".eslintrc.json", "eslint.config.js",
                                             "vite.config.ts", "vite.config.js", "makefile", ".npmrc", ".flake8", "tox.ini",
                                             "settings.json", "launch.json", "tasks.json", "extensions.json"], ["makefile"]),
    "web":      (g_globe, "blue", None, ["url", "webloc"], ["robots.txt", "sitemap.xml", "cname", "nginx.conf", "caddyfile"], []),
    "obsidian": (g_pen, "rose", None, ["canvas", "base"], [], []),
    "go":       (None, "slate", "Go", ["go"], [], ["go"]),
    "rust":     (None, "ember", "Rs", ["rs"], [], ["rust"]),
    "php":      (None, "rose", "PHP", ["php"], [], ["php"]),
    "lua":      (None, "blue", "Lua", ["lua"], [], ["lua"]),
}

# folder id: (glyph, colour, folder names)
FOLDERS = {
    "src":     (g_code, "blue", ["src", "source", "lib", "app", "core", "pkg"]),
    "git":     (g_branch, "ember", [".git", ".github", ".gitlab", ".gitea"]),
    "vscode":  (g_gear, "main", [".vscode", ".idea", ".obsidian", ".config", "config", "configs", "settings"]),
    "modules": (g_box, "muted", ["node_modules", "vendor", "packages", "site-packages", "bower_components"]),
    "venv":    (g_box, "blue", [".venv", "venv", "env", ".env", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"]),
    "docs":    (g_lines, "main", ["docs", "doc", "documentation", "notes", "wiki", "notizen", "dokumentation"]),
    "tests":   (g_check, "green", ["test", "tests", "__tests__", "spec", "specs", "e2e"]),
    "assets":  (g_image, "green", ["assets", "images", "img", "media", "static", "public", "icons", "bilder", "fonts"]),
    "scripts": (g_term, "green", ["scripts", "script", "bin", "tools", "cli", "shell"]),
    "build":   (g_arrow, "amber", ["dist", "build", "out", "output", "release", "target", ".next", "export"]),
    "data":    (g_db, "amber", ["data", "db", "database", "datasets", "sql", "migrations", "seeds"]),
    "secrets": (g_lock, "gold", ["secrets", "certs", "keys", ".ssh", "ssl"]),
    "docker":  (g_box, "blue", ["docker", ".docker", "containers", "compose", "deploy", "infra", "k8s"]),
    "web":     (g_globe, "blue", ["web", "www", "site", "html", "pages", "templates", "views", "components"]),
    "school":  (g_star, "olive", ["schule", "school", "ims", "module", "modules", "kurse", "aufgaben"]),
}


def build(out):
    defs, ext, names, langs, fnames, fnames_open = {}, {}, {}, {}, {}, {}
    light = {"fileExtensions": {}, "fileNames": {}, "languageIds": {}, "folderNames": {}, "folderNamesExpanded": {}}
    for v in ("dark", "light"):
        os.makedirs(f"{out}/icons/{v}", exist_ok=True)

    def add(key, maker):
        for v in ("dark", "light"):
            path = f"icons/{v}/{key}.svg"
            with open(f"{out}/{path}", "w") as f:
                f.write(maker(v))
            defs[key + ("" if v == "dark" else "_l")] = {"iconPath": "./" + path}

    add("_file", lambda v: doc_icon(v, g_lines, "muted"))
    add("_folder", lambda v: folder_icon(v))
    add("_folder_open", lambda v: folder_icon(v, open_=True))
    add("_root", lambda v: folder_icon(v, root=True))
    add("_root_open", lambda v: folder_icon(v, open_=True, root=True))

    for fid, (glyph, col, txt, exts, fns, lids) in FILES.items():
        key = "file_" + fid
        add(key, lambda v, g=glyph, c=col, t=txt: doc_icon(v, g, c, t))
        for e in exts:
            ext[e] = key; light["fileExtensions"][e] = key + "_l"
        for n in fns:
            names[n] = key; light["fileNames"][n] = key + "_l"
        for l in lids:
            langs[l] = key; light["languageIds"][l] = key + "_l"

    for did, (glyph, col, dirs) in FOLDERS.items():
        k, ko = "folder_" + did, "folder_" + did + "_open"
        add(k, lambda v, g=glyph, c=col: folder_icon(v, g, c))
        add(ko, lambda v, g=glyph, c=col: folder_icon(v, g, c, open_=True))
        for d in dirs:
            fnames[d] = k; fnames_open[d] = ko
            light["folderNames"][d] = k + "_l"; light["folderNamesExpanded"][d] = ko + "_l"

    theme = {
        "iconDefinitions": defs,
        "file": "_file", "folder": "_folder", "folderExpanded": "_folder_open",
        "rootFolder": "_root", "rootFolderExpanded": "_root_open",
        "fileExtensions": ext, "fileNames": names, "languageIds": langs,
        "folderNames": fnames, "folderNamesExpanded": fnames_open,
        "light": {"file": "_file_l", "folder": "_folder_l", "folderExpanded": "_folder_open_l",
                  "rootFolder": "_root_l", "rootFolderExpanded": "_root_open_l", **light},
        "hidesExplorerArrows": False,
    }
    with open(f"{out}/icons/novaroma-icon-theme.json", "w") as f:
        json.dump(theme, f, indent=2)
    return len(FILES), len(FOLDERS)
