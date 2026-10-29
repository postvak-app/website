# postvak.pataar.nl

The landing page of [Postvak](https://github.com/postvak-app/postvak): plain HTML and CSS, no build step. Open `index.html` in a browser to see it.

The site is deployed from postvak-app/postvak, whose `docs.yml` puts this repository at the root, the book from its `docs/` at `/docs/` and the Flatpak repository at `/flatpak/` (`docs/site.sh` there). A push to `main` here starts that workflow; it needs the secret `POSTVAK_DOCS_TOKEN`, a fine-grained token with Actions read/write on `postvak-app/postvak`.

Don't add `docs/`, `flatpak/` or a page named like one of the book's (`install.html`, `rules.html`, …) here: those paths belong to the docs and its redirects.

The fonts are under the SIL Open Font License (`assets/fonts/OFL-*.txt`); the screenshots are Postvak's own GUI snapshots.
