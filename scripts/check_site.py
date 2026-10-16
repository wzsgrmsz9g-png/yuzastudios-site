#!/usr/bin/env python3
"""Check the committed YuZa Studio site against the generator and the legal constraints."""

from __future__ import annotations

import importlib.util
import json
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
        self.script_srcs: list[str | None] = []
        self.iframes = 0
        self.imgs_missing_alt: list[str] = []
        self.imgs: list[dict[str, str | None]] = []
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
            self.script_srcs.append(data.get("src"))
        if tag == "iframe":
            self.iframes += 1
        if tag == "img":
            self.imgs.append(data)
            if "alt" not in data:
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


def css_variables(css: str) -> dict[str, str]:
    root = re.search(r":root \{([^}]+)\}", css)
    if not root:
        fail("CSS is missing :root color tokens")
        return {}
    if re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root \{", css):
        fail("CSS still overrides the navy palette for a second color scheme")
    if re.search(r'data-theme=', css):
        fail("CSS still switches background themes")
    return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", root.group(1)))


def check_contrast(css: str) -> None:
    tokens = css_variables(css)
    required = {
        "--bg": "#0e1420",
        "--surface": "#161d2b",
        "--section": "#12192a",
        "--ink": "#f4f7fb",
        "--muted": "#c5d0e0",
        "--accent": "#f5b82e",
        "--focus": "#9dccff",
    }
    for key, value in required.items():
        if tokens.get(key, "").lower() != value:
            fail(f"{key} is {tokens.get(key)}, expected {value}")
    pairs = [
        ("--ink", "--bg", 4.5),
        ("--ink", "--surface", 4.5),
        ("--ink", "--section", 4.5),
        ("--muted", "--bg", 4.5),
        ("--muted", "--surface", 4.5),
        ("--muted", "--section", 4.5),
        ("--accent", "--bg", 4.5),
        ("--accent", "--surface", 4.5),
        ("--accent", "--section", 4.5),
        ("--focus", "--bg", 3.0),
        ("--focus", "--surface", 3.0),
        ("--focus", "--section", 3.0),
    ]
    for fg, bg, minimum in pairs:
        if fg not in tokens or bg not in tokens:
            fail(f"missing token {fg} or {bg}")
            continue
        ratio = contrast(tokens[fg], tokens[bg])
        if ratio < minimum:
            fail(f"{fg} on {bg} contrast {ratio:.2f} < {minimum}")
    for name in ("--forge", "--canto", "--atlas", "--receipt", "--chroma"):
        if name not in tokens:
            fail(f"missing mark color {name}")
            continue
        ratio = contrast("#ffffff", tokens[name])
        if ratio < 4.5:
            fail(f"white on {name} contrast {ratio:.2f} < 4.5")
    if "#f7f4ee" not in css:
        fail("Forge marketing plates are no longer the light plate")


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
        ROOT / "favicon.ico",
        ROOT / "favicon-16.png",
        ROOT / "favicon-32.png",
        ROOT / "favicon-48.png",
        ROOT / "apple-touch-icon.png",
        ROOT / "og-image.png",
        ROOT / "svg" / "yuza-lockup-light.svg",
        ROOT / "svg" / "yuza-lockup-dark.svg",
        ROOT / "svg" / "yuza-favicon-tile.svg",
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
        if re.search(
            r"gtag|google-analytics|googletagmanager|facebook\.net|cookieconsent|document\.cookie",
            lowered,
        ):
            fail(f"{rel} includes a tracker")
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
        if parser.iframes:
            fail(f"{rel} has an iframe")
        if len(parser.script_srcs) != 1 or not (parser.script_srcs[0] or "").endswith("js/site.js"):
            fail(f"{rel} must load only js/site.js, found {parser.script_srcs}")
        elif (parser.script_srcs[0] or "").startswith(("http://", "https://", "//")):
            fail(f"{rel} loads a remote script")
        else:
            script_target = resolve_href(page, parser.script_srcs[0] or "", ROOT)
            if script_target is None or not script_target.exists():
                fail(f"{rel} missing local script {parser.script_srcs[0]}")
        if parser.imgs_missing_alt:
            fail(f"{rel} images missing alt")
        for img in parser.imgs:
            src = img.get("src") or ""
            if src.startswith(("http://", "https://", "//")):
                fail(f"{rel} remote image {src}")
            if not img.get("width") or not img.get("height"):
                fail(f"{rel} image missing width or height: {src}")
            target = resolve_href(page, src, ROOT)
            if target is not None and not target.exists():
                fail(f"{rel} missing image {src}")
            if "/icons/" not in src and "download-on-the-app-store" not in src and "yuza-lockup" not in src and src:
                alt = (img.get("alt") or "").strip()
                if len(alt) < 12:
                    fail(f"{rel} screenshot alt is too short: {src}")
        if "svg/yuza-lockup-light.svg" not in text or "svg/yuza-lockup-dark.svg" not in text:
            fail(f"{rel} missing the YuZa lockup")
        if 'property="og:image" content="https://yuzastudios.com/og-image.png"' not in text:
            fail(f"{rel} missing og:image")
        if 'name="twitter:card" content="summary_large_image"' not in text:
            fail(f"{rel} missing twitter card")
        if 'name="theme-color" content="#1B2440"' not in text:
            fail(f"{rel} missing navy theme-color")
        if re.search(r"\b(tiny|indie)\b", text, re.IGNORECASE):
            fail(f"{rel} still describes the studio as tiny or indie")
        if re.search(r"Small iOS apps", text):
            fail(f"{rel} still uses the old headline")
        if page == ROOT / "index.html":
            for bit in (
                '<p class="kicker">YuZa Studio</p>',
                "Thoughtfully crafted apps for everyday life.",
                "We design polished iPhone apps for fitness, language learning, family adventures and play. Each one is built with care and respects your privacy.",
            ):
                if bit not in text:
                    fail(f"home is missing the new positioning: {bit}")
        if "support@yuzastudios.com" not in text and page.name != "404.html":
            # 404 may still include the footer email. Require it everywhere.
            pass
        if "support@yuzastudios.com" not in text:
            fail(f"{rel} missing support email")
        for link in parser.hrefs:
            if link.lower().startswith("javascript:"):
                fail(f"{rel} has a javascript link")
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


def is_live(item: dict) -> bool:
    apple_id = item.get("appleId")
    return bool(item.get("live")) and isinstance(apple_id, str) and str(apple_id).isdigit()


def check_store(module) -> None:
    store = json.loads((ROOT / "data" / "apps.json").read_text(encoding="utf-8"))
    slugs = [item["slug"] for item in store["apps"]]
    if slugs != ["forge", "cantotalk", "littleatlas", "receiptly", "chromaclear"]:
        fail(f"apps.json slugs changed: {slugs}")
    badge_path = ROOT / store["badge"]["src"]
    if not badge_path.exists():
        fail("missing official App Store badge")
    else:
        badge = badge_path.read_text(encoding="utf-8")
        if "Download_on_the_App_Store_Badge" not in badge or "<script" in badge.lower():
            fail("App Store badge is missing its official title or contains a script")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    coming = 0
    for item in store["apps"]:
        page = (ROOT / item["slug"] / "index.html").read_text(encoding="utf-8")
        icon = {
            "forge": "icons/forge.webp",
            "cantotalk": "icons/cantotalk.webp",
            "littleatlas": "icons/little-atlas.webp",
            "receiptly": "icons/receiptly.webp",
            "chromaclear": "icons/chroma-clear.webp",
        }[item["slug"]]
        if icon not in page or icon not in home:
            fail(f"{item['slug']} icon missing from the app page or home")
        if is_live(item):
            url = f"https://apps.apple.com/app/id{item['appleId']}"
            if url not in page or "Download on the App Store" not in page:
                fail(f"{item['slug']} live badge missing")
            if "Coming soon to the App Store" in page:
                fail(f"{item['slug']} is live and still says coming soon")
        else:
            coming += 1
            if page.count("Coming soon to the App Store") < 1:
                fail(f"{item['slug']} missing coming soon label")
            if "apps.apple.com" in page:
                fail(f"{item['slug']} has a store link while it is not live")
    if home.count("Coming soon to the App Store") < coming:
        fail("home is missing a coming soon label")
    if coming == len(store["apps"]) and "apps.apple.com" in home:
        fail("home links to the App Store while no app is live")
    live_html = module.store_cta_from_status(
        "",
        live=True,
        apple_id="6816285160",
        badge=store["badge"],
    )
    if "https://apps.apple.com/app/id6816285160" not in live_html or "Download on the App Store" not in live_html:
        fail("live store helper did not emit the official badge link")
    if "Coming soon" in live_html:
        fail("live store helper still says coming soon")
    for live, apple_id in ((False, "6816285160"), (True, None)):
        quiet = module.store_cta_from_status("", live=live, apple_id=apple_id, badge=store["badge"])
        if "apps.apple.com" in quiet or "<a " in quiet or "Coming soon to the App Store" not in quiet:
            fail("unpublished store state emitted a link")


def check_motion() -> None:
    js = (ROOT / "js" / "site.js").read_text(encoding="utf-8")
    for bit in ("IntersectionObserver", "prefers-reduced-motion", "data-parallax", "requestAnimationFrame"):
        if bit not in js:
            fail(f"site.js missing {bit}")
    for banned in (
        "document.cookie",
        "localStorage",
        "sessionStorage",
        "indexedDB",
        "sendBeacon",
        "fetch(",
        "XMLHttpRequest",
        "gtag",
        "https://",
        "http://",
    ):
        if banned in js:
            fail(f"site.js contains {banned}")
    css = (ROOT / "css" / "site.css").read_text(encoding="utf-8")
    for bit in (
        "prefers-reduced-motion",
        "scroll-behavior: auto",
        "html.js .reveal:not(.is-in)",
        "scroll-snap-type: x mandatory",
    ):
        if bit not in css:
            fail(f"CSS missing {bit}")
    forge = (ROOT / "forge" / "index.html").read_text(encoding="utf-8")
    if "frame-device" in forge or "frame-plate" not in forge:
        fail("Forge screenshots must sit on a plate, not inside a phone frame")
    receipt = (ROOT / "receiptly" / "index.html").read_text(encoding="utf-8")
    if "frame-device" in receipt or "frame-plate" in receipt:
        fail("Receiptly should show the icon and coming soon label only")
    canto = (ROOT / "cantotalk" / "index.html").read_text(encoding="utf-8")
    if canto.count("frame-device") < 5:
        fail("CantoTalk gallery is missing phone frames")


def main() -> int:
    module = load_builder()
    check_generated(module)
    pages = check_pages()
    check_html(pages)
    check_legal()
    check_deploy_files()
    check_store(module)
    check_motion()
    if ERRORS:
        print(f"{len(ERRORS)} check(s) failed:")
        for message in ERRORS:
            print(f"- {message}")
        return 1
    print(f"ok ({len(pages)} html pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
