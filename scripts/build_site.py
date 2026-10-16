#!/usr/bin/env python3
"""Generate the YuZa Studio static site.

Legal copy for Forge Strength, CantoTalk, and Little Atlas is ported from
https://github.com/wzsgrmsz9g-png/clam-legal at 11022ca696cadcdf383b490ab1ca47581511e4f6.
Substitutions: Clam / ClamStudio → YuZa Studio, support@clam.app → support@yuzastudios.com.
CantoTalk gains one line because that app has in-app purchases: "Purchases are processed by Apple."
Forge already says purchases are processed by Apple. Receiptly and ChromaClear have no source
policy; their privacy pages do not describe data practices.

The committed HTML is the site. Run this script after editing copy, then scripts/check_site.py.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

HOST = "yuzastudios.com"
ROOT = Path(__file__).resolve().parents[1]
SITEMAP_DATE = "2026-10-15"

FORGE_WHAT = (
    "Forge Strength is a strength-training companion for iPhone and Apple Watch. "
    "Workouts, plans and progress are stored on your device. There is no Forge account "
    "and no Forge-operated server."
)
CANTO_WHAT = (
    "CantoTalk helps you practise everyday Hong Kong Cantonese on iPhone and iPad. "
    "Version 1.0 is offline: lessons, listening drills and self-recording work without "
    "an account and without contacting the network."
)
ATLAS_WHAT = (
    "Little Atlas is an offline family explorer for curated activities and nursing-room "
    "listings in Calgary. Catalog data and photos ship inside the app."
)

FORGE_PRIVACY = """
<h1>Forge Strength — Privacy Policy</h1>
<p class="meta"><strong>Effective date:</strong> 9 October 2026<br>
<strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<h2>What Forge is</h2>
<p>Forge Strength is a strength-training companion for iPhone and Apple Watch. Workouts, plans and progress are stored on your device. There is no Forge account and no Forge-operated server.</p>
<h2>Data Forge stores on your device</h2>
<ul>
<li>Workout plans, set logs, drafts, equipment preferences and weekly goals</li>
<li>Optional JSON backups you export yourself (unencrypted — store them privately)</li>
</ul>
<h2>Apple services Forge may use (with your permission)</h2>
<ul>
<li><strong>Apple Health:</strong> write completed strength workouts; optionally read Forge workouts to restore set-log history</li>
<li><strong>Apple Watch / WatchConnectivity:</strong> sync plans and completed sessions between phone and Watch</li>
<li><strong>iCloud Key-Value Storage (opt-in):</strong> sync plan <em>templates</em> only — not set logs or sensor readings</li>
</ul>
<p>Forge never uploads Health or workout data to an app-operated backend.</p>
<h2>In-app purchases</h2>
<p>Forge offers an optional one-time in-app purchase, Forge Plus. In-app purchases are processed by Apple through the App Store. No payment information (such as card details or billing address) reaches us. Whether Forge Plus is unlocked is checked on your device through Apple’s StoreKit. We do not collect or store purchase data.</p>
<h2>Tracking and ads</h2>
<p>Forge does not track you across apps or websites, does not show ads, and does not use advertising identifiers.</p>
<h2>Children’s privacy</h2>
<p>Forge is not directed at children under 13. Do not use it to collect information from children.</p>
<h2>Your choices</h2>
<ul>
<li>Deny Health access in iOS Settings at any time</li>
<li>Turn off iCloud plan sync in Forge Settings</li>
<li>Export or delete local data by restoring an empty backup or deleting the app (uninstall removes on-device Forge files; Apple Health records remain under your control)</li>
</ul>
<h2>Changes</h2>
<p>Material changes will be reflected in this document and in the App Store privacy labels.</p>
<h2>Contact</h2>
<p>Questions: use the in-app Support link or email the address above.</p>
<h2>Support</h2>
<p>See <a href="../support/">Support</a> for contact details.</p>
""".strip()

# The in-app purchases section is the only addition to the clam-legal CantoTalk policy.
CANTO_PRIVACY = """
<h1>CantoTalk — Privacy Policy</h1>
<p class="meta"><strong>Effective date:</strong> 8 October 2026<br>
<strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<h2>What CantoTalk is</h2>
<p>CantoTalk helps you practise everyday Hong Kong Cantonese on iPhone and iPad. Version 1.0 is offline: lessons, listening drills and self-recording work without an account and without contacting the network.</p>
<h2>Data on your device</h2>
<ul>
<li>Lesson completion, review progress and practice self-checks (UserDefaults)</li>
<li>Short-lived microphone recordings while you practise — stored only on this device and removed when you leave the practice screen or background the app (iOS may clean leftover temp files after an abrupt termination)</li>
</ul>
<p>CantoTalk does not collect personal data, does not create accounts, and does not upload progress or recordings.</p>
<h2>Audio and microphone</h2>
<p>Text-to-speech uses Apple’s on-device <strong>AVSpeechSynthesizer</strong>. When you tap Record, the app uses <strong>AVAudioRecorder</strong> to capture audio locally so you can listen back. Recordings stay on the device and are not uploaded. Microphone permission is requested only when you record.</p>
<h2>Network, SDKs and tracking</h2>
<p>The shipping 1.0 build does not make network calls for lessons, practice or progress. It does not include analytics, advertising or other third-party SDKs. CantoTalk does not track you across apps or websites and does not use advertising identifiers.</p>
<h2>Children</h2>
<p>Not directed at children under 13.</p>
<h2>Your choices</h2>
<ul>
<li>Deny microphone access in iOS Settings</li>
<li>Delete the app to remove on-device progress and any leftover local recordings</li>
</ul>
<h2>In-app purchases</h2>
<p>Purchases are processed by Apple.</p>
<h2>Contact</h2>
<p>Questions: use the in-app Support link or email <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a>.</p>
<h2>Support</h2>
<p>See <a href="../support/">Support</a> for contact details.</p>
""".strip()

ATLAS_PRIVACY = """
<h1>Little Atlas — Privacy Policy</h1>
<p class="meta"><strong>Effective date:</strong> 7 October 2026<br>
<strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<h2>What Little Atlas is</h2>
<p>Little Atlas is an offline family explorer for curated activities and nursing-room listings in Calgary. Catalog data and photos ship inside the app.</p>
<h2>Location</h2>
<p>When you tap <strong>Near me</strong>, the app uses Core Location (while in use) to sort places by distance. Coordinates are processed on device and are not sent to a Little Atlas server. There is no Little Atlas backend in this build.</p>
<h2>Saved lists</h2>
<p>Places you save are stored locally (UserDefaults / on-device storage).</p>
<h2>Maps handoff</h2>
<p>Opening directions may launch Apple Maps or Google Maps. Those apps apply their own privacy policies.</p>
<h2>Tracking and ads</h2>
<p>Little Atlas does not track you across apps or websites and does not show ads in this build.</p>
<h2>Children</h2>
<p>Family content is intended for parents/caregivers. The app is not designed to collect data from children.</p>
<h2>Accuracy</h2>
<p>Listings, hours and nursing-room confirmations come from sourced catalogs with review dates. They are not live availability checks. Always verify before visiting.</p>
<h2>Contact</h2>
<p>Use Support email above for privacy questions.</p>
<h2>Support</h2>
<p>See <a href="../support/">Support</a> for contact details.</p>
""".strip()

APPS = [
    {
        "slug": "forge",
        "name": "Forge Strength",
        "mark": "FS",
        "blurb": "Strength-training companion for iPhone and Apple Watch.",
        "summary": FORGE_WHAT,
        "privacy": FORGE_PRIVACY,
        "published": True,
    },
    {
        "slug": "cantotalk",
        "name": "CantoTalk",
        "mark": "CT",
        "blurb": "Practise everyday Hong Kong Cantonese on iPhone and iPad.",
        "summary": CANTO_WHAT,
        "privacy": CANTO_PRIVACY,
        "published": True,
    },
    {
        "slug": "littleatlas",
        "name": "Little Atlas",
        "mark": "LA",
        "blurb": "Offline family explorer for curated activities and nursing-room listings in Calgary.",
        "summary": ATLAS_WHAT,
        "privacy": ATLAS_PRIVACY,
        "published": True,
    },
    {
        "slug": "receiptly",
        "name": "Receiptly",
        "mark": "RC",
        "blurb": "iOS app from YuZa Studio. A product description has not been published yet.",
        "summary": "Receiptly is an iOS app from YuZa Studio.",
        "privacy": None,
        "published": False,
    },
    {
        "slug": "chromaclear",
        "name": "ChromaClear",
        "mark": "CC",
        "blurb": "iOS app from YuZa Studio. A product description has not been published yet.",
        "summary": "ChromaClear is an iOS app from YuZa Studio.",
        "privacy": None,
        "published": False,
    },
]


def load_store() -> dict:
    return json.loads((ROOT / "data" / "apps.json").read_text(encoding="utf-8"))


STORE = load_store()
STORE_BY_SLUG = {item["slug"]: item for item in STORE["apps"]}

# Real captures only. Forge files are already marketing frames, so they stay on a
# flat plate. The other shots are raw simulator screens and sit in a CSS phone.
MEDIA = {
    "forge": {
        "icon": "assets/apps/icons/forge.webp",
        "frame": "plate",
        "card_shot": 0,
        "features": [
            "Log every set with plates, reps, and a rest timer",
            "Train with the Apple Watch companion and share workouts with Apple Health",
            "Review weekly volume, reps, and workouts",
            "Follow strength trends for each lift, on your device",
        ],
        "shots": [
            {
                "src": "assets/apps/forge/01-log-every-set.webp",
                "w": 640,
                "h": 1387,
                "alt": "Forge Strength poster, Log every set. The phone shows a Pull workout with Bench Press, Lat Pulldown, and Barbell Row, including plates, reps, and a rest timer.",
            },
            {
                "src": "assets/apps/forge/02-watch-health.webp",
                "w": 640,
                "h": 1387,
                "alt": "Forge Strength poster, Apple Watch and Health. The watch shows heart-rate zones during Bench Press, and the phone shows the workout shared with Apple Health.",
            },
            {
                "src": "assets/apps/forge/03-weekly-progress.webp",
                "w": 640,
                "h": 1387,
                "alt": "Forge Strength poster, Weekly progress. A chart summarizes volume, reps, and workouts for the week of 12 October.",
            },
            {
                "src": "assets/apps/forge/04-strength-trend.webp",
                "w": 640,
                "h": 1387,
                "alt": "Forge Strength poster, Strength trend. Bench press weight is plotted rising from 135 to 185 pounds over recent weeks.",
            },
        ],
    },
    "cantotalk": {
        "icon": "assets/apps/icons/cantotalk.webp",
        "frame": "device",
        "card_shot": 0,
        "features": [
            "Practise everyday Hong Kong Cantonese with Jyutping and English",
            "Take short courses such as Café, Dim Sum, and Market",
            "Speak turns in a guided conversation",
            "Listen and practise on device. Version 1.0 stays offline",
        ],
        "shots": [
            {
                "src": "assets/apps/cantotalk/01-home.webp",
                "w": 640,
                "h": 1391,
                "alt": "CantoTalk home. Continue learning shows the Café lesson 你好, Jyutping nei5 hou2, meaning hello, and a path from Café to Dim Sum to Market.",
            },
            {
                "src": "assets/apps/cantotalk/02-courses.webp",
                "w": 640,
                "h": 1391,
                "alt": "CantoTalk courses for Café, Dim Sum, and Market, with the phrases 你好, 一位, and 幾多錢.",
            },
            {
                "src": "assets/apps/cantotalk/03-conversation.webp",
                "w": 640,
                "h": 1391,
                "alt": "CantoTalk conversation at a café register. The barista says 你好，想要啲咩？ and the line to practise is 一位，唔該.",
            },
            {
                "src": "assets/apps/cantotalk/04-conversation-complete.webp",
                "w": 640,
                "h": 1391,
                "alt": "CantoTalk marks the café conversation complete and offers another practice or the next scenario, after the line 一位，唔該.",
            },
            {
                "src": "assets/apps/cantotalk/05-practice.webp",
                "w": 640,
                "h": 1391,
                "alt": "CantoTalk practice card for 你好, Jyutping nei5 hou2, meaning hello, with a control to hear the phrase.",
            },
        ],
    },
    "littleatlas": {
        "icon": "assets/apps/icons/little-atlas.webp",
        "frame": "device",
        "card_shot": 1,
        "features": [
            "Browse curated family places in Calgary, including ages, cost, and hours",
            "Filter for indoor places, free places, and nursing rooms",
            "View places on a map",
            "Read nursing-room notes. The catalog ships inside the app",
        ],
        "shots": [
            {
                "src": "assets/apps/little-atlas/01-welcome.webp",
                "w": 640,
                "h": 1391,
                "alt": "Little Atlas welcome for Calgary. The screen offers Explore places and Saved places.",
            },
            {
                "src": "assets/apps/little-atlas/02-explore.webp",
                "w": 640,
                "h": 1391,
                "alt": "Little Atlas explore list for Calgary, with filters for indoor, free, and nursing rooms, and cards for the Central Library, Prince's Island Park, and the Calgary Zoo.",
            },
            {
                "src": "assets/apps/little-atlas/03-map.webp",
                "w": 640,
                "h": 1391,
                "alt": "Little Atlas map of Calgary with pins for the Central Library, Prince's Island Park, and the Calgary Zoo.",
            },
            {
                "src": "assets/apps/little-atlas/04-nursing-rooms.webp",
                "w": 640,
                "h": 1391,
                "alt": "Little Atlas nursing rooms list. The Central Library card mentions level 1 near the children's area and Monday to Saturday hours.",
            },
        ],
    },
    "receiptly": {
        "icon": "assets/apps/icons/receiptly.webp",
        "frame": "device",
        "card_shot": 0,
        "features": [],
        "shots": [],
    },
    "chromaclear": {
        "icon": "assets/apps/icons/chroma-clear.webp",
        "frame": "device",
        "card_shot": 3,
        "features": [
            "Play short levels on a grid of red, blue, and yellow tiles",
            "Finish a level within the moves you are given",
            "Line up tiles of the same color to build a combo",
        ],
        "shots": [
            {
                "src": "assets/apps/chroma-clear/01-combo.webp",
                "w": 552,
                "h": 1200,
                "alt": "Chroma Clear level 12 with 2 moves left and a 3-tile combo on a grid of red, blue, and yellow.",
            },
            {
                "src": "assets/apps/chroma-clear/02-amazing.webp",
                "w": 552,
                "h": 1200,
                "alt": "Chroma Clear level 12 result. The word Amazing appears over a finished grid of red, blue, and yellow tiles.",
            },
            {
                "src": "assets/apps/chroma-clear/03-unstoppable.webp",
                "w": 552,
                "h": 1200,
                "alt": "Chroma Clear level 12 result. The word Unstoppable appears over a finished grid of red, blue, and yellow tiles.",
            },
            {
                "src": "assets/apps/chroma-clear/04-level-start.webp",
                "w": 552,
                "h": 1200,
                "alt": "Chroma Clear level 12 start, with a goal of 20 tiles and a grid of red, blue, and yellow.",
            },
        ],
    },
}

HERO_SHOTS = [
    {
        "src": "assets/apps/cantotalk/01-home.webp",
        "w": 640,
        "h": 1391,
        "alt": "CantoTalk on iPhone. The home screen continues the Café lesson 你好, Jyutping nei5 hou2, meaning hello.",
        "speed": "0.045",
        "lazy": False,
        "priority": True,
        "extra": "",
    },
    {
        "src": "assets/apps/little-atlas/02-explore.webp",
        "w": 640,
        "h": 1391,
        "alt": "Little Atlas on iPhone. The Calgary explore list shows the Central Library, Prince's Island Park, and the Calgary Zoo.",
        "speed": "0.08",
        "lazy": True,
        "priority": False,
        "extra": "hero-phone-back",
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def prefix_for(depth: int, absolute: bool = False) -> str:
    if absolute:
        return "/"
    return "../" * depth


def href(prefix: str, path: str) -> str:
    if path.startswith(("mailto:", "https://", "http://", "#")):
        return path
    if path == "":
        return prefix or "./"
    return prefix + path


def store_is_live(live: bool, apple_id: str | None) -> bool:
    return bool(live) and isinstance(apple_id, str) and apple_id.isdigit()


def store_cta_from_status(
    prefix: str,
    *,
    live: bool,
    apple_id: str | None,
    badge: dict,
) -> str:
    """Official badge only for a live app with an Apple ID. Otherwise a text label and no link."""
    if store_is_live(live, apple_id):
        url = f"https://apps.apple.com/app/id{apple_id}"
        src = href(prefix, badge["src"])
        return (
            f'<a class="store-badge" href="{esc(url)}">'
            f'<img src="{esc(src)}" alt="Download on the App Store" '
            f'width="{int(badge["width"])}" height="{int(badge["height"])}" decoding="async">'
            f"</a>"
        )
    return '<p class="store-soon">Coming soon to the App Store</p>'


def store_cta(prefix: str, slug: str) -> str:
    meta = STORE_BY_SLUG[slug]
    apple_id = meta.get("appleId")
    if apple_id is not None:
        apple_id = str(apple_id)
    return store_cta_from_status(
        prefix,
        live=bool(meta.get("live")),
        apple_id=apple_id,
        badge=STORE["badge"],
    )


def icon_tag(prefix: str, slug: str, lazy: bool) -> str:
    loading = ' loading="lazy"' if lazy else ""
    src = href(prefix, MEDIA[slug]["icon"])
    return (
        f'<img class="app-icon" src="{esc(src)}" alt="" width="512" height="512"'
        f'{loading} decoding="async">'
    )


def shot_figure(prefix: str, shot: dict, frame: str, lazy: bool, priority: bool = False) -> str:
    loading = ' loading="lazy"' if lazy else ""
    fetch = ' fetchpriority="high"' if priority else ""
    src = href(prefix, shot["src"])
    return (
        f'<figure class="frame-{frame}">'
        f'<img src="{esc(src)}" alt="{esc(shot["alt"])}" width="{shot["w"]}" height="{shot["h"]}"'
        f'{loading}{fetch} decoding="async">'
        f"</figure>"
    )


def crumbs(items: list[tuple[str, str | None]]) -> str:
    parts = ['<nav aria-label="Breadcrumb">', '<ol class="crumbs">']
    for label, link in items:
        if link is None:
            parts.append(f'<li aria-current="page">{esc(label)}</li>')
        else:
            parts.append(f'<li><a href="{esc(link)}">{esc(label)}</a></li>')
    parts.append("</ol>")
    parts.append("</nav>")
    return "\n".join(parts)


def chrome(
    *,
    title: str,
    description: str,
    canonical_path: str,
    depth: int,
    current: str | None,
    body: str,
    absolute: bool = False,
    noindex: bool = False,
) -> str:
    prefix = prefix_for(depth, absolute)
    home = href(prefix, "")
    privacy = href(prefix, "privacy/")
    support = href(prefix, "support/")
    css = href(prefix, "css/site.css")
    icon = href(prefix, "favicon.svg")
    script = href(prefix, "js/site.js")

    def nav_link(label: str, link: str, key: str) -> str:
        current_attr = ' aria-current="page"' if current == key else ""
        return f'<li><a href="{esc(link)}"{current_attr}>{esc(label)}</a></li>'

    footer_links = [
        nav_link("Home", home, "home"),
        nav_link("Privacy", privacy, "privacy"),
        nav_link("Support", support, "support"),
    ]
    for app in APPS:
        footer_links.append(nav_link(app["name"], href(prefix, f"{app['slug']}/"), app["slug"]))
    footer_html = "\n          ".join(footer_links)

    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    canonical = f"https://{HOST}/{canonical_path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#f4f0e8" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#141311" media="(prefers-color-scheme: dark)">
  <title>{esc(title)}</title>
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" href="{esc(icon)}" type="image/svg+xml">{robots}
  <link rel="stylesheet" href="{esc(css)}">
  <script src="{esc(script)}" defer></script>
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <div class="stripe" aria-hidden="true"></div>
  <header class="site-header">
    <div class="wrap bar">
      <a class="wordmark" href="{esc(home)}">
        <span class="seal" aria-hidden="true"></span>
        YuZa
        <span class="studio">Studio</span>
      </a>
      <nav class="nav" aria-label="Primary">
        <ul>
          {nav_link("Home", home, "home")}
          {nav_link("Privacy", privacy, "privacy")}
          {nav_link("Support", support, "support")}
        </ul>
      </nav>
    </div>
  </header>
  <main id="content" tabindex="-1">
    <div class="wrap">
{body}
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div class="footer-id">
        <p class="footer-brand">YuZa Studio</p>
        <p><a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
        <p>This website does not use cookies or trackers.</p>
        <p class="copyright">© YuZa Studio</p>
      </div>
      <nav class="footer-nav" aria-label="Footer">
        <ul>
          {footer_html}
        </ul>
      </nav>
    </div>
  </footer>
</body>
</html>
"""


def indent(block: str, spaces: int = 6) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line else "" for line in block.strip().splitlines())


def support_article(name: str) -> str:
    return f"""
<h1>{esc(name)} — Support</h1>
<p><strong>Email:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<p>This is the public support address for all YuZa Studio apps. Please name the app in the subject line so we can help faster.</p>
<h2>Privacy</h2>
<ul>
<li><a href="../privacy/">{esc(name)} privacy</a></li>
</ul>
<p>For privacy questions, email the address above and name the app in the subject line.</p>
""".strip()


def unpublished_privacy(name: str) -> str:
    return f"""
<h1>{esc(name)} — Privacy Policy</h1>
<p class="meta"><strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<p class="notice" role="note">A product-specific privacy policy for {esc(name)} has not been published. This page does not describe how {esc(name)} handles data.</p>
<h2>Contact</h2>
<p>Questions: email <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a> and name {esc(name)} in the subject line.</p>
<h2>Support</h2>
<p>See <a href="../support/">Support</a> for contact details.</p>
""".strip()


def app_article(app: dict, prefix: str) -> str:
    media = MEDIA[app["slug"]]
    extra = ""
    if not app["published"]:
        extra = "\n        <p>A product description has not been published yet.</p>"
    hero_class = "app-hero reveal"
    shot_html = ""
    if media["shots"]:
        hero_class += " has-shot"
        shot = media["shots"][media["card_shot"]]
        shot_html = (
            '\n      <div class="parallax hero-shot" data-parallax="0.06">\n        '
            + shot_figure(prefix, shot, media["frame"], lazy=False)
            + "\n      </div>"
        )
    gallery = ""
    if media["shots"]:
        frames = "\n        ".join(
            shot_figure(prefix, shot, media["frame"], lazy=True) for shot in media["shots"]
        )
        gallery = f"""
    <section class="shot-section reveal" aria-labelledby="{esc(app["slug"])}-screens">
      <h2 id="{esc(app["slug"])}-screens">Screens</h2>
      <div class="gallery" tabindex="0" role="region" aria-label="{esc(app["name"])} screenshots">
        {frames}
      </div>
    </section>"""
    features = ""
    if media["features"]:
        items = "\n".join(f"        <li>{esc(item)}</li>" for item in media["features"])
        features = f"""
    <section class="feature-block reveal" aria-labelledby="{esc(app["slug"])}-features">
      <h2 id="{esc(app["slug"])}-features">Features</h2>
      <ul>
{items}
      </ul>
    </section>"""
    return f"""
<article class="app-page">
  <header class="{hero_class}">
    <div class="app-copy-block">
      <div class="app-intro">
        {icon_tag(prefix, app["slug"], lazy=False)}
        <div>
          <p class="kicker">iOS app</p>
          <h1>{esc(app["name"])}</h1>
        </div>
      </div>
      <p class="lede">{esc(app["summary"])}</p>{extra}
      {store_cta(prefix, app["slug"])}
    </div>{shot_html}
  </header>{gallery}{features}
  <ul class="page-links">
    <li><a href="privacy/">Privacy policy</a></li>
    <li><a href="support/">Support</a></li>
  </ul>
</article>
""".strip()


def home_card(prefix: str, app: dict, index: int) -> str:
    media = MEDIA[app["slug"]]
    shot = ""
    if media["shots"]:
        chosen = media["shots"][media["card_shot"]]
        plate = " is-plate" if media["frame"] == "plate" else ""
        shot = (
            f'\n        <div class="card-shot{plate}">'
            f'{shot_figure(prefix, chosen, media["frame"], lazy=True)}'
            f"</div>"
        )
    return f"""<li class="app-card app-{esc(app["slug"])} reveal delay-{index}">
        {icon_tag(prefix, app["slug"], lazy=True)}
        <div class="card-copy">
          <h3 class="app-name"><a class="card-link" href="{esc(href(prefix, app["slug"] + "/"))}">{esc(app["name"])}</a></h3>
          <p class="app-blurb">{esc(app["blurb"])}</p>
        </div>{shot}
        {store_cta(prefix, app["slug"])}
      </li>"""


def home_hero_stage(prefix: str) -> str:
    phones = []
    for shot in HERO_SHOTS:
        extra = f' {shot["extra"]}' if shot["extra"] else ""
        phones.append(
            f'<div class="parallax{extra}" data-parallax="{shot["speed"]}">'
            f'{shot_figure(prefix, shot, "device", lazy=shot["lazy"], priority=shot["priority"])}'
            f"</div>"
        )
    inner = "\n          ".join(phones)
    return f"""<div class="hero-stage reveal delay-1">
          {inner}
        </div>"""


def home_body(prefix: str) -> str:
    cards = "\n        ".join(home_card(prefix, app, index) for index, app in enumerate(APPS))
    return f"""
      <div class="home">
        <section class="hero">
          <div class="hero-copy reveal">
            <p class="kicker">Tiny indie studio</p>
            <h1>Small iOS apps and digital products.</h1>
            <p class="lede">YuZa Studio is a tiny indie studio. Open an app for a short introduction, its privacy page, and its support page.</p>
          </div>
          {home_hero_stage(prefix)}
        </section>
        <section class="catalog" aria-labelledby="catalog-heading">
          <h2 id="catalog-heading">Apps</h2>
          <ul class="app-list">
        {cards}
          </ul>
        </section>
        <section class="band reveal" aria-labelledby="help-heading">
          <h2 id="help-heading">Privacy and support</h2>
          <p>Email <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a> and name the app in the subject line.</p>
          <p><a href="{esc(href(prefix, "privacy/"))}">Privacy</a> · <a href="{esc(href(prefix, "support/"))}">Support page</a></p>
        </section>
      </div>
""".rstrip()


def studio_privacy(prefix: str) -> str:
    items = []
    for app in APPS:
        link = href(prefix, f"{app['slug']}/privacy/")
        note = ""
        if not app["published"]:
            note = " (a product-specific policy has not been published)"
        items.append(f'<li><a href="{esc(link)}">{esc(app["name"])}</a>{note}</li>')
    listing = "\n".join(items)
    return f"""
<h1>Privacy</h1>
<p>Public privacy policies and support information for YuZa Studio apps. Product-specific practices are described only on the app policy linked below.</p>
<h2>App policies</h2>
<ul>
{listing}
</ul>
<p>See each app’s privacy page for product-specific details.</p>
<h2>This website</h2>
<p>The pages on {HOST} are static files. They do not set cookies and do not load analytics, advertising, or other third-party scripts.</p>
<h2>Contact</h2>
<p>Email: <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<p>For privacy questions, name the app in the subject line. The <a href="{esc(href(prefix, "support/"))}">support page</a> lists the same address.</p>
""".strip()


def studio_support(prefix: str) -> str:
    items = []
    for app in APPS:
        link = href(prefix, f"{app['slug']}/privacy/")
        note = ""
        if not app["published"]:
            note = " (a product-specific policy has not been published)"
        items.append(
            f'<li><a href="{esc(link)}">{esc(app["name"])} privacy</a>{note}</li>'
        )
    listing = "\n".join(items)
    return f"""
<h1>Support</h1>
<p><strong>Email:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<p>This is the public support address for all YuZa Studio apps. Please name the app in the subject line so we can help faster.</p>
<h2>Apps</h2>
<ul>
{listing}
</ul>
<p>For privacy questions, email the address above and name the app in the subject line.</p>
""".strip()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def page_paths() -> list[str]:
    paths = ["", "privacy/", "support/"]
    for app in APPS:
        paths.append(f"{app['slug']}/")
        paths.append(f"{app['slug']}/privacy/")
        paths.append(f"{app['slug']}/support/")
    return paths


def build(dest: Path) -> None:
    home_prefix = prefix_for(0)
    write(
        dest / "index.html",
        chrome(
            title="YuZa Studio",
            description="YuZa Studio is a tiny indie studio making iOS apps and digital products.",
            canonical_path="",
            depth=0,
            current="home",
            body=home_body(home_prefix),
        ),
    )

    privacy_prefix = prefix_for(1)
    privacy_body = "\n".join(
        [
            crumbs([("Home", href(privacy_prefix, "")), ("Privacy", None)]),
            f'<article class="prose">\n{indent(studio_privacy(privacy_prefix), 2)}\n      </article>',
        ]
    )
    write(
        dest / "privacy" / "index.html",
        chrome(
            title="Privacy · YuZa Studio",
            description="Privacy policies for YuZa Studio apps, and a note about this website.",
            canonical_path="privacy/",
            depth=1,
            current="privacy",
            body=indent(privacy_body, 6),
        ),
    )

    support_prefix = prefix_for(1)
    support_body = "\n".join(
        [
            crumbs([("Home", href(support_prefix, "")), ("Support", None)]),
            f'<article class="prose">\n{indent(studio_support(support_prefix), 2)}\n      </article>',
        ]
    )
    write(
        dest / "support" / "index.html",
        chrome(
            title="Support · YuZa Studio",
            description="Support for YuZa Studio apps. Email support@yuzastudios.com.",
            canonical_path="support/",
            depth=1,
            current="support",
            body=indent(support_body, 6),
        ),
    )

    for app in APPS:
        app_prefix = prefix_for(1)
        app_body = "\n".join(
            [
                crumbs(
                    [
                        ("Home", href(app_prefix, "")),
                        (app["name"], None),
                    ]
                ),
                app_article(app, app_prefix),
            ]
        )
        write(
            dest / app["slug"] / "index.html",
            chrome(
                title=f"{app['name']} · YuZa Studio",
                description=app["summary"],
                canonical_path=f"{app['slug']}/",
                depth=1,
                current=app["slug"],
                body=indent(app_body, 6),
            ),
        )

        policy = app["privacy"] if app["published"] else unpublished_privacy(app["name"])
        privacy_depth_prefix = prefix_for(2)
        policy_body = "\n".join(
            [
                crumbs(
                    [
                        ("Home", href(privacy_depth_prefix, "")),
                        (app["name"], href(privacy_depth_prefix, f"{app['slug']}/")),
                        ("Privacy", None),
                    ]
                ),
                f'<article class="prose">\n{indent(policy, 2)}\n      </article>',
            ]
        )
        privacy_description = (
            f"Privacy policy for {app['name']}, a YuZa Studio app."
            if app["published"]
            else f"A product-specific privacy policy for {app['name']} has not been published."
        )
        write(
            dest / app["slug"] / "privacy" / "index.html",
            chrome(
                title=f"{app['name']} — Privacy Policy · YuZa Studio",
                description=privacy_description,
                canonical_path=f"{app['slug']}/privacy/",
                depth=2,
                current=None,
                body=indent(policy_body, 6),
            ),
        )

        support_depth_prefix = prefix_for(2)
        app_support = "\n".join(
            [
                crumbs(
                    [
                        ("Home", href(support_depth_prefix, "")),
                        (app["name"], href(support_depth_prefix, f"{app['slug']}/")),
                        ("Support", None),
                    ]
                ),
                f'<article class="prose">\n{indent(support_article(app["name"]), 2)}\n      </article>',
            ]
        )
        write(
            dest / app["slug"] / "support" / "index.html",
            chrome(
                title=f"{app['name']} — Support · YuZa Studio",
                description=f"Support for {app['name']}. Email support@yuzastudios.com.",
                canonical_path=f"{app['slug']}/support/",
                depth=2,
                current=None,
                body=indent(app_support, 6),
            ),
        )

    not_found = "\n".join(
        [
            '<article class="prose">',
            "  <h1>Page not found</h1>",
            "  <p>That address is not on the YuZa Studio site.</p>",
            '  <ul class="page-links">',
            '    <li><a href="/">Home</a></li>',
            '    <li><a href="/privacy/">Privacy</a></li>',
            '    <li><a href="/support/">Support</a></li>',
            "  </ul>",
            "</article>",
        ]
    )
    write(
        dest / "404.html",
        chrome(
            title="Page not found · YuZa Studio",
            description="That address is not on the YuZa Studio site.",
            canonical_path="404.html",
            depth=0,
            current=None,
            body=indent(not_found, 6),
            absolute=True,
            noindex=True,
        ),
    )

    locs = "\n".join(
        f"  <url><loc>https://{HOST}/{path}</loc><lastmod>{SITEMAP_DATE}</lastmod></url>"
        for path in page_paths()
    )
    write(
        dest / "sitemap.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{locs}
</urlset>
""",
    )
    write(
        dest / "robots.txt",
        f"""User-agent: *
Allow: /

Sitemap: https://{HOST}/sitemap.xml
""",
    )


def main() -> None:
    build(ROOT)


if __name__ == "__main__":
    main()
