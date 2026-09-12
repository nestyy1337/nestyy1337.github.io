# Design review log

12 September 2026. C is the working direction, but the design is not yet approved.

## Fourth pass, identity, tags and appearance

- Replaced the handle-only header with small `Szymon Głuch / nesty`, with the alias
  quieter than the full name. No name hero or introductory paragraph returned.
- Added a Light/Dark button beside Feed. It starts from the system preference,
  remembers an explicit choice locally and also switches the syntax stylesheet.
  This is the only script in the normal build, currently about 2.1 KB uncompressed.
- Footer links now say LinkedIn and GitHub, with persistent underlines and external
  arrows. The name already appears in the header.
- Added real tag navigation on articles and writing indexes. Taxonomy pages list
  matching articles and counts. No search library or JavaScript filter is needed.
- Tagged only the existing draft specimen. Isolated builds check published tags,
  filtering, slugged links and exclusion of draft-only tags. Empty production
  content does not create broken links to a nonexistent tag index.
- C is now also the default draft layout, so opening a tagged specimen does not
  jump back to B. The old comparison directions remain available in the switcher.
- Verified actual theme clicks and persistence between preview, tag and About
  routes. Inspected light and dark mobile layouts, including the article, and
  checked document overflow at 320px and 390px. Long code scrolls within its block.
- Exercised the theme script with a small disposable Node test: system updates,
  saved and invalid values, storage failures, URL override precedence, code colours
  and storage events. This adds no Node dependency to the site's build.
- Browser colour-scheme emulation confirmed that an explicit choice wins over
  the system, while an unset preference follows system changes. A script-blocked
  sandboxed frame confirmed CSS fallback, a hidden toggle and intact navigation.
  A full top-level no-JS accessibility check remains on the launch list.

Nothing is deployed. The earlier entries below describe the design at that pass,
including the original no-production-JavaScript policy before the theme switch.

## Third pass, indexes and one joke

- Researched six engineers' sites, with first-party links and rendered screenshots.
  See `DESIGN-REFERENCES.md`. Applied selection versus archive as a principle,
  rather than borrowing a recognisable name treatment or decorative numbering.
- Replaced the rejected glyph mark with plain `nesty`. Removed section numbering.
- Software and Writing headings now link to full indexes, with explicit browse
  links below each selection. Preview indexes preserve the design parameters.
- Added `/software/` and `data/software.toml`. The catalog's first two projects
  appear on the homepage; all appear on the full software index.
- The normal homepage shows up to three recent articles. Its archive is still
  honestly empty. Only draft preview routes show the existing specimen.
- Shared the minimal layout across the actual homepage, About and full indexes,
  so following a link no longer jumps back to the rejected profile-rail design.
- Tried a small SVG pendulum below the content. A session-storage value alternates
  its state on page loads in the same tab. Blocked storage falls back to random;
  blocked JS leaves a static drawing. No animation, network dependency or tracking.
- The pendulum remains a local design experiment. It is not in normal build output.
- Tested three libraries and four posts in an isolated temporary directory. Full
  indexes grow; homepage remains two libraries and three posts. No fake fixture
  content enters the actual source catalog or published content.
- Clicked both section links and return navigation in the browser. Verified mood
  changes, exactly one visible pendulum arm and no running animations. Inspected
  dark mobile rendering and checked no page overflow at 320px and 390px.

No source has been pushed and nothing is deployed. The entries below describe
earlier passes, including choices that have since been rejected.

## Second pass, following Szymon's feedback

- Removed C's large name, introductory paragraph, About prompt and Warsaw label.
- Replaced the role line with the topics Software engineering and Cybersecurity.
- Moved the feed to the top-right. The actual feed remains Atom, so the visible
  link says Feed rather than claiming it is an RSS-format document.
- Removed C's specimen badge and the article's preview chrome. The sample body is
  still a draft, excluded from normal builds. It is not a published article.
- The footer name now links to Szymon's supplied LinkedIn profile.
- Tried a small `gł.` wordmark, with the letter ł in the accent colour, as the only
  decorative detail. This is an experiment, not an approved identity.
- Narrowed the layout, reduced article title sizing and kept the numbered sections.
- Added `view=clean` to hide local controls while judging the design.
- Inspected desktop, mobile light and mobile dark layouts. No page-wide overflow
  at 320px or 390px. Normal build and isolated feed/draft checks still pass.

At the end of this second pass, the normal homepage still used B provisionally.
No deployment or domain changes were made.

## Question

How should a small personal site balance a profile, existing Rust projects and
future technical writing without imitating Yoshua Wuyts's site?

The experiment compares three structurally different homepages on `/prototype/`.
All use the same real projects and clearly labelled article specimen. Article
typography, column layout and table-of-contents placement change with the variant.

## Checked

- Zola 0.23.4 checks and normal builds succeed.
- Normal output has four HTML pages, a feed, a sitemap and syntax stylesheets.
- The normal archive is empty. No articles or publication dates were invented.
- No prototype route, sample article or script appears in normal output.
- Local HTML links and anchors resolve; feed and sitemap XML parse.
- The empty Atom feed has its required author and update metadata.
- Isolated article fixtures check XML escaping, HTML feed content, update dates
  and draft exclusion. They caught a date-format incompatibility before launch.
- All three desktop homepages and the editorial reading layout were inspected
  in the browser. Dark mobile code styling was also inspected.
- At 320px and 390px browser widths, checked home/article layouts do not cause
  document-wide horizontal overflow. Code blocks scroll independently.
- The reading layouts still fit at 390px with text size doubled. This is a
  reflow check, not a substitute for a full browser-zoom accessibility audit.
- Article heading and footnote targets resolve.
- Prototype navigation carries the selected variant and appearance.
- The next-design button updates the layout and URL, including wrapping C to A.
- Synthetic keyboard events verify left/right cycling and that code blocks and
  inputs keep their normal arrow-key behaviour. Native host key delivery still
  needs a manual check in a regular browser.
- Stylesheets and the preview live-reload script load from loopback only.

The first screenshot attempts failed in the browser tool. Retrying in a fresh
preview session worked, so the desktop and mobile inspections above were completed.

## Before launch

- Review personal copy. The profile is provisional.
- Choose the winning layout and rewrite the throwaway pieces into normal templates.
- Test a long real article, not only the specimen.
- Test keyboard-only navigation, including arrow keys outside the preview host,
  screen-reader behaviour, print output and actual browser zoom.
- Complete a top-level browser check with JavaScript disabled. Output checks allow
  only the local progressive theme switch; reading and navigation do not need it.
- Review social sharing metadata after a real public URL is chosen.
- Configure CI, hosting, account security and rollback. None is done yet.

The current site is for local review. It is not a completed deployment.

## Design accepted

Szymon accepted C on 12 September 2026, with About copy still to be rewritten.
The local prototype is preserved on `prototype/design-directions`; production
cleanup continues on `main`. This commit is the reference for the visual decision.
