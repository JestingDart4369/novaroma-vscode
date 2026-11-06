"""Nova Roma design tokens used by the Novaroma VS Code extension (from the Nova Roma design system)."""

SEASONS = [("standard", "Standard"), ("fruehling", "Frühling"), ("sommer", "Sommer"),
           ("herbst", "Herbst"), ("winter", "Winter")]

# Light: tokens bg / muted / season / season-ink per season, brand core shared.
LIGHT = {
    "bg": {"standard": "#f6f7fb", "fruehling": "#fbf3f6", "sommer": "#fdf8ea", "herbst": "#f8f0e6", "winter": "#f1f5fa"},
    "muted": {"standard": "#7e6e56", "fruehling": "#8e6271", "sommer": "#836e42", "herbst": "#85664c", "winter": "#5c7084"},
    "season": {"standard": "#eee3c9", "fruehling": "#f5c2d6", "sommer": "#ffd66b", "herbst": "#e8a63d", "winter": "#bfdcf5"},
    "season_ink": {"standard": "#886c2b", "fruehling": "#d02267", "sommer": "#916900", "herbst": "#946212", "winter": "#1d71b9"},
    "main": "#5e282c", "text": "#190607", "accent": "#eee3c9", "pressed": "#451d20",
    "dis_fill": "#ebe8e2", "dis_border": "#cfc8bc", "dis_ink": "#857c6e",
}

# Dark: "Seasons in dark" table from the design system README.
DARK = {
    "bg": {"standard": "#1b0e0f", "fruehling": "#1f0f14", "sommer": "#1d1608", "herbst": "#1d1109", "winter": "#0e1620"},
    "muted": {"standard": "#b7a68b", "fruehling": "#cfa6b6", "sommer": "#cdb67e", "herbst": "#cfa883", "winter": "#9db6cc"},
    "season": {"standard": "#6e3338", "fruehling": "#6b2c43", "sommer": "#5a4510", "herbst": "#6a4513", "winter": "#25405c"},
    "season_ink": {"standard": "#eee3c9", "fruehling": "#f29bbb", "sommer": "#f5cf5f", "herbst": "#eeb25a", "winter": "#8dc2ee"},
    "main": "#eee3c9", "text": "#fff8ea", "accent": "#6e3338", "pressed": "#cfc2a3",
    "dis_fill": "#2a2020", "dis_border": "#3e3333", "dis_ink": "#8a7f73",
}

# Named inks for syntax, terminal and icons. All are system tokens:
# season-inks of the five seasons, sv-forest / sv-ember / sv-amber, and Svenja particle colours.
INK_LIGHT = {"pink": "#d02267", "gold": "#916900", "amber": "#946212", "blue": "#1d71b9", "olive": "#886c2b",
             "green": "#4f6b3e", "ember": "#c05a2e", "main": "#5e282c", "text": "#190607", "muted": "#7e6e56",
             "slate": "#5c7084", "rose": "#8e6271"}
INK_DARK = {"pink": "#f29bbb", "gold": "#f5cf5f", "amber": "#eeb25a", "blue": "#8dc2ee", "olive": "#e8a63d",
            "green": "#c8e6a0", "ember": "#f7a8c4", "main": "#eee3c9", "text": "#fff8ea", "muted": "#b7a68b",
            "slate": "#9db6cc", "rose": "#cfa6b6",
            "ice": "#bfdcf5", "blossom": "#f5c2d6", "sun": "#ffd66b", "frost": "#bfe0ff"}


# Inks for text on the cream chrome (#eee3c9). Season inks only reach ~4.0:1 there,
# so git/list status text uses deeper tokens from the same system (all >= 4.7:1 on cream).
INK_ON_CREAM = {"green": "#4f6b3e", "amber": "#7a4a1e", "pink": "#6b3a4a", "blue": "#1b2a3a",
                "slate": "#6b5636", "gold": "#7a4a1e"}


def lum(h):
    h = h.lstrip("#")[:6]
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
