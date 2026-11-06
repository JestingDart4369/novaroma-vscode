// Novaroma — season, light/dark and profile switching for the Novaroma themes.
"use strict";
const vscode = require("vscode");
const presets = require("./presets.json");
const { taskLists } = require("./tasklists");

const SEASONS = [
  { id: "standard", name: "Standard", detail: "The live novaroma-homelab.uk colours" },
  { id: "fruehling", name: "Frühling", detail: "March – May · cherry blossom" },
  { id: "sommer", name: "Sommer", detail: "June – August · sun" },
  { id: "herbst", name: "Herbst", detail: "September – November · amber" },
  { id: "winter", name: "Winter", detail: "December – February · ice" },
];
const BACKUP_KEY = "novaroma.profileBackup";
const G = vscode.ConfigurationTarget.Global;

let statusItem;
let timer;
let applying = false;
let ctx;
const LAST_KEY = "novaroma.lastApplied";

function activeThemeNames() {
  const wb = vscode.workspace.getConfiguration("workbench");
  const win = vscode.workspace.getConfiguration("window");
  return win.get("autoDetectColorScheme")
    ? { auto: true, light: wb.get("preferredLightColorTheme"), dark: wb.get("preferredDarkColorTheme") }
    : { auto: false, theme: wb.get("colorTheme") };
}

function cfg() {
  return vscode.workspace.getConfiguration("novaroma");
}

function seasonByDate(d = new Date()) {
  const m = d.getMonth(); // 0 = January
  if (m >= 2 && m <= 4) return "fruehling";
  if (m >= 5 && m <= 7) return "sommer";
  if (m >= 8 && m <= 10) return "herbst";
  return "winter";
}

function currentSeason() {
  const s = cfg().get("season", "auto");
  return s === "auto" ? seasonByDate() : s;
}

function seasonName(id) {
  return (SEASONS.find((s) => s.id === id) || SEASONS[0]).name;
}

function themeName(season, mode, variant) {
  return `Novaroma ${seasonName(season)} ${mode === "light" ? "Light" : "Dark"}${variant === "swapped" ? " Swapped" : ""}`;
}

function targets() {
  const season = currentSeason();
  const variant = cfg().get("variant", "normal");
  return {
    season,
    variant,
    appearance: cfg().get("appearance", "system"),
    light: themeName(season, "light", variant),
    dark: themeName(season, "dark", variant),
  };
}

function novaromaActive() {
  const wb = vscode.workspace.getConfiguration("workbench");
  const win = vscode.workspace.getConfiguration("window");
  const isNR = (t) => typeof t === "string" && t.startsWith("Novaroma ");
  if (win.get("autoDetectColorScheme")) {
    return isNR(wb.get("preferredLightColorTheme")) || isNR(wb.get("preferredDarkColorTheme"));
  }
  return isNR(wb.get("colorTheme"));
}

function systemIsDark() {
  const k = vscode.window.activeColorTheme.kind;
  return k === vscode.ColorThemeKind.Dark || k === vscode.ColorThemeKind.HighContrast;
}

async function apply() {
  applying = true;
  try {
    await applyInner();
  } finally {
    applying = false;
  }
}

async function applyInner() {
  const t = targets();
  const wb = vscode.workspace.getConfiguration("workbench");
  const win = vscode.workspace.getConfiguration("window");
  // Always pair the two: the light version is the preferred light theme, the dark version the preferred dark theme.
  await wb.update("preferredLightColorTheme", t.light, G);
  await wb.update("preferredDarkColorTheme", t.dark, G);
  if (t.appearance === "system") {
    await win.update("autoDetectColorScheme", true, G);
    await wb.update("colorTheme", systemIsDark() ? t.dark : t.light, G);
  } else {
    await win.update("autoDetectColorScheme", false, G);
    await wb.update("colorTheme", t.appearance === "dark" ? t.dark : t.light, G);
  }
  if (cfg().get("setIconTheme", true)) {
    await wb.update("iconTheme", "novaroma-icons", G);
  }
  if (cfg().get("setProductIconTheme", true)) {
    await wb.update("productIconTheme", "novaroma-product-icons", G);
  }
  if (ctx) await ctx.globalState.update(LAST_KEY, activeThemeNames());
  updateStatus();
}

// Re-apply only if Novaroma is in use and the expected theme differs (e.g. a new season began).
async function maybeAutoApply() {
  if (!cfg().get("autoApply", true) || !novaromaActive()) return;
  const t = targets();
  const wb = vscode.workspace.getConfiguration("workbench");
  const win = vscode.workspace.getConfiguration("window");
  const pairOk = wb.get("preferredLightColorTheme") === t.light && wb.get("preferredDarkColorTheme") === t.dark;
  const upToDate = pairOk && (win.get("autoDetectColorScheme")
    ? t.appearance === "system"
    : wb.get("colorTheme") === (t.appearance === "dark" ? t.dark : t.light) && t.appearance !== "system");
  if (!upToDate) await apply();
}

// A Novaroma theme picked by hand in the theme picker becomes the new choice.
async function syncFromThemeName(name) {
  if (applying) return;
  applying = true;
  try {
    await syncInner(name);
  } finally {
    applying = false;
  }
  updateStatus();
}

async function syncInner(name) {
  const m = /^Novaroma (\S+) (Light|Dark)( Swapped)?$/.exec(name || "");
  if (!m) return;
  const season = SEASONS.find((s) => s.name === m[1]);
  if (!season) return;
  const variant = m[3] ? "swapped" : "normal";
  if (cfg().get("variant", "normal") !== variant) await cfg().update("variant", variant, G);
  if (currentSeason() !== season.id) {
    await cfg().update("season", season.id === seasonByDate() ? "auto" : season.id, G);
  }
  if (!vscode.workspace.getConfiguration("window").get("autoDetectColorScheme")) {
    const mode = m[2].toLowerCase();
    if (cfg().get("appearance", "system") !== mode) await cfg().update("appearance", mode, G);
  }
}

function updateStatus() {
  if (!statusItem) return;
  if (!cfg().get("showStatusBarItem", true) || !novaromaActive()) {
    statusItem.hide();
    return;
  }
  const t = targets();
  const auto = cfg().get("season", "auto") === "auto";
  statusItem.text = `$(symbol-color) ${seasonName(t.season)}`;
  statusItem.tooltip = new vscode.MarkdownString(
    `**Novaroma** · ${seasonName(t.season)}${auto ? " (automatic)" : ""}\n\n` +
      `${t.appearance === "system" ? "Follows system light/dark" : t.appearance === "dark" ? "Dark" : "Light"} · ` +
      `${t.variant === "swapped" ? "swapped" : "normal"} colours\n\nClick for options`
  );
  statusItem.show();
}

async function chooseSeason() {
  const now = cfg().get("season", "auto");
  const items = [
    { label: "$(calendar) Automatic", description: `now ${seasonName(seasonByDate())}`, id: "auto" },
    ...SEASONS.map((s) => ({ label: s.name, description: s.detail, id: s.id })),
  ].map((i) => ({ ...i, picked: i.id === now, detail: i.id === now ? "current" : undefined }));
  const pick = await vscode.window.showQuickPick(items, { title: "Novaroma: Season" });
  if (!pick) return;
  await cfg().update("season", pick.id, G);
  await apply();
}

async function chooseAppearance() {
  const now = cfg().get("appearance", "system");
  const items = [
    { label: "$(color-mode) Follow system", id: "system" },
    { label: "$(circle-large-outline) Light", id: "light" },
    { label: "$(circle-large-filled) Dark", id: "dark" },
  ].map((i) => ({ ...i, description: i.id === now ? "current" : undefined }));
  const pick = await vscode.window.showQuickPick(items, { title: "Novaroma: Light / Dark" });
  if (!pick) return;
  await cfg().update("appearance", pick.id, G);
  await apply();
}

async function toggleSwapped() {
  const v = cfg().get("variant", "normal") === "swapped" ? "normal" : "swapped";
  await cfg().update("variant", v, G);
  await apply();
  vscode.window.setStatusBarMessage(`Novaroma: ${v === "swapped" ? "swapped" : "normal"} colours`, 3000);
}

async function applyProfile(context) {
  const items = presets.presets.map((p) => ({
    label: `$(${p.icon}) ${p.label}`,
    detail: p.description,
    preset: p,
  }));
  const pick = await vscode.window.showQuickPick(items, { title: "Novaroma: Apply Profile", matchOnDetail: true });
  if (!pick) return;
  const settings = { ...presets.base, ...pick.preset.settings };

  // Back up what is changed, so "Undo Last Profile" can restore it.
  const backup = {};
  for (const key of Object.keys(settings)) {
    const dot = key.lastIndexOf(".");
    const section = vscode.workspace.getConfiguration(key.slice(0, dot));
    const info = section.inspect(key.slice(dot + 1));
    backup[key] = info ? info.globalValue : undefined;
  }
  const wb = vscode.workspace.getConfiguration("workbench");
  const win = vscode.workspace.getConfiguration("window");
  for (const [k, v] of [
    ["workbench.colorTheme", wb.inspect("colorTheme").globalValue],
    ["workbench.iconTheme", wb.inspect("iconTheme").globalValue],
    ["workbench.productIconTheme", wb.inspect("productIconTheme").globalValue],
    ["workbench.preferredLightColorTheme", wb.inspect("preferredLightColorTheme").globalValue],
    ["workbench.preferredDarkColorTheme", wb.inspect("preferredDarkColorTheme").globalValue],
    ["window.autoDetectColorScheme", win.inspect("autoDetectColorScheme").globalValue],
  ]) {
    if (!(k in backup)) backup[k] = v;
  }
  await context.globalState.update(BACKUP_KEY, { profile: pick.preset.label, values: backup });

  for (const [key, value] of Object.entries(settings)) {
    const dot = key.lastIndexOf(".");
    await vscode.workspace.getConfiguration(key.slice(0, dot)).update(key.slice(dot + 1), value, G);
  }
  await apply();
  const choice = await vscode.window.showInformationMessage(
    `${pick.preset.label} applied (${Object.keys(settings).length} settings).`,
    "Undo"
  );
  if (choice === "Undo") await resetProfile(context);
}

async function resetProfile(context) {
  const b = context.globalState.get(BACKUP_KEY);
  if (!b) {
    vscode.window.showInformationMessage("Novaroma: no profile to undo.");
    return;
  }
  for (const [key, value] of Object.entries(b.values)) {
    const dot = key.lastIndexOf(".");
    await vscode.workspace.getConfiguration(key.slice(0, dot)).update(key.slice(dot + 1), value, G);
  }
  await context.globalState.update(BACKUP_KEY, undefined);
  updateStatus();
  vscode.window.showInformationMessage(`Novaroma: restored the settings from before ${b.profile}.`);
}

async function menu(context) {
  const t = targets();
  const items = [
    { label: `$(calendar) Season: ${seasonName(t.season)}`, description: cfg().get("season") === "auto" ? "automatic" : "", run: chooseSeason },
    { label: `$(color-mode) Light / Dark: ${t.appearance}`, run: chooseAppearance },
    { label: `$(arrow-swap) Colours: ${t.variant}`, description: "toggle swapped", run: toggleSwapped },
    { label: "$(account) Apply profile…", run: () => applyProfile(context) },
    { label: "$(discard) Undo last profile", run: () => resetProfile(context) },
  ];
  const pick = await vscode.window.showQuickPick(items, { title: "Novaroma" });
  if (pick) await pick.run();
}

// On start: if the Novaroma theme in use is not the one this extension last set
// (first run, theme picker, settings sync), adopt it as the user's choice first.
async function startup() {
  if (novaromaActive()) {
    const now = activeThemeNames();
    const last = ctx.globalState.get(LAST_KEY);
    if (!last || JSON.stringify(last) !== JSON.stringify(now)) {
      const name = now.auto ? (systemIsDark() ? now.dark : now.light) : now.theme;
      await syncFromThemeName(name);
      await ctx.globalState.update(LAST_KEY, now);
    }
  }
  await maybeAutoApply();
  updateStatus();
}

function activate(context) {
  ctx = context;
  const reg = (id, fn) => context.subscriptions.push(vscode.commands.registerCommand(id, fn));
  reg("novaroma.menu", () => menu(context));
  reg("novaroma.applyProfile", () => applyProfile(context));
  reg("novaroma.resetProfile", () => resetProfile(context));
  reg("novaroma.chooseSeason", chooseSeason);
  reg("novaroma.chooseAppearance", chooseAppearance);
  reg("novaroma.toggleSwapped", toggleSwapped);
  reg("novaroma.apply", apply);

  statusItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusItem.command = "novaroma.menu";
  statusItem.name = "Novaroma season";
  context.subscriptions.push(statusItem);

  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (applying) return;
      if (e.affectsConfiguration("novaroma.season") || e.affectsConfiguration("novaroma.variant") ||
          e.affectsConfiguration("novaroma.appearance")) {
        maybeAutoApply();
      }
      const wb = vscode.workspace.getConfiguration("workbench");
      if (e.affectsConfiguration("workbench.colorTheme")) syncFromThemeName(wb.get("colorTheme"));
      if (e.affectsConfiguration("workbench.preferredLightColorTheme")) syncFromThemeName(wb.get("preferredLightColorTheme"));
      if (e.affectsConfiguration("workbench.preferredDarkColorTheme")) syncFromThemeName(wb.get("preferredDarkColorTheme"));
      if (e.affectsConfiguration("workbench") || e.affectsConfiguration("window") ||
          e.affectsConfiguration("novaroma.showStatusBarItem")) {
        updateStatus();
      }
    })
  );

  // The season can change while VS Code stays open: check every six hours.
  timer = setInterval(maybeAutoApply, 6 * 60 * 60 * 1000);
  context.subscriptions.push({ dispose: () => clearInterval(timer) });

  startup();

  // Markdown preview: render "- [ ]" / "- [x]" as checkboxes.
  return { extendMarkdownIt: (md) => taskLists(md) };
}

function deactivate() {}

module.exports = { activate, deactivate };
