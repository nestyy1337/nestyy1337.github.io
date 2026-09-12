#!/usr/bin/env python3
"""Small build-output checks, independent of the throwaway design variations."""

from html.parser import HTMLParser
from datetime import datetime
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.scripts = []
        self.inline_script = False
        self.in_script = False
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.add(attrs["id"])

        if tag == "script":
            self.scripts.append(attrs.get("src"))
            self.in_script = True

        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_script and data.strip():
            self.inline_script = True


def check(root):
    failures = []
    required = ("index.html", "about/index.html", "software/index.html", "writing/index.html", "404.html", "atom.xml", "sitemap.xml", "giallo-light.css", "giallo-dark.css", "js/theme.js")
    for name in required:
        if not (root / name).is_file():
            failures.append(f"Missing {name}")

    documents = {path: Document(path.read_text()) for path in root.rglob("*.html")}
    for path, document in documents.items():
        if document.scripts != ["https://example.invalid/js/theme.js"] or document.inline_script:
            failures.append(f"Unexpected production script in {path}")

        for link in document.links:
            url = urlsplit(link)
            if url.scheme in ("mailto", "tel") or url.netloc not in ("", "example.invalid"):
                continue

            target = root / unquote(url.path).lstrip("/") if url.path.startswith("/") else path.parent / unquote(url.path)
            if not url.path:
                target = path
            elif target.is_dir():
                target /= "index.html"

            if not target.exists():
                failures.append(f"Broken local link in {path}: {link}")
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                failures.append(f"Missing anchor in {path}: {link}")

    forbidden = ("prototype-controls", "What becomes possible after the trait solver?", "/prototype/", "content/prototype")
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if "prototype" in path.relative_to(root).parts:
            failures.append(f"Prototype file leaked: {path}")

        if path.suffix in (".html", ".xml", ".css", ".js"):
            content = path.read_text()
            for marker in forbidden:
                if marker in content:
                    failures.append(f"Prototype marker {marker!r} leaked into {path}")

    for name in ("atom.xml", "sitemap.xml"):
        if (root / name).is_file():
            ET.parse(root / name)

    if (root / "atom.xml").is_file():
        feed = ET.parse(root / "atom.xml").getroot()
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        for name in ("title", "id", "updated", "author"):
            if feed.find(f"atom:{name}", namespace) is None:
                failures.append(f"Atom feed is missing {name}")

        updated = feed.find("atom:updated", namespace)
        if updated is not None:
            datetime.fromisoformat(updated.text)

    if failures:
        sys.exit("\n".join(failures))

    print(f"Output checks passed: {len(documents)} HTML pages, local links, XML, theme script only, no prototype content.")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
