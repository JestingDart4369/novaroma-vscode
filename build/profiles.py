"""Write VS Code profile templates (.code-profile) for the Novaroma presets.

A .code-profile is a JSON object; its "settings" value is a JSON string of {"settings": "<settings.json text>"}.
Import with: Profiles: Import Profile… (or the gear menu > Profiles > Import).
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main():
    data = json.load(open(f"{ROOT}/src/presets.json", encoding="utf-8"))
    os.makedirs(f"{ROOT}/profiles", exist_ok=True)
    for p in data["presets"]:
        settings = {
            "window.autoDetectColorScheme": True,
            "workbench.colorTheme": "Novaroma Standard Light",
            "workbench.preferredLightColorTheme": "Novaroma Standard Light",
            "workbench.preferredDarkColorTheme": "Novaroma Standard Dark",
            "workbench.iconTheme": "novaroma-icons",
            "workbench.productIconTheme": "novaroma-product-icons",
            "novaroma.palette": "auto",
            "novaroma.appearance": "system",
            "novaroma.variant": "normal",
            **data["base"],
            **p["settings"],
        }
        profile = {
            "name": p["label"],
            "icon": p["icon"],
            "settings": json.dumps({"settings": json.dumps(settings, indent=4, ensure_ascii=False)}, ensure_ascii=False),
        }
        fn = f"{ROOT}/profiles/{p['label'].replace(' ', '-')}.code-profile"
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print("wrote", os.path.relpath(fn, ROOT))


if __name__ == "__main__":
    main()
