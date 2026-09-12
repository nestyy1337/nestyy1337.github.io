# Design and implementation decisions

Szymon accepted the minimal index layout on 12 September 2026. About will be
rewritten later; the current copy was approved for initial publication.

- Small full name first, with `/ nesty` as a quieter alias. No large name hero.
- Software engineering and cybersecurity as the topic line.
- Two selected libraries and up to three recent posts, with links to full indexes.
- Article tags link to static filtered archives.
- Light/dark control beside Feed. Persistent underlined external footer links.
- A small, still pendulum joke on the homepage. No continuous animation.
- System fonts and local assets. No framework, tracking, comments or contact form.

The discarded designs, sample article and research are preserved in commit
`528df06` on `prototype/design-directions`. They are absent from the launch tree
and from deployable output. The local prototype can be reopened in a separate
worktree if needed, without restoring it to main.

## Checks

- Zola version and downloaded release checksum are pinned.
- Generated links, anchors, canonical URLs, feed and sitemap are checked.
- Temporary fixtures test tags, feeds, draft exclusion and homepage selection.
- Root-domain and subpath builds are tested, including deliberately broken links.
- Theme and pendulum logic have dependency-free Node regression tests.
- Desktop and narrow-mobile layouts were inspected during design review.

## Follow-ups

- Rewrite About and publish the first real article when ready.
- Choose separate licensing terms for the code and written content.
- Select a domain later.
- Complete a screen-reader and real browser-zoom audit with a long real article.
