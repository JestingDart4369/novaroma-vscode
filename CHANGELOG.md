# Changelog

## 2.1.2

- Fixed the file icon theme: icon paths are now relative to the icon theme file, so the icons load in VS Code.
- Releases are built and published by GitHub Actions; `main` is protected and `dev` builds test versions.

## 2.1.1

- Applying a theme now always sets the preferred light colour theme to the light version and the preferred dark colour theme to the dark version, also when light or dark is fixed.

## 2.1.0

- New Novaroma Product Icons: 97 VS Code interface icons in the Nova Roma line style.
- Markdown preview styling while a Novaroma theme is active.
- Novaroma terminal prompt for Starship, switchable for VS Code terminals.

## 2.0.0

- Renamed the extension to Novaroma.
- Reworked colour roles: declarations in `text`, keywords in `season-ink`, control flow bold, built-in types italic, terminal ANSI colours, git, diff, debug and testing colours.
- Every text pair checked to at least 4.5:1; git decorations on cream chrome use deeper system tokens.
- New Novaroma Icons file icon theme.
- Automatic season switching, light/dark and swapped commands, status bar item.
- Profiles: Standard, Focus, Presentation and Compact, with undo, plus importable .code-profile files.
- Extension icon and preview images.

## 1.0.0

- First version: 20 colour themes.
