# Szymon's personal site

Local implementation in progress. Zola, Markdown, HTML templates and plain CSS.
No frontend package manager, backend, database, analytics or third-party fonts.

Nothing is deployed. `https://example.invalid` is deliberately a placeholder.
The About copy is provisional and needs Szymon's review before publication.

## Run locally

From this directory:

```sh
./scripts/site preview
```

Open <http://127.0.0.1:1111/prototype/?variant=C&view=clean>.
The server binds to loopback only. Ctrl+C stops it. Restart with the same command.
Use `PORT=1112 ./scripts/site preview` if port 1111 is occupied.
The current review server was started in the background on port 1111. Its log
and process ID are in the ignored `.tools/preview.log` and `.tools/preview.pid`.

The design switcher compares three independent homepage layouts:

| URL parameter | Direction | Structure |
| --- | --- | --- |
| `variant=A` | Editorial | Serif-led, writing first, marginal labels |
| `variant=B` | Notebook | Left profile rail, compact writing and project lists |
| `variant=C` | Index | Small name and alias, linked indexes and tags, a pendulum experiment |

Use the bottom buttons or left/right arrow keys. Parameters survive reload and
carry through to the article specimen. C is the default, including without JS.
`appearance=light` and `appearance=dark` pin an initial theme for local review.
The real header switch clears that URL override and saves your choice locally.
Layout selection stays in the URL; the pendulum uses session storage.

C is now the preferred direction for further refinement. Open
<http://127.0.0.1:1111/prototype/?variant=C&view=clean>
to judge it without the floating development controls. Remove `view=clean` to
restore the switcher. The page and article remain unpublished draft routes.

The article specimen is at `/prototype/reading/`. It is sample copy, not an essay
ready to publish. It tests headings, code, tables, footnotes and long identifiers.

The pendulum alternates between two moods on page loads in the same tab, using
one session-storage value. With storage blocked it chooses randomly. With
JavaScript disabled it stays at "we're so back". It never animates, fetches data or
affects the site's links. `mood=over` or `mood=back` pins a state for design review.
It is currently included only in C's draft preview, not the normal build.

Other commands:

```sh
./scripts/site serve  # Normal site without draft routes, at the same local port
./scripts/site check  # Check links, build, then inspect the generated output
./scripts/site build # Build and inspect output without starting a server
```

`serve` and `preview` use `.preview/`. `build` and `check` use `public/`.
Both directories are generated and overwritten. Do not keep source material there.

## Toolchain

The wrapper requires exactly Zola **0.23.4**, recorded in `.zola-version`.
Python 3.11 or later runs the small build-output checker.

This machine has an ignored `.tools/zola` symlink to the Nix-provided binary.
No global installation or system configuration was changed.

On another machine, install that version from the
[official Zola release](https://github.com/getzola/zola/releases/tag/v0.23.4)
and put it on `PATH`, or set `ZOLA_BIN=/absolute/path/to/zola`.
The wrapper refuses a mismatched version. A portable, locked CI installation is
still part of the deployment milestone, not this design experiment.

## Where things live

```text
content/about.md              Provisional public bio
content/writing/              Published Markdown articles go here
content/software/             Full software index
data/software.toml            Ordered catalog, first two entries on the homepage
content/prototype/            Disposable design specimen, marked draft
templates/                   Normal page templates
templates/components/        Shared project list, navigation and tags, using Tera 2
templates/tags/              Tag index and per-tag article lists
templates/prototype/         Three directions and local-only controls
static/css/site.css          Reading styles and provisional notebook layout
static/css/index.css         Shared minimal layout for the actual site and C
static/js/theme.js           Small progressive light/dark switch
zola.toml                    Site metadata and generator configuration
scripts/check_output.py      Generated-output checks
scripts/check_articles.py    Temporary article fixtures for feed and draft checks
```

The normal `/` homepage uses the minimal index layout, with Szymon Głuch first
and a quieter `/ nesty` alias. Footer links name their destinations.
It shows the first two catalog entries and at most three recent articles. It has
an honest empty writing section until posts exist. `/software/`, `/writing/`, `/about/`, `/404.html`, `/atom.xml` and
`/sitemap.xml` work without JavaScript.

Appearance follows your system until you use the Light/Dark button next to Feed.
The switch remembers your choice in one local-storage value, `site-appearance`,
and matches code highlighting to it. It makes no network requests. If storage is
blocked, switching still works for the current page. Without JavaScript the button
stays hidden and the CSS follows the system. No content depends on the script.

Add a project to `data/software.toml`. Every entry appears on `/software/`; move
an entry into the first two positions to feature it on the homepage. No template
edits are needed for a third library. Tests add temporary libraries and posts to
verify the homepage caps and complete indexes without publishing fake content.

## Drafts and build boundaries

Private drafts stay **outside this repository**. `draft = true` prevents normal
publication but does not make a committed file private.

The prototype is safe to share as source. Its sample article is deliberately
marked `draft = true`. Controls, styles and scripts live in templates gated on
Zola's `serve` mode, rather than in a publicly copied static folder.

Normal output checks reject prototype paths, specimen text and all scripts except
the one local theme file. They also
check required routes, internal HTML links and anchors, XML parsing and required
feed metadata. `zola check` checks internal Markdown links before the build.

Never deploy a preview directory or use `zola build --drafts` for publication.
Upload only checked `public/` output once deployment is configured.

## Writing a real post later

Create `content/writing/a-specific-slug.md` only when the content is okay to be
public as source. Use a real publication date when ready, not a placeholder date.

```toml
+++
title = "A specific title"
description = "One sentence describing the article."
draft = true
# Add date = YYYY-MM-DD and set draft = false when ready to publish.

[taxonomies]
tags = ["rust", "language design"]
+++
```

Then write Markdown below the front matter. Local preview includes public-safe
drafts. Normal builds omit them. Set `updated = YYYY-MM-DD` for substantive later
revisions. The homepage, archive and feed use the Markdown metadata.

Tags link to static article lists at `/tags/<tag>/`, with a full index at `/tags/`.
This uses [Zola taxonomies](https://www.getzola.org/documentation/templates/taxonomies/),
not client-side filtering. Tag browsing appears once a tagged post exists. Drafts
and draft-only tags stay out of normal builds. The existing preview specimen has
two tags so the design can be reviewed without publishing a placeholder article.

## Next decisions

1. Refine C and decide whether the pendulum belongs on the finished site.
2. Promote approved remaining details to normal templates. Remove preview code from
   the launch branch and preserve the experiment on `prototype/design-directions`.
3. Review the bio and empty-homepage wording. No employer or contact email has
   been invented. Choose a source/content license before making the repo public.
4. Add pinned build and deploy workflows, choose the GitHub repository and
   configure Pages only after publication approval.
5. Set the real base URL and launch metadata. Domain purchase and DNS come later.
6. Run the remaining launch checks in `../blog-launch-plan.md`, including actual
   HTTPS, canonical redirects, social metadata, keyboard review and rollback.

This is an uncommitted local repository on `prototype/design-directions`, with no
remote. See `DESIGN-REVIEW.md` for checks and `DESIGN-REFERENCES.md` for the research.
