#!/usr/bin/env python3
"""Check the committed YuZa Studio site against the generator and the legal constraints."""

from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load_builder():
    path = ROOT / "scripts" / "build_site.py"
    spec = importlib.util.spec_from_file_location("build_site", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load build_site.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rel_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = []
    for channel in channels:
        if channel <= 0.04045:
            linear.append(channel / 12.92)
        else:
            linear.append(((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    left, right = rel_luminance(a), rel_luminance(b)
    lighter, darker = max(left, right), min(left, right)
    return (lighter + 0.05) / (darker + 0.05)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.main = False
        self.skip = False
        self.lang = False
        self.scripts = 0
        self.iframes = 0
        self.imgs_missing_alt: list[str] = []
        self.hrefs: list[str] = []
        self.css: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value for key, value in attrs}
        if tag == "html" and data.get("lang") == "en":
            self.lang = True
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main = True
        if tag == "script":
            self.scripts += 1
        if tag == "iframe":
            self.iframes += 1
        if tag == "img" and "alt" not in data:
            self.imgs_missing_alt.append(str(data.get("src")))
        if tag == "a" and data.get("href"):
            self.hrefs.append(data["href"])
            classes = data.get("class") or ""
            if "skip" in classes.split():
                self.skip = True
        if tag == "link" and data.get("rel") == "stylesheet" and data.get("href"):
            self.css.append(data["href"])


def resolve_href(page: Path, href: str, root: Path) -> Path | None:
    raw = href.split("#", 1)[0]
    if raw == "" or raw.startswith(("mailto:", "http://", "https://")):
        return None
    if raw.startswith("/"):
        target = (root / raw.lstrip("/")).resolve()
    else:
        target = (page.parent / raw).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        fail(f"{page.relative_to(root)} links outside the site: {href}")
        return None
    if raw.endswith("/") or (target.exists() and target.is_dir()):
        target = target / "index.html"
    return target


def css_variables(css: str) -> tuple[dict[str, str], dict[str, str]]:
    root = re.search(r":root \{([^}]+)\}", css)
    dark = re.search(
        r"@media \(prefers-color-scheme: dark\) \{\s*:root \{([^}]+)\}",
        css,
    )
    if not root or not dark:
        fail("CSS is missing :root color tokens")
        return {}, {}

    def grab(block: str) -> dict[str, str]:
        return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", block))

    return grab(root.group(1)), grab(dark.group(1))


def check_contrast(css: str) -> None:
    light, dark = css_variables(css)
    pairs = [
        ("--ink", "--bg", 4.5),
        ("--muted", "--bg", 4.5),
        ("--muted", "--surface", 4.5),
        ("--accent", "--bg", 4.5),
        ("--accent", "--surface", 4.5),
        ("--focus", "--bg", 3.0),
    ]
    for theme, tokens in (("light", light), ("dark", dark)):
        for fg, bg, minimum in pairs:
            if fg not in tokens or bg not in tokens:
                fail(f"missing {theme} token {fg} or {bg}")
                continue
            ratio = contrast(tokens[fg], tokens[bg])
            if ratio < minimum:
                fail(f"{theme} {fg} on {bg} contrast {ratio:.2f} < {minimum}")
    for name in ("--forge", "--canto", "--atlas", "--receipt", "--chroma"):
        if name not in light:
            fail(f"missing mark color {name}")
            continue
        ratio = contrast("#ffffff", light[name])
        if ratio < 4.5:
            fail(f"white on {name} contrast {ratio:.2f} < 4.5")


def check_generated(module) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        module.build(dest)
        for path in sorted(p for p in dest.rglob("*") if p.is_file()):
            rel = path.relative_to(dest)
            committed = ROOT / rel
            if not committed.exists():
                fail(f"generator output missing from repo: {rel}")
                continue
            if path.read_bytes() != committed.read_bytes():
                fail(f"committed file differs from generator: {rel}")


def check_pages() -> list[Path]:
    slugs = ["forge", "cantotalk", "littleatlas", "receiptly", "chromaclear"]
    expected = [
        ROOT / "index.html",
        ROOT / "404.html",
        ROOT / "privacy" / "index.html",
        ROOT / "support" / "index.html",
        ROOT / "CNAME",
        ROOT / "css" / "site.css",
        ROOT / "favicon.svg",
        ROOT / ".nojekyll",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / ".github" / "workflows" / "pages.yml",
    ]
    for slug in slugs:
        expected.append(ROOT / slug / "index.html")
        expected.append(ROOT / slug / "privacy" / "index.html")
        expected.append(ROOT / slug / "support" / "index.html")
    pages = []
    for path in expected:
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")
        elif path.suffix == ".html":
            pages.append(path)
    return pages


def check_html(pages: list[Path]) -> None:
    for page in pages:
        text = page.read_text(encoding="utf-8")
        rel = str(page.relative_to(ROOT))
        lowered = text.lower()
        if "<!doctype html>" not in lowered:
            fail(f"{rel} missing doctype")
        if 'charset="utf-8"' not in lowered:
            fail(f"{rel} missing charset")
        if 'name="viewport"' not in lowered:
            fail(f"{rel} missing viewport")
        if re.search(r"\bclam\b", text, re.IGNORECASE):
            fail(f"{rel} still mentions Clam")
        if "clam.app" in lowered or "clamstudio" in lowered:
            fail(f"{rel} still uses the old brand contact")
        if re.search(r"<script|gtag|google-analytics|googletagmanager|facebook\.net|cookieconsent", lowered):
            fail(f"{rel} includes a tracker or script")
        parser = PageParser()
        parser.feed(text)
        if not parser.lang:
            fail(f"{rel} missing lang=en")
        if parser.h1 != 1:
            fail(f"{rel} has {parser.h1} h1 elements")
        if not parser.main:
            fail(f"{rel} missing main")
        if not parser.skip:
            fail(f"{rel} missing skip link")
        if parser.scripts or parser.iframes:
            fail(f"{rel} has script or iframe tags")
        if parser.imgs_missing_alt:
            fail(f"{rel} images missing alt")
        if "support@yuzastudios.com" not in text and page.name != "404.html":
            # 404 may still include the footer email. Require it everywhere.
            pass
        if "support@yuzastudios.com" not in text:
            fail(f"{rel} missing support email")
        for link in parser.hrefs:
            target = resolve_href(page, link, ROOT)
            if target is not None and not target.exists():
                fail(f"{rel} broken link {link} -> {target}")
        for link in parser.css:
            target = resolve_href(page, link, ROOT)
            if target is None or not target.exists():
                fail(f"{rel} missing stylesheet {link}")


def check_legal() -> None:
    forge = (ROOT / "forge" / "privacy" / "index.html").read_text(encoding="utf-8")
    canto = (ROOT / "cantotalk" / "privacy" / "index.html").read_text(encoding="utf-8")
    atlas = (ROOT / "littleatlas" / "privacy" / "index.html").read_text(encoding="utf-8")
    receipt = (ROOT / "receiptly" / "privacy" / "index.html").read_text(encoding="utf-8")
    chroma = (ROOT / "chromaclear" / "privacy" / "index.html").read_text(encoding="utf-8")
    support = (ROOT / "support" / "index.html").read_text(encoding="utf-8")

    forge_bits = [
        "Effective date:</strong> 9 October 2026",
        "Workout plans, set logs, drafts, equipment preferences and weekly goals",
        "Optional JSON backups you export yourself (unencrypted — store them privately)",
        "sync plan <em>templates</em> only — not set logs or sensor readings",
        "Forge Plus",
        "Apple’s StoreKit",
        "In-app purchases are processed by Apple through the App Store.",
        "does not use advertising identifiers",
        "Forge is not directed at children under 13.",
        "Apple Health records remain under your control",
    ]
    canto_bits = [
        "Effective date:</strong> 8 October 2026",
        "practise everyday Hong Kong Cantonese",
        "AVSpeechSynthesizer",
        "AVAudioRecorder",
        "Not directed at children under 13.",
        "Purchases are processed by Apple.",
        "does not upload progress or recordings",
    ]
    atlas_bits = [
        "Effective date:</strong> 7 October 2026",
        "nursing-room listings in Calgary",
        "Core Location (while in use)",
        "Apple Maps or Google Maps",
        "The app is not designed to collect data from children.",
        "Always verify before visiting.",
    ]
    for label, text, bits in (
        ("forge", forge, forge_bits),
        ("cantotalk", canto, canto_bits),
        ("littleatlas", atlas, atlas_bits),
    ):
        for bit in bits:
            if bit not in text:
                fail(f"{label} privacy missing ported text: {bit}")

    if "processed by Apple" in atlas or "in-app purchase" in atlas.lower():
        fail("Little Atlas privacy gained purchase language")
    for label, text in (("receiptly", receipt), ("chromaclear", chroma)):
        if "has not been published" not in text or "does not describe" not in text:
            fail(f"{label} privacy should say a policy has not been published")
        if "processed by Apple" in text or "we do not collect" in text.lower():
            fail(f"{label} privacy invents a data-practice claim")
    support_bits = [
        "support@yuzastudios.com",
        "This is the public support address for all YuZa Studio apps.",
        "Please name the app in the subject line so we can help faster.",
        "For privacy questions, email the address above and name the app in the subject line.",
        "Forge Strength privacy",
        "Little Atlas privacy",
        "CantoTalk privacy",
        "Receiptly privacy",
        "ChromaClear privacy",
    ]
    for bit in support_bits:
        if bit not in support:
            fail(f"studio support missing: {bit}")


def check_deploy_files() -> None:
    cname = (ROOT / "CNAME").read_text(encoding="utf-8")
    if cname != "yuzastudios.com\n":
        fail(f"CNAME must be exactly yuzastudios.com, got {cname!r}")
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    for bit in (
        'branches: ["main"]',
        "actions/upload-pages-artifact@v3",
        "actions/deploy-pages@v5",
        "github-pages",
    ):
        if bit not in workflow:
            fail(f"workflow missing {bit}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for bit in (
        "185.199.108.153",
        "185.199.109.153",
        "185.199.110.153",
        "185.199.111.153",
        "wzsgrmsz9g-png.github.io",
        "TODO",
        "Legal review",
        "support@yuzastudios.com",
        "yuzastudios.com",
    ):
        if bit not in readme:
            fail(f"README missing {bit}")
    css = (ROOT / "css" / "site.css").read_text(encoding="utf-8")
    for font in (
        "../fonts/newsreader-latin-500.woff2",
        "../fonts/newsreader-latin-600.woff2",
        "../fonts/atkinson-hyperlegible-latin-400.woff2",
        "../fonts/atkinson-hyperlegible-latin-700.woff2",
    ):
        if font not in css:
            fail(f"CSS missing {font}")
        if not (ROOT / "css" / font).resolve().exists():
            # resolve relative to css file
            pass
        font_path = (ROOT / "css" / font).resolve()
        if not font_path.exists():
            fail(f"missing font file {font}")
    if re.search(r"https?://", css):
        fail("CSS loads a remote URL")
    check_contrast(css)
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for path in (
        "https://yuzastudios.com/",
        "https://yuzastudios.com/forge/privacy/",
        "https://yuzastudios.com/cantotalk/support/",
        "https://yuzastudios.com/littleatlas/",
        "https://yuzastudios.com/receiptly/privacy/",
        "https://yuzastudios.com/chromaclear/support/",
        "https://yuzastudios.com/privacy/",
        "https://yuzastudios.com/support/",
    ):
        if path not in sitemap:
            fail(f"sitemap missing {path}")


def main() -> int:
    module = load_builder()
    check_generated(module)
    pages = check_pages()
    check_html(pages)
    check_legal()
    check_deploy_files()
    if ERRORS:
        print(f"{len(ERRORS)} check(s) failed:")
        for message in ERRORS:
            print(f"- {message}")
        return 1
    print(f"ok ({len(pages)} html pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
