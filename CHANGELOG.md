# Changelog

## 2.2.3

- First version published automatically from GitHub with Trusted Publishing. Same content as 2.2.2, the first version on the Marketplace.

## 2.2.2

- Smaller, cleaner package: the build scripts are no longer listed in `package.json`, and the importable `.code-profile` files are only in the GitHub repository, not inside the extension.
- "obsidian" is no longer a search keyword; the README still describes the Obsidian syntax support.
- Licence holder is now JestingDart4369.
- The extension description no longer names VS Code.
- The five colour sets (Standard, Frühling, Sommer, Herbst, Winter) are now called "palettes" everywhere: the command **Novaroma: Choose Palette…** and the setting `novaroma.palette` replace the old command and setting. Set `novaroma.palette` again if you had chosen a fixed one; `auto` (follow the calendar) is still the default.
- GitHub Actions use vsce 4.1.0, the first version with `--oidc` for Trusted Publishing.
- The preview screenshots are no longer inside the extension (the Marketplace page loads them from GitHub); only the logo is packaged.

## 2.2.1

- Added a privacy statement (PRIVACY.md and a README section): Novaroma collects no data and makes no network requests.
- Added SUPPORT.md with where to ask questions and report bugs.

## 2.2.0

- Markdown preview understands Obsidian syntax: callouts (`> [!note]` with all Obsidian types and aliases), the alternate checkboxes (`- [>]`, `- [!]`, `- [?]`, `- [3]` and the rest), `#tags` as pills, `==highlights==`, hidden `%%comments%%` and footnotes. Wiki-links and embeds are left as text.

## 2.1.3

- Markdown preview: task lists (`- [ ]` and `- [x]`) now show as checkboxes instead of plain text.

## 2.1.2

- Fixed the file icon theme: icon paths are now relative to the icon theme file, so the icons load in VS Code.
- Removed the terminal prompt (Starship) feature; the extension no longer changes terminal settings or writes files.
- Releases are built and published by GitHub Actions; `main` is protected and `dev` builds test versions.

## 2.1.1

- Applying a theme now always sets the preferred light colour theme to the light version and the preferred dark colour theme to the dark version, also when light or dark is fixed.

## 2.1.0

- New Novaroma Product Icons: 97 VS Code interface icons in the Nova Roma line style.
- Markdown preview styling while a Novaroma theme is active.
- Novaroma terminal prompt for Starship, switchable for VS Code terminals.

## 2.0.0

- Renamed the extension to Novaroma.
- Reworked colour roles: declarations in `text`, keywords in `palette-ink`, control flow bold, built-in types italic, terminal ANSI colours, git, diff, debug and testing colours.
- Every text pair checked to at least 4.5:1; git decorations on cream chrome use deeper system tokens.
- New Novaroma Icons file icon theme.
- Automatic palette switching, light/dark and swapped commands, status bar item.
- Profiles: Standard, Focus, Presentation and Compact, with undo, plus importable .code-profile files.
- Extension icon and preview images.

## 1.0.0

- First version: 20 colour themes.
