#!/usr/bin/env python3
"""Build test articles outside the repository so fixtures cannot be published."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

from check_output import check as check_output


def check_articles(zola):
    source = Path(__file__).resolve().parent.parent
    namespace = {"a": "http://www.w3.org/2005/Atom"}

    with tempfile.TemporaryDirectory(prefix="personal-site-check-") as temporary:
        root = Path(temporary)
        for directory in ("content", "templates", "static", "data"):
            shutil.copytree(source / directory, root / directory)
        shutil.copy(source / "zola.toml", root / "zola.toml")

        # Isolate the fixtures from any future real articles.
        shutil.rmtree(root / "content/writing")
        (root / "content/writing").mkdir()
        shutil.copy(source / "content/writing/_index.md", root / "content/writing/_index.md")

        (root / "content/writing/feed-test.md").write_text('''+++
title = "Feed <escaping> & dates"
description = "Test-only article in an isolated temporary directory."
date = 2026-09-01
updated = 2026-09-10

[taxonomies]
tags = ["rust", "language design"]
+++
A paragraph with **bold** and `Option<&str>`.
''')
        (root / "content/writing/draft-test.md").write_text('''+++
title = "draft-test-sentinel"
date = 2026-09-02
draft = true

[taxonomies]
tags = ["draft-only-tag-sentinel"]
+++
draft-test-sentinel
''')

        subprocess.run([str(zola), "-r", str(root), "build"], check=True)
        feed = ET.parse(root / "public/atom.xml").getroot()
        entries = feed.findall("a:entry", namespace)
        assert len(entries) == 1, "Only the published test article should be in the feed"
        assert entries[0].find("a:title", namespace).text == "Feed <escaping> & dates"
        assert entries[0].find("a:content", namespace).text.startswith("<p>")
        assert "<strong>bold</strong>" in entries[0].find("a:content", namespace).text
        assert feed.find("a:updated", namespace).text.startswith("2026-09-10")
        assert not (root / "public/writing/draft-test").exists()
        assert not (root / "public/tags/draft-only-tag-sentinel").exists()
        assert (root / "public/tags/language-design/index.html").is_file()
        check_output(root / "public")

        for path in (root / "public").rglob("*"):
            if path.is_file() and path.suffix in (".xml", ".html"):
                assert "draft-test-sentinel" not in path.read_text(), f"Draft leaked into {path}"
                assert "draft-only-tag-sentinel" not in path.read_text(), f"Draft tag leaked into {path}"

        # A larger collection must grow the indexes, not the homepage.
        with (root / "data/software.toml").open("a") as catalog:
            catalog.write('''
[[projects]]
name = "third-library-fixture"
description = "Only exists in this temporary test directory."
repository = "https://example.org/third-library"
documentation = "https://example.org/third-library/docs"
''')

        for day in (2, 3, 4):
            (root / f"content/writing/article-{day}.md").write_text(f'''+++
title = "Recent article fixture {day}"
description = "A test for the homepage selection."
date = 2026-09-0{day}

[taxonomies]
tags = ["rust"]
+++
Temporary article.
''')

        subprocess.run([str(zola), "-r", str(root), "build"], check=True)
        home = (root / "public/index.html").read_text()
        software = (root / "public/software/index.html").read_text()
        writing = (root / "public/writing/index.html").read_text()
        assert "third-library-fixture" in software
        assert "third-library-fixture" not in home
        assert home.count('class="project"') == 2
        assert home.count('class="writing-entry"') == 3
        assert writing.count('class="writing-entry"') == 4

        rust = (root / "public/tags/rust/index.html").read_text()
        language = (root / "public/tags/language-design/index.html").read_text()
        assert rust.count('class="writing-entry"') == 4
        assert language.count('class="writing-entry"') == 1
        assert "Recent article fixture" not in language
        assert 'rel="tag"' in home and 'rel="tag"' in writing
        check_output(root / "public")

    print("Content checks passed: feeds, draft/tag exclusion, filtered tag archives and homepage limits.")


if __name__ == "__main__":
    check_articles(Path(sys.argv[1]).resolve())
