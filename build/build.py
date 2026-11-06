"""Build the Novaroma extension: colour themes, icon theme, package.json contributions."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from themes import all_themes
import icons

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def slug(name):
    return name.lower().replace("ü", "ue").replace(" ", "-")


def main():
    os.makedirs(f"{ROOT}/themes", exist_ok=True)
    contrib, rows = [], []
    for mode, s, sname, swapped, name, data, rep, r, chrome in all_themes():
        fn = f"themes/{slug(name)}-color-theme.json"
        with open(f"{ROOT}/{fn}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        contrib.append({"label": name, "uiTheme": "vs" if mode == "light" else "vs-dark", "path": "./" + fn})
        rows.append((name, rep))
    nf, nd = icons.build(ROOT)

    pkg_path = f"{ROOT}/package.json"
    pkg = json.load(open(pkg_path, encoding="utf-8"))
    pkg["contributes"]["themes"] = contrib
    pkg["contributes"]["iconThemes"] = [{"id": "novaroma-icons", "label": "Novaroma Icons",
                                         "path": "./icons/novaroma-icon-theme.json"}]
    with open(pkg_path, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"{len(contrib)} colour themes, icon theme with {nf} file types and {nd} folder types")
    worst = {}
    for name, rep in rows:
        for k, v in rep.items():
            if k not in worst or v < worst[k][0]:
                worst[k] = (v, name)
    for k, (v, n) in worst.items():
        print(f"  lowest {k:10s} {v:5.2f}  ({n})")


if __name__ == "__main__":
    main()
