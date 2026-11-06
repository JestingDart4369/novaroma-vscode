// GitHub-style task lists for the Markdown preview:  - [ ] open   - [x] done
// markdown-it plugin with no dependencies. Checkboxes are display-only (disabled).
"use strict";

const BOX = /^\[([ xX])\][  ]/;

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

      const checked = m[1] !== " ";
      first.content = first.content.slice(m[0].length);
      inline.content = inline.content.replace(BOX, "");

      const box = new state.Token("html_inline", "", 0);
      box.content =
        `<input class="task-list-item-checkbox" type="checkbox" disabled` +
        `${checked ? " checked" : ""} aria-label="${checked ? "Done" : "Open"}"> `;
      inline.children.unshift(box);

      const li = tokens[i - 2];
      li.attrJoin("class", checked ? "task-list-item checked" : "task-list-item");

      // mark the surrounding list
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
