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
5. **Check the screenshots.** `assets/gui_inbox_light.png`, `gui_inbox_dark.png` and `gui_rules.png` are copies of the app's `tests/snapshots/<name>.png`. Compare each blob SHA from `gh api "repos/postvak-app/postvak/contents/tests/snapshots/<name>.png?ref=<head>" --jq .sha` with `git hash-object assets/<name>.png`. For each that differs, download the new PNG (`--jq .download_url`), look at it, re-encode the AVIF beside it, and update the image's `alt` text if what it shows changed:
   ```sh
   ffmpeg -y -i gui_x.png -frames:v 1 -c:v libaom-av1 -still-picture 1 -cpu-used 4 -crf 30 \
     -pix_fmt yuv444p -color_range pc -colorspace bt709 -color_primaries bt709 -color_trc iec61966-2-1 gui_x.avif
   ```
   Decode one AVIF back to PNG and look at it: text must stay sharp. `social-preview.png` is drawn by hand; leave it unless the rule it shows stopped being valid.
6. **Report before editing.** List each change as: app change → what the page says now → proposed edit, or "no change needed". Include any screenshots that differ. Flag claims the app no longer supports. Let the user pick what to apply.
7. **Apply and verify.** Edit the page, then run `pnpx html-validate@10.17.0 index.html` (the same check as CI) and look at the changed parts in the browser at desktop and phone width.
8. **Move the baseline.** Replace the SHA in the README's "Feature sync" section with the head SHA from step 2, even for changes the user chose to skip. They have been reviewed.

Commit only when the user asks, using a conventional commit such as `docs: sync landing page with postvak <short-sha>`.
