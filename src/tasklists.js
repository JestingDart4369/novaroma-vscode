// Task lists for the Markdown preview, including Obsidian's alternate checkboxes.
//   - [ ] open   - [x] done   - [>] rescheduled   - [!] important   - [?] question   - [3] speech bubble …
// markdown-it plugin with no dependencies. Checkboxes are display-only.
"use strict";

const BOX = /^\[([^\]\n])\][  ]/;

// status character -> [glyph, label, colour group]
const STATUS = {
  ">": ["›", "Rescheduled", "blue"],
  "<": ["‹", "Scheduled", "blue"],
  "!": ["!", "Important", "red"],
  "-": ["–", "Cancelled", "muted"],
  "/": ["", "In progress", "amber"],
  "?": ["?", "Question", "gold"],
  "*": ["★", "Star", "gold"],
  n: ["✎", "Note", "blue"],
  l: ["⌖", "Location", "red"],
  i: ["i", "Information", "blue"],
  I: ["✦", "Idea", "gold"],
  S: ["$", "Amount", "green"],
  p: ["+", "Pro", "green"],
  c: ["−", "Con", "red"],
  b: ["⚑", "Bookmark", "amber"],
  '"': ["“", "Quote", "muted"],
  u: ["↑", "Up", "green"],
  d: ["↓", "Down", "red"],
  w: ["♛", "Win", "gold"],
  k: ["⚷", "Key", "gold"],
  f: ["✹", "Fire", "red"],
};

function esc(s) {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function marker(ch) {
  if (ch === " ") {
    return { html: '<input class="task-list-item-checkbox" type="checkbox" disabled aria-label="Open"> ', cls: "" };
  }
  if (ch === "x" || ch === "X") {
    return { html: '<input class="task-list-item-checkbox" type="checkbox" disabled checked aria-label="Done"> ', cls: " checked" };
  }
  let glyph, label, group;
  if (/[0-9]/.test(ch)) {
    [glyph, label, group] = [ch, `Speech bubble ${ch}`, "bubble"];
  } else if (STATUS[ch]) {
    [glyph, label, group] = STATUS[ch];
  } else {
    [glyph, label, group] = [ch, `Status ${ch}`, "muted"];
  }
  return {
    html: `<span class="task-icon" data-task="${esc(ch)}" data-group="${group}" role="img" aria-label="${esc(label)}">${esc(glyph)}</span> `,
    cls: ` alt status-${group}${ch === "-" ? " cancelled" : ""}`,
  };
}

function taskLists(md) {
  md.core.ruler.after("inline", "novaroma-task-lists", (state) => {
    const tokens = state.tokens;
    for (let i = 2; i < tokens.length; i++) {
      const inline = tokens[i];
      if (inline.type !== "inline") continue;
      if (tokens[i - 1].type !== "paragraph_open" || tokens[i - 2].type !== "list_item_open") continue;
      const first = inline.children && inline.children[0];
      if (!first || first.type !== "text") continue;
      const m = BOX.exec(first.content);
      if (!m) continue;

      const mk = marker(m[1]);
      first.content = first.content.slice(m[0].length);
      inline.content = inline.content.replace(BOX, "");

      const box = new state.Token("html_inline", "", 0);
      box.content = mk.html;
      inline.children.unshift(box);

      const li = tokens[i - 2];
      li.attrJoin("class", "task-list-item" + mk.cls);

      for (let j = i - 3, level = li.level - 1; j >= 0; j--) {
        const t = tokens[j];
        if ((t.type === "bullet_list_open" || t.type === "ordered_list_open") && t.level === level) {
          if (!(t.attrGet("class") || "").includes("contains-task-list")) t.attrJoin("class", "contains-task-list");
          break;
        }
      }
    }
  });
  return md;
}

module.exports = { taskLists };
