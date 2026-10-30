---
name: feature-sync
description: Bring the landing page up to date with what changed in the Postvak app since the last sync. Use when the user says "feature sync", "sync the site with the app", "what's new in postvak that the site misses", or asks whether the landing page is out of date.
---

# Feature sync

The README's "Feature sync" section records the postvak-app/postvak commit the landing page last matched. This skill finds what changed in the app since then and updates `index.html` (and `style.css` if needed) to match.

## Steps

1. **Read the baseline.** Take the full SHA from the "Feature sync" section of `README.md`.
2. **List what changed in the app.**
   - `gh api repos/postvak-app/postvak/compare/<baseline>...main --jq '.commits[] | .sha[0:7] + " " + (.commit.message | split("\n")[0])'`. The compare API returns at most 250 commits; if `total_commits` is higher, page through it or work from the CHANGELOG alone.
   - Read the new entries in `CHANGELOG.md`: `gh api repos/postvak-app/postvak/contents/CHANGELOG.md --jq .content | base64 -d`.
   - For unclear changes, read the docs they touch (`docs/src/*.md`, especially `rules.md`, `mcp.md`, `cli.md`, `install.md`).
   - Note the head SHA of `main` now, so commits landing during the sync don't get skipped: `gh api repos/postvak-app/postvak/commits/main --jq .sha`.
3. **Keep only what a visitor would notice.** New or removed features, rule keys and actions, install methods, platforms, MCP scopes and tools, renamed CLI commands. Skip refactors, CI, dependency bumps and internal fixes.
4. **Check the page against them.** For each change, look for what `index.html` says about that area: the hero copy and example rule, the install tabs, the "why" cards, the sorting animation's rule chips (they use real rule keys, so check them against `docs/src/rules.schema.json`), the MCP section, the four-surfaces grid, and every `/docs/...#anchor` link.
5. **Report before editing.** List each change as: app change → what the page says now → proposed edit, or "no change needed". Flag claims the app no longer supports. Let the user pick what to apply.
6. **Apply and verify.** Edit the page, then run `pnpx html-validate@10.17.0 index.html` (the same check as CI) and look at the changed parts in the browser at desktop and phone width.
7. **Move the baseline.** Replace the SHA in the README's "Feature sync" section with the head SHA from step 2, even for changes the user chose to skip. They have been reviewed.

Commit only when the user asks, using a conventional commit such as `docs: sync landing page with postvak <short-sha>`.
