#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


SOURCE_POLICIES = {
    "learningenglish.voanews.com": {
        "label": "VOA Learning English",
        "mode": "adaptable",
        "note": "Preferred source for moderate-difficulty educational English.",
    },
    "simple.wikipedia.org": {
        "label": "Simple English Wikipedia",
        "mode": "adaptable_with_attribution",
        "note": "Creative Commons source; preserve source URL and attribution in practice metadata.",
    },
    "theconversation.com": {
        "label": "The Conversation",
        "mode": "theme_only",
        "note": "Use title, summary, and public facts as inspiration; generate an original passage instead of rewriting the article.",
    },
    "www.bbc.com": {
        "label": "BBC",
        "mode": "theme_only",
        "note": "Use only as a topic source; do not reproduce or closely paraphrase the article.",
    },
    "www.npr.org": {
        "label": "NPR",
        "mode": "theme_only",
        "note": "Use only as a topic source; do not reproduce or closely paraphrase the article.",
    },
}

THIRD_PARTY_MARKERS = (
    "associated press",
    "reuters",
    "agence france-presse",
    "afp",
    "ap news",
)


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_stack = []
        self.in_title = False
        self.in_paragraph = False
        self.title = ""
        self.paragraphs = []
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg", "form"}:
            self.skip_stack.append(tag)
            return
        if self.skip_stack:
            return
        if tag == "title":
            self.in_title = True
            self._buffer = []
        elif tag == "p":
            self.in_paragraph = True
            self._buffer = []

    def handle_endtag(self, tag):
        if self.skip_stack:
            if self.skip_stack[-1] == tag:
                self.skip_stack.pop()
            return
        if tag == "title" and self.in_title:
            self.title = clean_text(" ".join(self._buffer))
            self.in_title = False
            self._buffer = []
        elif tag == "p" and self.in_paragraph:
            text = clean_text(" ".join(self._buffer))
            if is_useful_paragraph(text):
                self.paragraphs.append(text)
            self.in_paragraph = False
            self._buffer = []

    def handle_data(self, data):
        if self.skip_stack:
            return
        if self.in_title or self.in_paragraph:
            self._buffer.append(data)


def clean_text(value):
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def is_useful_paragraph(text):
    if len(text.split()) < 8:
        return False
    lowered = text.lower()
    boilerplate = (
        "cookie",
        "subscribe",
        "sign up",
        "all rights reserved",
        "share this",
        "download our app",
    )
    return not any(item in lowered for item in boilerplate)


def quality_warnings(title, paragraphs):
    joined = " ".join(paragraphs).lower()
    warnings = []
    if not title:
        warnings.append("missing_title")
    if len(paragraphs) < 3:
        warnings.append("few_paragraphs")
    if word_count(paragraphs) < 250:
        warnings.append("short_extracted_text")
    for marker in THIRD_PARTY_MARKERS:
        if marker in joined:
            warnings.append(f"third_party_marker:{marker}")
    return warnings


def normalize_domain(url):
    domain = urlparse(url).netloc.lower()
    if domain.startswith("www.learningenglish.voanews.com"):
        return "learningenglish.voanews.com"
    return domain


def fetch_url(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Echo-Kaoyan-English-Skill/0.1 (+educational practice)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def parse_article(raw_html):
    parser = ArticleParser()
    parser.feed(raw_html)
    return parser.title, parser.paragraphs


def word_count(paragraphs):
    return sum(len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", paragraph)) for paragraph in paragraphs)


def main():
    arg_parser = argparse.ArgumentParser(description="Fetch and extract a whitelisted source article for simulation practice.")
    arg_parser.add_argument("url", help="Source article URL.")
    arg_parser.add_argument("--html-file", help="Use a local HTML file instead of fetching the URL. Useful for tests.")
    arg_parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    args = arg_parser.parse_args()

    domain = normalize_domain(args.url)
    policy = SOURCE_POLICIES.get(domain)
    if not policy:
        allowed = ", ".join(sorted(SOURCE_POLICIES))
        raise SystemExit(f"Unsupported source domain: {domain}. Allowed domains: {allowed}")

    raw_html = Path(args.html_file).read_text(encoding="utf-8") if args.html_file else fetch_url(args.url)
    title, paragraphs = parse_article(raw_html)
    data = {
        "source_url": args.url,
        "source_domain": domain,
        "source_label": policy["label"],
        "source_mode": policy["mode"],
        "source_note": policy["note"],
        "title": title,
        "word_count": word_count(paragraphs),
        "paragraphs": paragraphs,
        "paragraph_count": len(paragraphs),
        "quality_warnings": quality_warnings(title, paragraphs),
        "agent_next_step": (
            "Adapt this article into a kaoyan-style original practice passage."
            if policy["mode"] != "theme_only"
            else "Use this only for topic inspiration and write an original kaoyan-style passage."
        ),
    }

    output = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
