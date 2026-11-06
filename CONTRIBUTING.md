# Working on Novaroma

## Branches

- `dev` is where changes are made and tested. Every push to `dev` runs the checks and replaces the **dev-build** pre-release on GitHub with a fresh test VSIX (Releases → "Novaroma dev build"). Install it with Extensions → … → Install from VSIX.
- `main` is protected. It only changes through a pull request from `dev`, and only when the **build** check passes. Force pushes and deleting the branch are blocked.
- Every merge into `main` that carries a new version is published to the Visual Studio Marketplace automatically, tagged `v<version>` and released on GitHub with the VSIX.

## Making a change

1. Work on `dev` (or a feature branch merged into `dev`).
2. If you changed colours or icons, regenerate the files:

   ```sh
   python3 build/build.py      # colour themes and file icon theme
   python3 build/check.py      # contrast check, must end with "failures: 0"
   python3 build/product_icons.py   # only after changing product icons
   python3 build/profiles.py   # only after changing src/presets.json
   ```

3. Push to `dev` and test the dev pre-release in VS Code.

## Releasing

1. On `dev`, raise `"version"` in `package.json` (for example 2.1.2 → 2.1.3) and add a `## 2.1.3` section at the top of `CHANGELOG.md`.
2. Push, and open a pull request from `dev` into `main`.
3. The **build** check also verifies that the version is new and has a changelog section.
4. Merge (squash or rebase). The **Publish** workflow publishes to the Marketplace, creates the tag `v2.1.3` and a GitHub release with the VSIX.

A merge into `main` without a new version only runs the workflow; nothing is published.

## One-time setup

- **Rulesets:** Settings → Rules → Rulesets → New ruleset → Import a ruleset, once with `.github/rulesets/main.json` and once with `.github/rulesets/dev.json`.
- **Marketplace publisher:** create the publisher `JestingDart4369` at marketplace.visualstudio.com/manage.
- **Trusted Publishing:** on the publisher page, Trusted Publishing → Create, with repository owner `JestingDart4369`, repository `novaroma-vscode`, workflow `publish.yml`, environment `marketplace`.
- **Environment (optional, recommended):** Settings → Environments → `marketplace` → Deployment branches and tags → Selected branches → `main`, so only `main` can publish.
