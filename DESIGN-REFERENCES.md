# Personal-site design references

Reviewed 12 September 2026. First-party homepages and linked indexes were read. All six homepages were also inspected in rendered browser screenshots at 1280 × 800, in a separate background tab. Themes were not normalized. The observations below distinguish page content from rendered layout. Recommendations are design judgments, not claims about the authors' intentions.

## What the sites actually do

### matklad

The homepage is a reverse-chronological list with dates, plus About, Links, and Blogroll navigation. The introduction, contact details, and résumé live on About. In the rendered homepage, large article links follow smaller dates in one centered reading column. There are no article cards or introductory hero. The nickname already supplies enough identity. Borrow the immediate access to writing and the separate About page, not the exact typography. [Homepage](https://matklad.github.io/), [About](https://matklad.github.io/about.html).

### without.boats

The homepage explicitly identifies its links as favorite posts; Posts and Tags provide other ways to browse the content. The rendered layout is left-aligned, with a compact header, a Dijkstra quotation, and a dense bulleted list. Underlined titles and adjacent dates do the organizational work. The phrase used as the site title and the chosen quotation add personality without a professional biography. This is the clearest precedent for keeping a homepage selective while making the complete collection accessible. Borrow that distinction, not the quotation or title treatment. [Homepage](https://without.boats/), [Posts](https://without.boats/blog/).

### Brandur

The homepage contains a short introduction and a small selection of recent writing with descriptions; separate sections distinguish Articles, Atoms, and Fragments. The browser also showed navigation destinations omitted by the text extraction, including Now and Uses. Visually, the small site name gives way to a restrained paragraph and then a very large personal photograph. This is useful evidence that personality can come from something outside software. The photo's scale and the many content categories are wrong for this brief. Borrow selective publishing and concrete descriptions, not a taxonomy that a small library cannot fill. [Homepage](https://brandur.org/), [Articles](https://brandur.org/articles).

### fasterthanli.me

The homepage identifies current projects separately from the latest article, and links to all articles. Four project names each have a very short explanation. The rendered page uses a bright pink header, a portrait, compact project cards, and paired video/article sections. Its expressive identity is coherent but substantially louder than the requested site. Borrow the project name plus specific purpose, and the separation of current work from the archive. Do not transplant the portrait, accent slashes, or media-heavy layout. [Homepage](https://fasterthanli.me/), [Articles](https://fasterthanli.me/articles).

### Julia Evans

The homepage starts with ten recent posts, then organizes the full writing collection by topic; Projects has its own page. The screenshot shows compact date/title rows inside a narrow white page, with orange striped decoration and a large name header. Those visual motifs are personal, but not appropriate here. Borrow the easy scanning of titles and dates. Topic indexes make sense for her large archive, not for two libraries and a handful of articles. [Homepage](https://jvns.ca/), [Projects](https://jvns.ca/projects/).

### Nicholas Nethercote

The homepage combines a short factual introduction, links to About and Publications, and a chronological post list. Rendered, it is a single mint-colored column with teal links, muted dates, and ample spacing. The ordinary-sized header and straightforward writing are sufficient identity. Borrow the unforced presentation and visible hierarchy; a long introduction is optional, not a prerequisite. [Homepage](https://nnethercote.github.io/).

## Direction for nesty

Use these principles, not a collage of recognizable decorations:

- Keep `nesty` or `sg` small. Put fuller identity and background on About. No oversized name, sales pitch, numbered section labels, or Polish-glyph monogram.
- Make Software and Writing headings real links to complete indexes, with a visible link cue. The homepage shows the two chosen libraries and only the writing that exists. Do not manufacture content to fill a layout.
- Give each library one sentence explaining what it does. Avoid badges, download counters, and large cards unless they answer an actual reader question.
- A small collection needs fewer sections, not more whitespace inflated to imply importance. Delay filters, tags, and separate notes streams until finding content becomes difficult.
- The pendulum can be the single personal oddity. Choose its state on refresh, keep it visually secondary and still while reading, and never randomize navigation or content order. Use a static fallback and respect reduced motion. The joke should remain optional to understanding the site.
