---
name: feature-sync
description: Bring the landing page up to date with the Postvak app. Reviews what changed in postvak-app/postvak since the commit recorded in README.md, updates index.html and the screenshots in assets/, and moves the recorded commit forward. Use when the user says "/feature-sync", "sync the site with the app" or "update the landing page for new features".
---

# Feature sync

The landing page describes postvak-app/postvak as of the commit in README.md's "Feature sync" section. This skill moves the page, and that commit, forward to the app's current `main`.

## 1. See what changed

Get the app repo (a sibling checkout, or clone `postvak-app/postvak`) and fetch `main`. Then, with `B` the commit from README.md:

```sh
git log --oneline B..origin/main
git diff --stat B origin/main -- docs/src tests/snapshots
```

If the range is empty, say the page is already current and stop.

Read each commit's message (`git show -s --format=%B`): the PR bodies say what changed for users. Skip commits that change only docs for contributors, CI or internal tooling.

## 2. Check the page against the changes

Read `index.html` and check every claim against the app at `origin/main`, not against memory. Look for:

- **Claims that became false.** The closing line says Postvak "does not send" mail; the MCP section names the default scopes; the install tabs name commands; the hero shows rule keys and CLI commands. Check each against `docs/src/` and `rules.schema.json`.
- **Features worth a line.** Add copy only for what changes how someone sees Postvak (a new surface, a new kind of rule action, a new install route). The page is about rules you write, not a feature list: GUI details belong in the docs.
- **Links** into `/docs/…` whose page or anchor was renamed.

Write copy the way the page does: short, concrete, no marketing adjectives.

## 3. Screenshots

The images in `assets/` are copies of the app's GUI test snapshots:

| Site file | App snapshot |
| --- | --- |
| `assets/gui_inbox_light.png` | `tests/snapshots/gui_inbox_light.png` |
| `assets/gui_inbox_dark.png` | `tests/snapshots/gui_inbox_dark.png` |
| `assets/gui_rules.png` | `tests/snapshots/gui_rules.png` |

Compare hashes; for each that differs, copy the snapshot from `origin/main` (`git show origin/main:tests/snapshots/<name>.png`), look at it, and re-encode the AVIF next to it:

```sh
ffmpeg -y -i gui_x.png -frames:v 1 -c:v libaom-av1 -still-picture 1 -cpu-used 4 -crf 30 \
  -pix_fmt yuv444p -color_range pc -colorspace bt709 -color_primaries bt709 -color_trc iec61966-2-1 gui_x.avif
```

Decode one AVIF back to PNG and look at it: text must stay sharp. Update an image's `alt` text if what it shows changed. `social-preview.png` is drawn by hand; leave it unless the rule it shows stopped being valid.

## 4. Record and ship

- Set the commit in README.md to the full hash of the app's `origin/main` you reviewed.
- If `index.html` changed, validate it as CI does: `npx html-validate@10.17.0 index.html`. Check it in a browser at desktop and 375px width with no horizontal scroll.
- Commit with a message that names the app commit and lists what changed on the page, and what you checked but left alone and why.
