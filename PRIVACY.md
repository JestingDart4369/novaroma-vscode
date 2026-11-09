# Privacy statement

Novaroma is a theme extension for Visual Studio Code. This statement covers every version of the extension published under the Marketplace publisher ID `JestingDart4369`.

## Data collection

Novaroma does not collect, store, send or share any personal data or usage data.

- It contains no telemetry and no analytics.
- It makes no network requests and does not contact any server, including novaroma-homelab.uk.
- It does not read, open or upload your files, your workspace or your Markdown notes. The Markdown preview styling runs inside VS Code's own preview, on the note VS Code is already showing.
- It does not start processes, run scripts or download anything.

## What the extension changes on your computer

Novaroma only uses the VS Code extension API, and only for these purposes:

- **VS Code settings**: when you run a Novaroma command (apply theme, choose palette, light/dark, swapped colours, apply profile), it changes the related VS Code settings, such as `workbench.colorTheme`, `workbench.iconTheme`, `workbench.productIconTheme` and the editor settings listed for each profile in the README. While a Novaroma theme is in use and `novaroma.autoApply` is on, it also switches to the next palette's theme on 1 March, 1 June, 1 September and 1 December. Turn `novaroma.autoApply` off to prevent this.
- **Local extension storage**: it keeps two small values in VS Code's own storage for the extension, which never leaves your computer: the settings a profile replaced (so **Novaroma: Undo Last Profile** can restore them) and the name of the theme it last applied.

Uninstalling the extension removes this storage. The VS Code settings it changed stay as they are, like any setting you changed yourself.

## Contact

Questions about privacy: open an issue at https://github.com/JestingDart4369/novaroma-vscode/issues.
