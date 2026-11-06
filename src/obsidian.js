// Obsidian syntax for the Markdown preview (no wiki-links or embeds):
//   > [!note] Title     callouts (all Obsidian types and aliases, +/- fold markers accepted)
//   #tag                tags as pills
//   ==text==            highlights
//   %%comment%%         hidden comments, inline or across lines
// markdown-it plugin with no dependencies.
"use strict";

// ---- comments --------------------------------------------------------------------------
// Blank out %%…%% before parsing. Newlines are kept so preview scroll-sync stays in line.
// Fenced code blocks and inline code are left alone.
function stripComments(src) {
  const lines = src.split("\n");
  let fence = null; // e.g. "```" or "~~~~"
  let inComment = false;
  for (let n = 0; n < lines.length; n++) {
    let line = lines[n];
    if (!inComment) {
      const f = /^ {0,3}(`{3,}|~{3,})/.exec(line);
      if (fence) {
        if (f && f[1][0] === fence[0] && f[1].length >= fence.length && /^ {0,3}[`~]+\s*$/.test(line)) fence = null;
        continue;
      }
      if (f) {
        fence = f[1];
        continue;
      }
    }
    let out = "";
    let i = 0;
    while (i < line.length) {
      if (inComment) {
        const end = line.indexOf("%%", i);
        if (end === -1) {
          i = line.length;
        } else {
          inComment = false;
          i = end + 2;
        }
        continue;
      }
      if (line[i] === "`") {
        const run = /^`+/.exec(line.slice(i))[0];
        const close = line.indexOf(run, i + run.length);
        if (close !== -1) {
          out += line.slice(i, close + run.length);
          i = close + run.length;
          continue;
        }
        out += run;
        i += run.length;
        continue;
      }
      if (line.startsWith("%%", i)) {
        inComment = true;
        i += 2;
        continue;
      }
      out += line[i];
      i++;
    }
    lines[n] = out;
  }
  return lines.join("\n");
}

// ---- callouts --------------------------------------------------------------------------
const TYPES = {
  note: "note",
  abstract: "abstract", summary: "abstract", tldr: "abstract",
  info: "info",
  todo: "todo",
  tip: "tip", hint: "tip", important: "tip",
  success: "success", check: "success", done: "success",
  question: "question", help: "question", faq: "question",
  warning: "warning", caution: "warning", attention: "warning",
  failure: "failure", fail: "failure", missing: "failure",
  danger: "danger", error: "danger",
  bug: "bug",
  example: "example",
  quote: "quote", cite: "quote",
};

// 24px line icons, drawn like the Novaroma product icons (stroke = currentColor)
const P = (d) => `<path d="${d}"/>`;
const ICONS = {
  note: P("M4 20l1-4.5L15.5 5a2.1 2.1 0 0 1 3 0l.5.5a2.1 2.1 0 0 1 0 3L8.5 19z") + P("M14 6.5l3.5 3.5"),
  abstract: P("M8 4h8M8 4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2M9 10h6M9 14h6M9 18h3"),
  info: '<circle cx="12" cy="12" r="9"/>' + P("M12 11v6M12 7.6v.1"),
  todo: '<circle cx="12" cy="12" r="9"/>' + P("M8 12.3l2.8 2.8L16.2 9.5"),
  tip: P("M12 3c1 3 4 4.5 4 8.5a4 4 0 0 1-8 0c0-1.8.8-3 1.8-4 .2 1.6 1 2.5 2.2 2.5C12 8 11 6 12 3z") + P("M10 20.5h4"),
  success: P("M5 12.5l4.5 4.5L19 7"),
  question: '<circle cx="12" cy="12" r="9"/>' + P("M9.5 9.5a2.5 2.5 0 1 1 3.4 2.3c-.6.3-.9.8-.9 1.4v.6M12 16.8v.1"),
  warning: P("M12 3.5L21.5 20h-19z") + P("M12 10v4.5M12 17.3v.1"),
  failure: P("M6 6l12 12M18 6L6 18"),
  danger: P("M13 2.5L5 13.5h6l-1 8 8-11h-6z"),
  bug: P("M8 9a4 4 0 0 1 8 0v6a4 4 0 0 1-8 0zM12 9v10M4 13h4M16 13h4M5 7.5l3 2M19 7.5l-3 2M5 19l3-2M19 19l-3-2"),
  example: P("M4 6h16M4 12h16M4 18h10"),
  quote: P("M9 7H6a2 2 0 0 0-2 2v3h5v5H4M20 7h-3a2 2 0 0 0-2 2v3h5v5h-5"),
};

function icon(type) {
  return `<svg class="callout-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" ` +
    `stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[type]}</svg>`;
}

const HEAD = /^\[!([^\]\s]+)\]([+-]?)[ \t]*(.*)$/;

function callouts(state) {
  const tokens = state.tokens;
  for (let i = 0; i < tokens.length - 2; i++) {
    const open = tokens[i];
    if (open.type !== "blockquote_open") continue;
    const pOpen = tokens[i + 1];
    const inline = tokens[i + 2];
    if (pOpen.type !== "paragraph_open" || inline.type !== "inline") continue;

    const nl = inline.content.indexOf("\n");
    const firstLine = nl === -1 ? inline.content : inline.content.slice(0, nl);
    const m = HEAD.exec(firstLine);
    if (!m) continue;

    const raw = m[1].toLowerCase();
    const type = TYPES[raw] || "note";
    const titleText = m[3].trim() || raw.charAt(0).toUpperCase() + raw.slice(1);
    const rest = nl === -1 ? "" : inline.content.slice(nl + 1);

    open.attrJoin("class", "callout");
    open.attrSet("data-callout", type);
    if (m[2]) open.attrSet("data-callout-fold", m[2]);

    const tOpen = new state.Token("html_block", "", 0);
    tOpen.content = `<div class="callout-title">${icon(type)}<span class="callout-title-inner">`;
    const tInline = new state.Token("inline", "", 0);
    tInline.content = titleText;
    tInline.children = [];
    tInline.map = inline.map;
    const tClose = new state.Token("html_block", "", 0);
    tClose.content = "</span></div>\n";
    for (const t of [tOpen, tInline, tClose]) t.level = pOpen.level;

    if (rest.trim()) {
      inline.content = rest;
      tokens.splice(i + 1, 0, tOpen, tInline, tClose);
    } else {
      // title only: drop the now-empty first paragraph
      tokens.splice(i + 1, 3, tOpen, tInline, tClose);
    }
  }
}

// ---- tags ------------------------------------------------------------------------------
const TAG = /^#([\p{L}\p{N}_\/-]+)/u;

function tag(state, silent) {
  const pos = state.pos;
  if (state.src.charCodeAt(pos) !== 0x23 /* # */) return false;
  if (pos > 0 && !/\s/.test(state.src[pos - 1])) return false;
  const m = TAG.exec(state.src.slice(pos));
  if (!m || /^[0-9]+$/.test(m[1])) return false;
  if (!silent) {
    const t = state.push("html_inline", "", 0);
    t.content = `<span class="tag">#${state.md.utils.escapeHtml(m[1])}</span>`;
  }
  state.pos += m[0].length;
  return true;
}

// ---- highlights ------------------------------------------------------------------------
function highlight(state, silent) {
  const start = state.pos;
  const src = state.src;
  if (src.charCodeAt(start) !== 0x3d || src.charCodeAt(start + 1) !== 0x3d) return false;
  if (start + 2 >= state.posMax || /\s/.test(src[start + 2]) || src[start + 2] === "=") return false;
  const end = src.indexOf("==", start + 2);
  if (end === -1 || end > state.posMax || /\s/.test(src[end - 1])) return false;
  if (silent) return true;

  const oldMax = state.posMax;
  state.push("mark_open", "mark", 1);
  state.pos = start + 2;
  state.posMax = end;
  state.md.inline.tokenize(state);
  state.push("mark_close", "mark", -1);
  state.pos = end + 2;
  state.posMax = oldMax;
  return true;
}

function obsidian(md) {
  md.core.ruler.after("normalize", "novaroma-comments", (state) => {
    if (state.src.includes("%%")) state.src = stripComments(state.src);
  });
  md.core.ruler.after("block", "novaroma-callouts", callouts);
  md.inline.ruler.before("emphasis", "novaroma-highlight", highlight);
  md.inline.ruler.before("emphasis", "novaroma-tag", tag);
  return md;
}

module.exports = { obsidian, stripComments };
