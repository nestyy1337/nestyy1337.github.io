#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.scripts = []
        self.inline_script = False
        self.in_script = False
        self.canonical = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.add(attrs["id"])

        if tag == "script":
            self.scripts.append(attrs.get("src"))
            self.in_script = True
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")

        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_script and data.strip():
            self.inline_script = True


def check_document(path, document, documents, root, base_url):
    failures = []
    relative = path.relative_to(root).as_posix()
    page_url = base_url + relative.removesuffix("index.html")
    expected_scripts = [base_url + "js/theme.js"]

    if relative == "index.html":
        expected_scripts.append(base_url + "js/pendulum.js")

    if document.scripts != expected_scripts or document.inline_script:
        failures.append(f"Unexpected or missing script in {path}")
    if relative != "404.html" and document.canonical != page_url:
        failures.append(f"Wrong canonical URL in {path}: {document.canonical}")

    base = urlsplit(base_url)
    for link in document.links:
        url = urlsplit(urljoin(page_url, link))
        if url.scheme not in ("http", "https") or url.netloc != base.netloc:
            continue
        if not unquote(url.path).startswith(unquote(base.path)):
            failures.append(f"Link escapes the site base path in {path}: {link}")
            continue

        target = (root / unquote(url.path)[len(unquote(base.path)) :]).resolve()
        if not target.is_relative_to(root):
            failures.append(f"Link escapes the output directory in {path}: {link}")
            continue
        if target.is_dir():
            target /= "index.html"

        if not target.is_file():
            failures.append(f"Broken local link in {path}: {link}")
        elif (
            url.fragment
            and target in documents
            and unquote(url.fragment) not in documents[target].ids
        ):
            failures.append(f"Missing anchor in {path}: {link}")

    return failures


def check_xml(root, base_url):
    failures = []
    namespace = {
        "a": "http://www.w3.org/2005/Atom",
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
    }
    feed = ET.parse(root / "atom.xml").getroot()
    for name in ("title", "id", "updated", "author"):
        if feed.find(f"a:{name}", namespace) is None:
            failures.append(f"Atom feed is missing {name}")

    updated = feed.find("a:updated", namespace)
    if updated is not None:
        datetime.fromisoformat(updated.text)
    urls = [node.text for node in feed.findall(".//a:id", namespace)]
    urls.extend(node.attrib["href"] for node in feed.findall(".//a:link", namespace))
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    urls.extend(node.text for node in sitemap.findall("s:url/s:loc", namespace))

    for url in urls:
        if url != base_url.rstrip("/") and not url.startswith(base_url):
            failures.append(f"Wrong base URL in feed or sitemap: {url}")
    return failures


def check(root, base_url="https://example.invalid"):
    root = root.resolve()
    base_url = base_url.rstrip("/") + "/"
    base = urlsplit(base_url)
    if (
        base.scheme not in ("http", "https")
        or not base.netloc
        or base.query
        or base.fragment
    ):
        sys.exit(f"Invalid base URL: {base_url}")

    required = (
        "index.html",
        "software/index.html",
        "writing/index.html",
        "404.html",
        "atom.xml",
        "sitemap.xml",
        "giallo-light.css",
        "giallo-dark.css",
        "js/theme.js",
        "js/pendulum.js",
    )
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        sys.exit(f"Missing output: {missing}")

    documents = {path: Document(path.read_text()) for path in root.rglob("*.html")}
    failures = []
    for path, document in documents.items():
        failures.extend(check_document(path, document, documents, root, base_url))

    forbidden = [
        "prototype-controls",
        "What becomes possible after the trait solver?",
        "/prototype/",
        "content/prototype",
        "data-variant",
        "data-design",
    ]
    if base.hostname != "example.invalid":
        forbidden.append("example.invalid")
    for path in root.rglob("*"):
        if path.is_symlink():
            failures.append(f"Symlink in deployable output: {path}")
        if not path.is_file():
            continue
        if "prototype" in path.relative_to(root).parts:
            failures.append(f"Prototype file leaked: {path}")

        if path.suffix in (".html", ".xml", ".css", ".js"):
            content = path.read_text()
            for marker in forbidden:
                if marker in content:
                    failures.append(f"Forbidden marker {marker!r} in {path}")

    failures.extend(check_xml(root, base_url))
    if failures:
        sys.exit("\n".join(failures))

    print(
        f"Output checks passed: {len(documents)} pages, local links, canonical/feed URLs, allowed scripts and no prototype content."
    )


if __name__ == "__main__":
    check(
        Path(sys.argv[1]),
        sys.argv[2] if len(sys.argv) > 2 else "https://example.invalid",
    )
