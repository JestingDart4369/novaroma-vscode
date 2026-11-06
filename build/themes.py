"""Colour themes: 5 seasons x light/dark x normal/swapped = 20 themes."""
from tokens import SEASONS, LIGHT, DARK, INK_LIGHT, INK_DARK, INK_ON_CREAM, ratio


def roles(mode, s):
    """Semantic roles. Every colour is a Nova Roma token."""
    P, I = (LIGHT, INK_LIGHT) if mode == "light" else (DARK, INK_DARK)
    r = {k: (v[s] if isinstance(v, dict) else v) for k, v in P.items()}
    r["keyword"] = r["season_ink"]
    if mode == "dark" and s == "standard":
        r["keyword"] = I["olive"]          # Standard dark season-ink equals main; use sv-amber
    r["string"] = I["green"]
    if mode == "light":
        r["number"] = I["pink"] if s == "winter" else I["blue"]
    else:
        r["number"] = INK_DARK["blossom"] if s == "winter" else INK_DARK["ice"]
    r["error"], r["warning"], r["info"] = I["pink"], I["amber"], I["blue"]
    r["added"], r["deleted"] = I["green"], I["pink"]
    r["modified"] = r["keyword"]
    r["ink"] = I
    return r


def ansi(mode):
    if mode == "light":
        I = INK_LIGHT
        return {"Black": I["text"], "Red": I["pink"], "Green": I["green"], "Yellow": I["gold"], "Blue": I["blue"],
                "Magenta": I["main"], "Cyan": I["slate"], "White": I["muted"],
                "BrightBlack": I["muted"], "BrightRed": I["ember"], "BrightGreen": I["green"],
                "BrightYellow": I["amber"], "BrightBlue": I["blue"], "BrightMagenta": I["rose"],
                "BrightCyan": I["slate"], "BrightWhite": I["main"]}
    I = INK_DARK
    return {"Black": "#6e3338", "Red": I["pink"], "Green": I["green"], "Yellow": I["gold"], "Blue": I["blue"],
            "Magenta": I["rose"], "Cyan": I["slate"], "White": I["main"],
            "BrightBlack": I["muted"], "BrightRed": I["blossom"], "BrightGreen": I["green"],
            "BrightYellow": I["sun"], "BrightBlue": I["ice"], "BrightMagenta": I["pink"],
            "BrightCyan": I["frost"], "BrightWhite": I["text"]}


def theme_name(mode, sname, swapped):
    return f"Novaroma {sname} {'Light' if mode == 'light' else 'Dark'}{' Swapped' if swapped else ''}"


def build(mode, s, sname, swapped):
    r = roles(mode, s)
    bg, main, text, accent, muted = r["bg"], r["main"], r["text"], r["accent"], r["muted"]
    season, sink = r["season"], r["season_ink"]
    on_season = main if mode == "light" else text          # ink on a season fill
    T = "#00000000"

    # Chrome = title bar, activity bar, side bar, tab strip.
    #   normal : accent fill, main ink   (like a primary button)
    #   swapped: main fill,  accent ink  (main and accent exchanged)
    cbg, cfg = (main, accent) if swapped else (accent, main)
    cdim = cfg + "d9"
    # A highlight that reads on the chrome: season-ink on light chrome, season fill on dark chrome
    chrome_is_light = (mode == "light") != swapped
    if chrome_is_light:
        c_hi = LIGHT["season_ink"][s]
    elif mode == "light":            # burgundy chrome (Light Swapped)
        c_hi = season
    else:                            # dark-burgundy chrome (Dark)
        c_hi = DARK["season_ink"][s] if s != "standard" else INK_DARK["olive"]

    # Selection in lists (side bar, quick open, menus, suggest)
    if mode == "light":
        if s == "standard" and not swapped:      # season == chrome there, so invert like a hovered button
            sel_bg, sel_fg, sel_in = main, accent, main + "b3"
        else:
            sel_bg, sel_fg, sel_in = season, main, season + "99"
    else:
        if not swapped:                          # dark seasons sit too close to the #6e3338 chrome
            sel_bg, sel_fg, sel_in = DARK["season_ink"][s] + "40", text, DARK["season_ink"][s] + "26"
        else:
            sel_bg, sel_fg, sel_in = season, text, season + "b3"

    # Badges: a season fill with burgundy ink, readable on every chrome
    if chrome_is_light and s == "standard":
        badge_bg, badge_fg = LIGHT["main"], LIGHT["accent"]
    else:
        badge_bg, badge_fg = LIGHT["season"][s], LIGHT["main"]
    # Git colours that read on the chrome
    gI = INK_ON_CREAM if chrome_is_light else INK_DARK

    btn_bg, btn_fg = (main, accent) if swapped else (accent, main)
    btn_hover = (accent, main) if swapped else (main, bg)

    c = {
        # base
        "focusBorder": text,
        "foreground": main,
        "disabledForeground": r["dis_ink"],
        "descriptionForeground": muted,
        "errorForeground": r["error"],
        "icon.foreground": main,
        "selection.background": season + "aa",
        "widget.border": accent,
        "widget.shadow": T, "scrollbar.shadow": T, "contrastBorder": T,
        "sash.hoverBorder": sink,
        "textLink.foreground": main, "textLink.activeForeground": muted,
        "textCodeBlock.background": accent + ("80" if mode == "light" else "66"),
        "textPreformat.foreground": main, "textPreformat.background": accent + "80",
        "textBlockQuote.background": accent + "40", "textBlockQuote.border": accent,
        "textSeparator.foreground": main,

        # editor
        "editor.background": bg,
        "editor.foreground": main,
        "editorCursor.foreground": sink,
        "editorLineNumber.foreground": muted,
        "editorLineNumber.activeForeground": text,
        "editorLineNumber.dimmedForeground": muted + "66",
        "editor.selectionBackground": (sink + "40") if (mode == "light" and s == "standard") else season + ("99" if mode == "light" else "cc"),
        "editor.selectionHighlightBackground": season + "4d",
        "editor.inactiveSelectionBackground": season + "4d",
        "editor.wordHighlightBackground": season + "40",
        "editor.wordHighlightStrongBackground": season + "66",
        "editor.findMatchBackground": season,
        "editor.findMatchBorder": sink,
        "editor.findMatchHighlightBackground": season + "66",
        "editor.findRangeHighlightBackground": accent + "4d",
        "editor.hoverHighlightBackground": season + "40",
        "editor.lineHighlightBackground": accent + ("59" if mode == "light" else "40"),
        "editor.lineHighlightBorder": T,
        "editor.rangeHighlightBackground": accent + "40",
        "editor.foldBackground": accent + "33",
        "editorWhitespace.foreground": muted + "40",
        "editorIndentGuide.background1": muted + "33",
        "editorIndentGuide.activeBackground1": muted + "99",
        "editorRuler.foreground": accent if mode == "light" else muted + "33",
        "editorCodeLens.foreground": muted,
        "editorInlayHint.background": accent + "66",
        "editorInlayHint.foreground": muted,
        "editorBracketMatch.background": season + "66",
        "editorBracketMatch.border": sink,
        "editorBracketHighlight.foreground1": main,
        "editorBracketHighlight.foreground2": r["keyword"],
        "editorBracketHighlight.foreground3": muted,
        "editorBracketHighlight.foreground4": main,
        "editorBracketHighlight.foreground5": r["keyword"],
        "editorBracketHighlight.foreground6": muted,
        "editorBracketHighlight.unexpectedBracket.foreground": r["error"],
        "editorGutter.background": bg,
        "editorGutter.addedBackground": r["added"],
        "editorGutter.modifiedBackground": r["modified"],
        "editorGutter.deletedBackground": r["deleted"],
        "editorGutter.foldingControlForeground": muted,
        "editorError.foreground": r["error"],
        "editorWarning.foreground": r["warning"],
        "editorInfo.foreground": r["info"],
        "editorHint.foreground": muted,
        "editorLink.activeForeground": sink,
        "editorOverviewRuler.border": T,
        "editorOverviewRuler.findMatchForeground": sink + "99",
        "editorOverviewRuler.errorForeground": r["error"],
        "editorOverviewRuler.warningForeground": r["warning"],
        "editorOverviewRuler.addedForeground": r["added"] + "99",
        "editorOverviewRuler.modifiedForeground": r["modified"] + "99",
        "editorOverviewRuler.deletedForeground": r["deleted"] + "99",
        "editorStickyScroll.background": bg,
        "editorStickyScrollHover.background": accent + "66",
        "editorStickyScroll.shadow": accent,

        # widgets (outlined, no shadows)
        "editorWidget.background": bg, "editorWidget.foreground": main, "editorWidget.border": accent,
        "editorSuggestWidget.background": bg, "editorSuggestWidget.border": accent,
        "editorSuggestWidget.foreground": main,
        "editorSuggestWidget.selectedBackground": sel_bg, "editorSuggestWidget.selectedForeground": sel_fg,
        "editorSuggestWidget.highlightForeground": text if mode == "light" else sink if s != "standard" else r["keyword"],
        "editorSuggestWidget.focusHighlightForeground": text,
        "editorHoverWidget.background": bg, "editorHoverWidget.border": accent,
        "editorHoverWidget.statusBarBackground": accent + "66",
        "debugExceptionWidget.background": bg, "debugExceptionWidget.border": r["error"],
        "peekView.border": sink,
        "peekViewEditor.background": bg, "peekViewEditor.matchHighlightBackground": season + "99",
        "peekViewResult.background": bg, "peekViewResult.selectionBackground": sel_bg,
        "peekViewResult.selectionForeground": sel_fg, "peekViewResult.matchHighlightBackground": season + "99",
        "peekViewTitle.background": accent, "peekViewTitleLabel.foreground": main if mode == "light" else text,
        "peekViewTitleDescription.foreground": main if mode == "light" else text,
        "minimap.background": bg,
        "minimap.selectionHighlight": season,
        "minimap.findMatchHighlight": sink,
        "minimapSlider.background": muted + "26",
        "minimapSlider.hoverBackground": muted + "40",

        # editor groups & tabs: active tab sits on the editor ground, season-ink rule on top
        "editorGroup.border": accent,
        "editorGroup.dropBackground": season + "66",
        "editorGroupHeader.tabsBackground": cbg,
        "editorGroupHeader.tabsBorder": T,
        "editorGroupHeader.noTabsBackground": bg,
        "tab.activeBackground": bg,
        "tab.activeForeground": text,
        "tab.activeBorderTop": sink,
        "tab.activeBorder": T,
        "tab.unfocusedActiveBackground": bg,
        "tab.unfocusedActiveForeground": main,
        "tab.unfocusedActiveBorderTop": muted,
        "tab.inactiveBackground": cbg,
        "tab.inactiveForeground": cdim,
        "tab.unfocusedInactiveForeground": cfg + "80",
        "tab.hoverBackground": cfg + "1f",
        "tab.hoverForeground": cfg,
        "tab.border": cbg,
        "tab.lastPinnedBorder": cfg + "40",
        "tab.activeModifiedBorder": sink,
        "tab.inactiveModifiedBorder": c_hi,
        "breadcrumb.background": bg,
        "breadcrumb.foreground": muted,
        "breadcrumb.focusForeground": text,
        "breadcrumb.activeSelectionForeground": text,
        "breadcrumbPicker.background": bg,

        # title / activity / side bar = chrome
        "titleBar.activeBackground": cbg, "titleBar.activeForeground": cfg,
        "titleBar.inactiveBackground": cbg, "titleBar.inactiveForeground": cdim,
        "titleBar.border": T,
        "commandCenter.background": cfg + "14", "commandCenter.foreground": cfg,
        "commandCenter.border": cfg + "40", "commandCenter.activeBackground": cfg + "26",
        "commandCenter.activeBorder": cfg + "66",
        "menubar.selectionBackground": cfg + "26", "menubar.selectionForeground": cfg,
        "activityBar.background": cbg, "activityBar.foreground": cfg,
        "activityBar.inactiveForeground": cfg + "99",
        "activityBar.activeBorder": c_hi, "activityBar.activeBackground": cfg + "14",
        "activityBar.border": T,
        "activityBar.dropBorder": c_hi,
        "activityBarBadge.background": badge_bg,
        "activityBarBadge.foreground": badge_fg,
        "sideBar.background": cbg, "sideBar.foreground": cfg, "sideBar.border": T,
        "sideBar.dropBackground": cfg + "1f",
        "sideBarTitle.foreground": cfg,
        "sideBarSectionHeader.background": cbg, "sideBarSectionHeader.foreground": cfg,
        "sideBarSectionHeader.border": cfg + "33",
        "sideBarActivityBarTop.border": cfg + "33",
        "tree.indentGuidesStroke": cfg + "4d",
        "tree.inactiveIndentGuidesStroke": cfg + "26",

        # lists (side bar and quick open both use these)
        "list.activeSelectionBackground": sel_bg, "list.activeSelectionForeground": sel_fg,
        "list.activeSelectionIconForeground": sel_fg,
        "list.inactiveSelectionBackground": sel_in, "list.inactiveSelectionForeground": sel_fg if mode == "dark" or sel_bg != main else cfg,
        "list.hoverBackground": cfg + "1a", "list.hoverForeground": cfg,
        "list.focusOutline": text if chrome_is_light == (mode == "light") else cfg,
        "list.focusAndSelectionOutline": T,
        "list.inactiveFocusOutline": T,
        "list.highlightForeground": c_hi,
        "list.focusHighlightForeground": sel_fg,
        "list.dropBackground": season + "66",
        "list.errorForeground": gI["pink"], "list.warningForeground": gI["amber"],
        "list.deemphasizedForeground": cfg + "80",

        # panel & terminal (on the editor ground)
        "panel.background": bg, "panel.border": accent,
        "panelTitle.activeForeground": text, "panelTitle.activeBorder": sink,
        "panelTitle.inactiveForeground": muted,
        "panelSectionHeader.background": accent + "40",
        "terminal.background": bg, "terminal.foreground": main,
        "terminalCursor.foreground": sink,
        "terminal.selectionBackground": season + "99",
        "terminal.findMatchBackground": season,
        "terminal.border": accent,
        "terminalCommandDecoration.defaultBackground": muted,
        "terminalCommandDecoration.successBackground": r["added"],
        "terminalCommandDecoration.errorBackground": r["error"],

        # status bar = the season mark
        "statusBar.background": season, "statusBar.foreground": on_season,
        "statusBar.border": T,
        "statusBar.noFolderBackground": season, "statusBar.noFolderForeground": on_season,
        "statusBar.debuggingBackground": main, "statusBar.debuggingForeground": bg,
        "statusBar.focusBorder": text,
        "statusBarItem.hoverBackground": main + "26",
        "statusBarItem.activeBackground": main + "40",
        "statusBarItem.remoteBackground": main, "statusBarItem.remoteForeground": bg,
        "statusBarItem.prominentBackground": main, "statusBarItem.prominentForeground": bg,
        "statusBarItem.errorBackground": r["error"], "statusBarItem.errorForeground": bg,
        "statusBarItem.warningBackground": r["warning"], "statusBarItem.warningForeground": bg,

        # inputs & buttons: the site's five-state pill button
        "input.background": bg, "input.foreground": main, "input.border": accent if mode == "light" else muted + "66",
        "input.placeholderForeground": muted,
        "inputOption.activeBackground": season, "inputOption.activeForeground": on_season,
        "inputOption.activeBorder": sink, "inputOption.hoverBackground": accent + "66",
        "inputValidation.errorBackground": bg, "inputValidation.errorBorder": r["error"],
        "inputValidation.warningBackground": bg, "inputValidation.warningBorder": r["warning"],
        "inputValidation.infoBackground": bg, "inputValidation.infoBorder": r["info"],
        "dropdown.background": bg, "dropdown.foreground": main, "dropdown.border": accent,
        "dropdown.listBackground": bg,
        "checkbox.background": bg, "checkbox.foreground": main, "checkbox.border": main,
        "checkbox.selectBackground": bg, "checkbox.selectBorder": sink,
        "radio.activeBackground": season, "radio.activeForeground": on_season, "radio.activeBorder": sink,
        "button.background": btn_bg, "button.foreground": btn_fg,
        "button.hoverBackground": btn_hover[0],
        "button.border": main if not swapped else T,
        "button.separator": btn_fg + "66",
        "button.secondaryBackground": bg, "button.secondaryForeground": main,
        "button.secondaryHoverBackground": accent,
        "toolbar.hoverBackground": accent + "80",
        "toolbar.activeBackground": accent,
        "badge.background": badge_bg, "badge.foreground": badge_fg,
        "progressBar.background": sink,
        "scrollbarSlider.background": muted + "33",
        "scrollbarSlider.hoverBackground": muted + "59",
        "scrollbarSlider.activeBackground": muted + "80",

        # menus, quick input, notifications
        "menu.background": bg, "menu.foreground": main, "menu.border": accent,
        "menu.selectionBackground": sel_bg, "menu.selectionForeground": sel_fg,
        "menu.separatorBackground": accent,
        "quickInput.background": bg, "quickInput.foreground": main,
        "quickInputTitle.background": accent + "66",
        "quickInputList.focusBackground": sel_bg, "quickInputList.focusForeground": sel_fg,
        "quickInputList.focusIconForeground": sel_fg,
        "pickerGroup.foreground": sink if mode == "light" else r["keyword"], "pickerGroup.border": accent,
        "keybindingLabel.background": accent + "80",
        "keybindingLabel.foreground": main if mode == "light" else text,
        "keybindingLabel.border": accent, "keybindingLabel.bottomBorder": accent,
        "notifications.background": bg, "notifications.foreground": main, "notifications.border": accent,
        "notificationCenterHeader.background": accent, "notificationCenterHeader.foreground": main if mode == "light" else text,
        "notificationToast.border": accent,
        "notificationsErrorIcon.foreground": r["error"],
        "notificationsWarningIcon.foreground": r["warning"],
        "notificationsInfoIcon.foreground": r["info"],
        "notificationLink.foreground": sink if mode == "light" else r["keyword"],

        # git / scm (decorations live on the chrome)
        "gitDecoration.addedResourceForeground": gI["green"],
        "gitDecoration.untrackedResourceForeground": gI["green"],
        "gitDecoration.modifiedResourceForeground": gI["amber"] if chrome_is_light else c_hi,
        "gitDecoration.stageModifiedResourceForeground": gI["amber"] if chrome_is_light else c_hi,
        "gitDecoration.deletedResourceForeground": gI["pink"],
        "gitDecoration.stageDeletedResourceForeground": gI["pink"],
        "gitDecoration.renamedResourceForeground": gI["blue"],
        "gitDecoration.conflictingResourceForeground": gI["pink"],
        "gitDecoration.ignoredResourceForeground": cfg + "73",
        "gitDecoration.submoduleResourceForeground": gI["slate"],
        "scmGraph.foreground1": sink, "scmGraph.foreground2": r["string"], "scmGraph.foreground3": r["number"],
        "diffEditor.insertedTextBackground": r["added"] + "26",
        "diffEditor.removedTextBackground": r["deleted"] + "26",
        "diffEditor.insertedLineBackground": r["added"] + "14",
        "diffEditor.removedLineBackground": r["deleted"] + "14",
        "diffEditor.border": accent,
        "merge.currentHeaderBackground": r["added"] + "59", "merge.currentContentBackground": r["added"] + "1f",
        "merge.incomingHeaderBackground": r["info"] + "59", "merge.incomingContentBackground": r["info"] + "1f",

        # debug, testing, welcome
        "debugToolBar.background": bg, "debugToolBar.border": accent,
        "debugIcon.breakpointForeground": r["error"],
        "debugIcon.startForeground": r["added"],
        "editor.stackFrameHighlightBackground": season + "66",
        "testing.iconPassed": r["added"], "testing.iconFailed": r["error"], "testing.iconQueued": r["warning"],
        "welcomePage.tileBackground": bg, "welcomePage.tileBorder": accent, "welcomePage.tileHoverBackground": accent + "66",
        "walkThrough.embeddedEditorBackground": bg,
        "settings.headerForeground": text, "settings.modifiedItemIndicator": sink,
        "settings.focusedRowBackground": accent + "33",
        "chat.requestBorder": accent, "chat.avatarBackground": accent, "chat.avatarForeground": main if mode == "light" else text,
        "chat.slashCommandBackground": season, "chat.slashCommandForeground": on_season,
    }
    for k, v in ansi(mode).items():
        c[f"terminal.ansi{k}"] = v

    kw, st, num, ty = r["keyword"], r["string"], r["number"], main
    tc = [
        ("Comment", ["comment", "punctuation.definition.comment", "string.quoted.docstring",
                     "comment.block.documentation"], muted, "italic"),
        ("Doc tags", ["storage.type.class.jsdoc", "keyword.other.documentation", "comment.block.documentation storage"], muted, "bold italic"),
        ("Control flow", ["keyword.control", "keyword.control.flow", "keyword.control.import",
                          "keyword.control.conditional", "keyword.control.loop", "keyword.control.return",
                          "keyword.control.trycatch", "keyword.control.from", "keyword.other.using",
                          "keyword.other.import"], kw, "bold"),
        ("Keywords & storage", ["keyword", "storage", "storage.type", "storage.modifier", "keyword.other",
                                "keyword.operator.new", "keyword.operator.expression", "keyword.operator.word",
                                "keyword.operator.logical.python", "keyword.other.DML.sql",
                                "keyword.other.DDL.sql", "keyword.other.sql"], kw, ""),
        ("Operators & punctuation", ["keyword.operator", "punctuation", "meta.brace", "punctuation.separator",
                                     "punctuation.terminator", "punctuation.accessor"], muted, ""),
        ("Strings", ["string", "string.quoted", "string.template", "string.unquoted.yaml",
                     "string.unquoted.plain.out.yaml"], st, ""),
        ("String interpolation", ["punctuation.definition.template-expression", "meta.template.expression",
                                  "constant.character.format.placeholder", "punctuation.section.embedded"], kw, ""),
        ("Escapes & regex", ["constant.character.escape", "string.regexp", "constant.other.character-class.regexp"], num, ""),
        ("Numbers & constants", ["constant.numeric", "constant.language", "constant.other", "support.constant",
                                 "variable.other.constant", "variable.other.enummember", "constant.language.boolean",
                                 "constant.language.python", "constant.language.null"], num, ""),
        ("Function declarations", ["entity.name.function", "meta.definition.method entity.name.function",
                                   "entity.name.function.member"], text, "bold"),
        ("Function calls", ["meta.function-call entity.name.function", "meta.function-call.generic",
                            "support.function", "variable.function", "entity.name.function.call",
                            "meta.method-call entity.name.function", "support.function.builtin"], text, ""),
        ("Types & classes", ["entity.name.type", "entity.name.class", "entity.name.namespace",
                             "entity.other.inherited-class", "entity.name.type.class", "entity.name.struct",
                             "entity.name.type.interface", "entity.name.type.enum"], ty, "bold"),
        ("Built-in types", ["support.type", "support.class", "storage.type.primitive", "storage.type.built-in",
                            "support.type.python", "storage.type.cs", "keyword.type"], ty, "italic"),
        ("Variables", ["variable", "variable.other", "variable.other.readwrite", "meta.definition.variable"], main, ""),
        ("Parameters", ["variable.parameter", "meta.function.parameters variable"], main, "italic"),
        ("Self / this", ["variable.language", "variable.parameter.function.language.special.self.python",
                         "variable.language.this", "keyword.other.this"], kw, "italic"),
        ("Properties & keys", ["variable.other.property", "variable.other.object.property",
                               "support.variable.property", "meta.object-literal.key", "entity.name.tag.yaml",
                               "support.type.property-name.json", "support.type.property-name.toml",
                               "variable.other.member"], main, ""),
        ("Decorators & attributes", ["entity.name.function.decorator", "meta.decorator", "punctuation.decorator",
                                     "meta.attribute.cs", "entity.name.function.attribute", "storage.type.annotation"], kw, "italic"),
        ("Tags", ["entity.name.tag", "punctuation.definition.tag"], kw, ""),
        ("Tag attributes", ["entity.other.attribute-name"], muted, "italic"),
        ("CSS selectors", ["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css",
                           "entity.name.tag.css", "entity.other.attribute-name.pseudo-class.css"], kw, ""),
        ("CSS properties", ["support.type.property-name.css", "support.type.vendored.property-name.css"], main, ""),
        ("CSS values & units", ["support.constant.property-value.css", "keyword.other.unit", "constant.other.color"], num, ""),
        ("Markdown heading", ["markup.heading", "entity.name.section", "punctuation.definition.heading.markdown"], text, "bold"),
        ("Markdown bold", ["markup.bold"], text, "bold"),
        ("Markdown italic", ["markup.italic"], main, "italic"),
        ("Markdown strike", ["markup.strikethrough"], muted, "strikethrough"),
        ("Markdown link", ["markup.underline.link", "string.other.link", "meta.link.inline.markdown"], kw, "underline"),
        ("Markdown inline code", ["markup.inline.raw", "markup.fenced_code.block.markdown punctuation"], num, ""),
        ("Markdown quote", ["markup.quote"], muted, "italic"),
        ("Markdown list", ["punctuation.definition.list.begin.markdown", "beginning.punctuation.definition.list"], kw, ""),
        ("Diff inserted", ["markup.inserted"], r["added"], ""),
        ("Diff deleted", ["markup.deleted"], r["deleted"], ""),
        ("Diff changed", ["markup.changed"], r["modified"], ""),
        ("Invalid", ["invalid", "invalid.illegal"], r["error"], "underline"),
    ]
    token_colors = []
    for n, scope, fg, fs in tc:
        stl = {"foreground": fg}
        if fs:
            stl["fontStyle"] = fs
        token_colors.append({"name": n, "scope": scope, "settings": stl})

    semantic = {
        "namespace": {"foreground": ty, "bold": True},
        "class": {"foreground": ty, "bold": True},
        "class.defaultLibrary": {"foreground": ty, "italic": True},
        "type": {"foreground": ty, "bold": True},
        "type.defaultLibrary": {"foreground": ty, "italic": True},
        "interface": {"foreground": ty, "bold": True},
        "enum": {"foreground": ty, "bold": True},
        "struct": {"foreground": ty, "bold": True},
        "typeParameter": {"foreground": ty, "italic": True},
        "function.declaration": {"foreground": text, "bold": True},
        "method.declaration": {"foreground": text, "bold": True},
        "function": text, "method": text,
        "function.defaultLibrary": text,
        "parameter": {"foreground": main, "italic": True},
        "variable": main,
        "variable.readonly": num,
        "variable.readonly.defaultLibrary": num,
        "enumMember": num,
        "property": main,
        "property.readonly": main,
        "keyword": kw,
        "decorator": {"foreground": kw, "italic": True},
        "selfParameter": {"foreground": kw, "italic": True},
        "clsParameter": {"foreground": kw, "italic": True},
        "builtinConstant": num,
        "magicFunction": text,
        "comment": {"foreground": muted, "italic": True},
        "string": st,
        "number": num,
    }

    report = {k: round(ratio(v, bg), 2) for k, v in
              {"main": main, "text": text, "muted": muted, "keyword": kw, "string": st, "number": num}.items()}
    report["chrome"] = round(ratio(cfg, cbg), 2)
    report["chrome-hi"] = round(ratio(c_hi, cbg), 2)
    report["status"] = round(ratio(on_season, season), 2)
    report["list-sel"] = round(ratio(sel_fg, sel_bg[:7]), 2)
    name = theme_name(mode, sname, swapped)
    return name, {
        "$schema": "vscode://schemas/color-theme",
        "name": name, "type": mode, "semanticHighlighting": True,
        "colors": c, "tokenColors": token_colors, "semanticTokenColors": semantic,
    }, report, r, (cbg, cfg)


def all_themes():
    for mode in ("light", "dark"):
        for s, sname in SEASONS:
            for swapped in (False, True):
                yield (mode, s, sname, swapped) + build(mode, s, sname, swapped)
