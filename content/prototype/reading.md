+++
title = "What becomes possible after the trait solver?"
description = "An article layout specimen, not a published essay."
template = "prototype/reading.html"
draft = true

[taxonomies]
tags = ["rust", "language design"]
+++
The announcement of a new trait solver answers one question: what is changing inside the compiler? The question I would want to follow is a different one. Which language ideas have been waiting on that work, and what else do they need?

This is **sample copy for the design review**, not a researched account of Rust's current implementation. It is here to test how an essay reads, including references, code and longer paragraphs.

## Separate the questions

A useful article would distinguish a feature's design from its implementation. An accepted idea might still lack compiler support. A working implementation might still have unresolved language-design questions. A tracking issue is a starting point, not a complete explanation.

The article should make those distinctions explicit rather than treating every dependency as a promise. It should also attach a date to its findings. A reader arriving a year later needs to know which parts they should verify again.[^dates]

> What does this change make possible, and what does it leave unresolved?

That question is the thread to follow. Each candidate feature needs its own evidence. Const traits, new default bounds and async genericity should not be bundled into a single story just because they concern traits.

### A small example

For the layout, this ordinary Rust example tests lifetimes, generics, comments and syntax highlighting. It is not a demonstration of a new solver feature.

```rust
// The returned slice borrows from the input.
fn first_nonempty<'a>(items: &[&'a str]) -> Option<&'a str> {
    items.iter().copied().find(|item| !item.is_empty())
}

fn main() {
    let items = ["", "borrowed", "not allocated"];

    assert_eq!(first_nonempty(&items), Some("borrowed"));
}
```

Inline code, such as `Option<&str>`, should fit naturally into the sentence. A long identifier like `a_deliberately_long_identifier_for_checking_small_screen_wrapping` should not force the whole page sideways.

## What to check before publishing

The eventual essay needs primary sources and examples, not just a collection of links. This table tests the page's handling of denser material.

| Question | Evidence to look for |
| --- | --- |
| What is the proposed behaviour? | The RFC or current design document, including unresolved questions. |
| What does the compiler support? | The tracking issue, implementation PRs and a minimal example. |
| Is the solver actually a blocker? | An explicit dependency or an explanation from the implementation work. |
| What can a user rely on? | The feature's current release status and documented limitations. |

A good follow-up should also record negative results. If an appealing connection turns out not to exist, say so. That is more useful than stretching the narrative to make every idea fit.

## Leave room for corrections

The page needs a clear way to link to a section, readable footnotes, and enough space between paragraphs that a correction does not get buried. None of that calls for a comments backend. A GitHub link is enough for the first version.

Before this becomes a real post, replace the specimen with researched writing and verify every claim against the sources. There is no publication date because this is not a published article.

[^dates]: A date describes when the author checked the evidence. It does not make the evidence permanent. This footnote also tests the return link and long-form typography.
