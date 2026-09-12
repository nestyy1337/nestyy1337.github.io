# Szymon's personal site

[Website](https://nestyy1337.github.io/) · [Source](https://github.com/nestyy1337/nestyy1337.github.io)

Zola, Markdown, HTML templates and plain CSS. No frontend packages, server-side
application, database, analytics or external fonts. Domain selection comes later.

## Run locally

Requirements: Zola **0.23.4**, Bash and Python 3.11 or later. Full checks also use
Node 22 or later for its built-in test runner. Node is not needed to build or serve.

On x86_64 Linux:

```sh
./scripts/install-zola
./scripts/site serve
```

The installer checks a pinned SHA-256 digest before extracting the official Zola
release into `.tools/`. It does not need sudo or change system packages. On other
platforms, install the same version from the [official release](https://github.com/getzola/zola/releases/tag/v0.23.4)
and put it on `PATH`, or set `ZOLA_BIN=/absolute/path/to/zola`.

Open <http://127.0.0.1:1111/>. The server binds to loopback only. Ctrl+C stops it.
Use `PORT=1112 ./scripts/site serve` if the port is occupied.

```sh
./scripts/site preview # Include public-safe drafts locally
./scripts/site check   # Build, check output and run content/JS tests
./scripts/site build   # Build and check deployable output only
```

`serve` and `preview` write `.preview/`. `build` and `check` write `public/`.
These are generated directories, not places to edit content.

## Edit the site

| File | Purpose |
| --- | --- |
| `content/about.md` | Bio, deliberately kept short |
| `content/writing/` | Markdown articles |
| `data/software.toml` | Ordered software catalog |
| `templates/` | Shared layouts, article/tag indexes, feed |
| `static/css/site.css` | Typography and article content |
| `static/css/layout.css` | Layout, colours and pendulum drawing |
| `static/js/theme.js` | Persistent light/dark preference |
| `static/js/pendulum.js` | Homepage joke, changes on page loads |
| `zola.toml` | Metadata, base URL and generator configuration |

The first two catalog entries appear on the homepage. `/software/` shows all of
them. The homepage shows at most three recent posts; `/writing/` shows every post.
Tags and tag browsing appear when there is tagged content. No placeholder article
is published. The original visual experiment is preserved on
[`prototype/design-directions`](https://github.com/nestyy1337/nestyy1337.github.io/tree/prototype/design-directions).

Without JavaScript, reading, navigation and tags still work. CSS follows the
system theme, the appearance button stays hidden and the pendulum is static.
With JavaScript, the theme choice uses one local-storage value and the pendulum
uses one session-storage value. Neither script sends requests or tracks visitors.

## Write and publish

Private drafts belong **outside the repository**. A draft flag does not hide a
committed file or its history from people browsing the public source.

Create `content/writing/a-specific-slug.md` when its source is okay to be public:

```toml
+++
title = "A specific title"
description = "One sentence describing the article."
date = 2026-09-12 # Replace with the actual intended publication date.
draft = true

[taxonomies]
tags = ["rust", "language design"]
+++
```

Write Markdown below the front matter. Preview it, then set `draft = false` when
ready. Keep the filename stable so edits do not change the URL. Use
`updated = YYYY-MM-DD` for substantive later revisions.

```sh
./scripts/site check
git diff
# Stage only the files you intend to publish.
git add content/writing/a-specific-slug.md
git commit -m "Publish article on a specific topic"
git push origin main
```

A successful push to `main` runs the deployment workflow. Pull requests run checks
without publishing. The [Actions page](https://github.com/nestyy1337/nestyy1337.github.io/actions/workflows/site.yml)
shows the result. Check the live article and `/atom.xml` after publication.

## Deployment and rollback

The workflow pins action revisions and verifies the Zola download. Checks cover
local links and anchors, canonical/feed URLs, draft/tag exclusion, homepage
limits, both root and subpath hosting, and the two scripts' state changes.

The build reads the actual site URL from Pages, then uploads only checked
`public/` files. Deployment has its own job and short-lived GitHub token; it does
not use a personal access token. The `github-pages` environment must allow only
the `main` branch. See [GitHub's workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Repository variable `ENABLE_PAGES=true` enables deployment. Set it to `false` to
pause new deployments. This does **not** take the existing website offline.

To undo a bad change, revert the relevant commit and push the revert:

```sh
git revert <bad-commit>
./scripts/site check
git push origin main
```

Wait for the new deployment and verify the page. Do not reset or force-push main.
For a failed infrastructure run without a code change, use **Re-run failed jobs**
in Actions. The last successful site should remain available.

## Maintenance

Review monthly Dependabot PRs for GitHub Actions. To update Zola, change
`.zola-version` and the corresponding official asset digest in `.zola-checksums`,
then run the installer and full checks. Do not change the version without its
checksum. Keep GitHub account recovery details and a local content backup safe.

When adding a domain, configure and verify it in Pages, update `base_url` in
`zola.toml` and rerun deployment. Do not add registrar credentials to this repo.
`SITE_BASE_URL=https://example.org/path ./scripts/site build` can test another URL
without changing the source configuration.

About copy can be revised later. A licence for the site code and articles has not
yet been selected; publishing the repository did not select one implicitly.
