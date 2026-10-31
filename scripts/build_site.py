#!/usr/bin/env python3
"""Generate the YuZa Studio static site.

Legal copy for Forge Strength, CantoTalk, and Little Atlas is ported from
https://github.com/wzsgrmsz9g-png/clam-legal at 11022ca696cadcdf383b490ab1ca47581511e4f6.
Substitutions: Clam / ClamStudio → YuZa Studio, support@clam.app → support@yuzastudios.com.
CantoTalk 1.1 adds an In-app purchase (StoreKit) section; see the 2026-10-17 Legal review.
Forge already says purchases are processed by Apple. Receiptly's policy is the 2026-10-30 Legal
review. ChromaClear has no source policy; its privacy page does not describe data practices.

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
    "Lessons, listening drills and self-recording work offline, without an account. "
    "The full course is a one-time in-app purchase."
)
ATLAS_WHAT = (
    "Discover family-friendly places, playgrounds and nursing rooms wherever you are."
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

# CantoTalk 1.1 policy: subscriptions (Legal review 2026-10-30).
CANTO_PRIVACY = """
<h1>CantoTalk — Privacy Policy</h1>
<p>CantoTalk is published by YuZa Studio.</p>
<p class="meta"><strong>Effective date:</strong> 30 October 2026<br>
<strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<h2>What CantoTalk is</h2>
<p>CantoTalk helps you practise everyday Hong Kong Cantonese on iPhone and iPad. Lessons, listening drills and self-recording work offline, and you don’t need an account.</p>
<p>The first lesson is free. The full course is available through optional auto-renewing subscriptions sold through Apple.</p>
<p>The only network activity is Apple’s App Store system, which handles those subscriptions (see Subscriptions below).</p>
<h2>Data on your device</h2>
<ul>
<li>Lesson completion, review progress, practice self-checks and game scores.</li>
<li>Short-lived microphone recordings while you practise. These stay on this device and are removed when you leave the practice screen or send the app to the background. iOS may clean up leftover temporary files if the app closes unexpectedly.</li>
<li>Simple counters about the subscription offer screen, such as whether you’ve already seen or dismissed it, so the app doesn’t keep showing it.</li>
<li>Whether you have an active subscription. This is a cached flag; Apple’s StoreKit remains the source of truth.</li>
</ul>
<p>We do not collect personal data, create accounts, or upload progress or recordings.</p>
<h2>Audio and microphone</h2>
<p>CantoTalk speaks phrases using Apple’s on-device text-to-speech (<strong>AVSpeechSynthesizer</strong>).</p>
<p>When you tap Record, CantoTalk uses <strong>AVAudioRecorder</strong> to record audio on your device so you can listen back. It does not use speech recognition. Recordings stay on the device and are not uploaded.</p>
<p>Microphone permission is requested only when you record.</p>
<h2>Network, SDKs and tracking</h2>
<p>CantoTalk does not send your lessons, practice, progress, recordings or any other data to us or to any server we operate. Apple’s App Store system on your device communicates with Apple’s servers to show prices and to process, restore and check subscriptions.</p>
<p>CantoTalk includes no analytics, advertising or other third-party SDKs. It does not track you across apps or websites and does not use advertising identifiers.</p>
<h2>Subscriptions</h2>
<p>CantoTalk offers optional <strong>auto-renewing subscriptions</strong> that unlock the full course:</p>
<ul>
<li><strong>Monthly</strong>, renewing every month. Apple may offer a reduced price for the first month, or a one-week free trial on some offers.</li>
<li><strong>Annual</strong>, renewing every year.</li>
</ul>
<p>The price is shown in the app and on the App Store, in your local currency, before you buy.</p>
<p><strong>Apple processes the payment.</strong> You buy subscriptions through Apple’s in-app purchase system (StoreKit). Apple handles your payment method, billing, receipts, renewals and refunds under its own terms and privacy policy. We never receive your card number, billing address or other payment information.</p>
<p><strong>Renewal and cancellation.</strong> A subscription renews automatically, and your Apple Account is charged, unless you cancel at least 24 hours before the end of the current period.</p>
<ul>
<li>To manage or cancel it at any time, go to <strong>Settings › your name › Subscriptions</strong> on your iPhone or iPad, or to your Apple Account settings in the App Store.</li>
<li>If you cancel, you keep access until the end of the period you’ve paid for.</li>
<li>If you cancel during a free trial, you won’t be charged.</li>
</ul>
<p><strong>How your subscription is checked.</strong> CantoTalk uses Apple’s StoreKit to ask whether your Apple Account has an active subscription. Apple digitally signs this information, and the app checks it on your device.</p>
<ul>
<li>The app saves a small “unlocked” flag on your device so it opens quickly. This flag is not sent anywhere.</li>
<li>If a subscription ends or Apple refunds it, the full course locks again the next time the app checks. Your progress stays on your device.</li>
<li><strong>Restore Purchases</strong> asks Apple to re-sync your purchases.</li>
</ul>
<p><strong>What goes over the network.</strong> To show prices, or to start, restore or check a subscription, iOS’s App Store system communicates with Apple’s servers. That connection is between your device and Apple.</p>
<p>CantoTalk sends no purchase, payment or other data to us. We receive only the aggregated sales and subscription reports that Apple gives all developers, and these don’t identify you.</p>
<p><strong>Family Sharing.</strong> CantoTalk subscriptions are not shared through Family Sharing.</p>
<p><strong>Refunds.</strong> Apple handles refund requests at <a href="https://reportaproblem.apple.com/">reportaproblem.apple.com</a>.</p>
<p>Apple’s standard Terms of Use (EULA) apply: <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">https://www.apple.com/legal/internet-services/itunes/dev/stdeula/</a></p>
<h2>Your choices</h2>
<ul>
<li>Deny microphone access in iOS Settings.</li>
<li>Delete the app to remove your progress and any leftover recordings from your device.</li>
<li>Cancel a subscription at any time in your Apple Account settings.</li>
</ul>
<h2>Children</h2>
<p>CantoTalk is not directed at children. We don’t knowingly collect personal information from anyone, including children.</p>
<h2>Your privacy rights</h2>
<p>Depending on where you live, privacy laws may give you rights over personal data a business holds about you. Examples are the EU and UK GDPR, California’s CCPA/CPRA, Canada’s PIPEDA and Hong Kong’s PDPO.</p>
<p>CantoTalk sends no personal data to us, so we hold none about you to access, correct, delete or transfer. You can remove everything on your device by deleting the app. We do not sell or share personal information.</p>
<p>If you have a privacy question, email <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a>.</p>
<h2>Changes</h2>
<p>If we change how CantoTalk handles data, we’ll update this policy and its effective date before the change ships, and update the App Store privacy label.</p>
<h2>Contact</h2>
<p>Questions: use the in-app Support link, email <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a>, or see <a href="../support/">Support</a>.</p>
""".strip()

# Receiptly 1.0 policy v3 (effective 1 November 2026; Clam approved). Seller line names Clay Cavanagh; optional iCloud sync for Pro.
RECEIPTLY_PRIVACY = """
<h1>Receiptly — Privacy Policy</h1>
<p>Receiptly is published by YuZa Studio, the studio name of Clay Cavanagh (the App Store seller).</p>
<p class="meta"><strong>Effective date:</strong> 1 November 2026<br>
<strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<h2>The short version</h2>
<ul>
<li>Receiptly reads your receipts <strong>on your iPhone</strong>. Your receipts, photos and scanned text stay on your device.</li>
<li>If you have <strong>Receiptly Pro</strong>, you can choose to turn on <strong>iCloud sync</strong>. Your receipts and photos are then also stored in <strong>your own private iCloud</strong>, using Apple’s CloudKit. We can’t see or access that copy.</li>
<li>We <strong>do not collect</strong> any data. Receiptly has no account, no sign-in and no bank linking, and we run no server for it. iCloud sync uses your own iCloud, not a server of ours.</li>
<li>Receiptly has <strong>no analytics, no advertising and no third-party SDKs</strong>, and it <strong>does not track you</strong>.</li>
<li>Subscriptions are sold and billed by <strong>Apple</strong>. We never see your payment details.</li>
</ul>
<h2>What Receiptly is</h2>
<p>Receiptly is an iPhone app for saving and organising receipts. You can add a receipt in several ways:</p>
<ul>
<li>take a photo, or scan a document with the camera</li>
<li>pick photos</li>
<li>open a file (PDF, image or email)</li>
<li>paste text</li>
<li>share a receipt to Receiptly from another app</li>
</ul>
<p>Receiptly reads the merchant, date, total and other details, and keeps everything on your device. If you turn on iCloud sync (Pro only), it also keeps a copy in your private iCloud.</p>
<h2>How your receipts are read: on your device</h2>
<ul>
<li>Receiptly reads text with Apple’s <strong>Vision</strong> framework, Apple’s document scanner (<strong>VisionKit</strong>) and <strong>PDFKit</strong> for PDFs. All of these run on your iPhone.</li>
<li>On iOS 26 and later, where Apple’s on-device model is available, Receiptly may also use Apple’s <strong>on-device Foundation Models</strong> to help pick out receipt details. This model also runs on your iPhone.</li>
<li>Receiptly does not send your receipts to us, to Apple or to anyone else to be read.</li>
<li>Reading receipts doesn’t need an internet connection. Apart from optional iCloud sync, described below, Receiptly makes no network requests of its own.</li>
</ul>
<h2>Data stored on your device</h2>
<p>Receiptly stores the following on your iPhone, in the app’s own storage:</p>
<ul>
<li><strong>Saved receipts:</strong> the details Receiptly read (such as merchant, date, amounts, currency and category), any notes you add, the receipt image or images, and the receipt text.</li>
<li><strong>Learned categories:</strong> when you change a receipt’s category, Receiptly remembers that choice for that merchant so it can suggest it next time.</li>
<li><strong>Usage counter:</strong> how many scans you’ve used this month on the free plan.</li>
<li><strong>Subscription status:</strong> this is read from Apple’s StoreKit on your device (see Subscriptions).</li>
</ul>
<p>Nothing is sent to any server of ours. If you back up your iPhone with iCloud Backup or a computer, iOS may include Receiptly’s data in that backup. You control those backups.</p>
<h2>iCloud sync (optional, Receiptly Pro)</h2>
<p>iCloud sync is <strong>off unless you turn it on</strong>, and it’s available only with an active Receiptly Pro subscription.</p>
<ul>
<li><strong>What syncs:</strong> your saved receipts (merchant, date, amounts, currency, category, any notes you add, and the receipt text) and their photos and extra pages.</li>
<li><strong>What doesn’t sync:</strong> learned categories and your monthly free-scan count stay on each device.</li>
<li><strong>Where it goes:</strong> your <strong>own private iCloud database</strong>, through Apple’s CloudKit. It’s tied to the Apple Account you’re signed in with, and it lets your receipts appear on your other devices signed in to the same Apple Account.</li>
<li><strong>We can’t access it.</strong> YuZa Studio runs no server for sync. Data in your private iCloud database is stored by Apple for you, and we can’t read, download or delete it.</li>
<li><strong>Apple’s terms apply.</strong> Apple stores your iCloud data under its own iCloud terms and privacy policy (<a href="https://www.apple.com/legal/privacy/">https://www.apple.com/legal/privacy/</a>). Synced receipts and photos use your iCloud storage.</li>
<li><strong>Deletions sync too.</strong> While sync is on, receipts you delete in Receiptly, including with <strong>Delete all receipts</strong>, are also deleted from your iCloud and your other synced devices.</li>
<li><strong>Turning sync off, or your Pro subscription ending,</strong> stops syncing. Nothing is deleted: the receipts on your iPhone stay there, and the copy in your iCloud stays in iCloud until you remove it. If you subscribe again and turn sync back on, Receiptly picks up where it left off and merges your receipts.</li>
<li><strong>Removing your iCloud copy:</strong> in iOS go to <strong>Settings › [your name] › iCloud › Manage Storage</strong>, choose Receiptly, and delete its data. (Menu names can vary slightly between iOS versions.) Deleting the app from your iPhone doesn’t delete your iCloud copy.</li>
</ul>
<h2>Sharing receipts into Receiptly (share extension)</h2>
<p>You can share a receipt to Receiptly from other apps, for example Mail, Files, Photos or Safari. The extension accepts PDFs, images, emails, plain text and HTML. You can share up to 20 items at a time.</p>
<ul>
<li>The extension reads what you share <strong>on your device</strong>. It passes it to the Receiptly app through a private shared folder on your iPhone that only Receiptly and its extension can use.</li>
<li>After Receiptly imports the receipt, it deletes that hand-off copy.
<ul>
<li>If an import fails, or you’ve reached your monthly scan limit, the copy stays in the folder so Receiptly can try again later.</li>
<li>The copy is also deleted when you delete the receipt.</li>
</ul></li>
<li><strong>Receiptly does not open web links.</strong> If you share a web address, Receiptly does not download it. It asks you to share the receipt itself, its PDF or a screenshot.</li>
<li>Emails and documents can include personal details, such as your name, address or the last digits of a card number. These details stay on your device with the saved receipt.</li>
</ul>
<h2>Camera, photos and clipboard</h2>
<ul>
<li><strong>Camera:</strong> Receiptly asks for camera access only so you can photograph or scan receipts.</li>
<li><strong>Photos:</strong> Receiptly reads only the photos you pick.</li>
<li>You can turn off either permission at any time in iOS <strong>Settings › Receiptly</strong>. You can still add receipts in other ways.</li>
<li>Receiptly reads the clipboard only when you choose <strong>Paste</strong>.</li>
</ul>
<h2>Exports</h2>
<p>You can export receipts as a CSV file or a PDF. Exports are created on your device and go only where you send them with the iOS share sheet. Once you share an export, whoever receives it handles it under their own terms. Receiptly deletes its temporary export files when you delete receipts.</p>
<h2>Subscriptions (Receiptly Pro)</h2>
<p>Receiptly is free to use with a monthly scan limit. <strong>Receiptly Pro</strong> is an optional, auto-renewing subscription sold through Apple’s App Store in-app purchase system (StoreKit). It comes in two options:</p>
<ul>
<li><strong>Monthly</strong>, renewing every month. Apple may offer a reduced price for the first month, or a one-week free trial on some offers.</li>
<li><strong>Annual</strong>, renewing every year.</li>
</ul>
<p>The price is shown in the app and on the App Store, in your local currency, before you buy.</p>
<ul>
<li><strong>Apple processes the payment.</strong> Apple handles your payment method, billing, receipts, renewals and refunds under its own terms and privacy policy. We never receive your card number, billing address or other payment information.</li>
<li><strong>Renewal and cancellation.</strong> A subscription renews automatically, and your Apple Account is charged, unless you cancel at least 24 hours before the end of the current period.
<ul>
<li>You can manage or cancel it at any time in <strong>Settings › [your name] › Subscriptions</strong> on your iPhone, or in your Apple Account settings in the App Store.</li>
<li>If you cancel, Pro stays active until the end of the period you’ve paid for.</li>
<li>If you cancel during a free trial, you won’t be charged.</li>
</ul></li>
<li><strong>How your subscription is checked.</strong> Receiptly asks Apple’s StoreKit on your device whether your Apple Account has an active subscription. Apple signs this information, and Receiptly checks it <strong>on your device</strong>. We run no server that checks purchases.</li>
<li><strong>Restore Purchases</strong> asks Apple to re-sync your purchases.</li>
<li><strong>What goes over the network.</strong> To show prices, and to complete, restore or check a purchase, iOS’s App Store system talks to Apple’s servers. That connection is between your device and Apple. We only receive the aggregated sales reports Apple gives all developers, and these don’t identify you.</li>
<li><strong>Family Sharing.</strong> Receiptly Pro subscriptions are not shared through Family Sharing.</li>
<li><strong>Refunds</strong> are handled by Apple at <a href="https://reportaproblem.apple.com/">reportaproblem.apple.com</a>.</li>
</ul>
<p>Apple’s standard Terms of Use (EULA) apply: <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">https://www.apple.com/legal/internet-services/itunes/dev/stdeula/</a></p>
<h2>Network, SDKs and tracking</h2>
<ul>
<li>Receiptly sends no receipts, images, text, categories, usage or other data to us or to any server we operate. If you turn on iCloud sync, your receipts and images go only to your own private iCloud (see iCloud sync).</li>
<li>Receiptly includes <strong>no analytics, advertising, crash-reporting or other third-party SDKs</strong>.</li>
<li>Receiptly <strong>does not track you</strong> across apps or websites, and it doesn’t use the advertising identifier.</li>
<li>If you choose to share analytics with app developers in iOS <strong>Settings › Privacy &amp; Security › Analytics &amp; Improvements</strong>, Apple may give us crash and usage statistics. Apple controls this, and the statistics don’t identify you to us.</li>
</ul>
<h2>Ratings</h2>
<p>Receiptly may show Apple’s standard in-app rating prompt (StoreKit). Apple runs that prompt. We don’t receive your rating or any personal data through it. Receiptly has no in-app link to write a review.</p>
<h2>Deleting your data</h2>
<p>Your data is on your iPhone (and, if you turn on sync, in your own iCloud), so you control it:</p>
<ul>
<li><strong>Delete receipts</strong> in the app. This removes the saved receipt, its images and any hand-off copy.</li>
<li><strong>Settings › Delete all receipts</strong> removes every saved receipt and image, the learned categories, and Receiptly’s temporary export files from this iPhone. If iCloud sync is on, it also removes those receipts and images from your iCloud and your other synced devices. This can’t be undone.</li>
<li><strong>Settings › Forget learned categories</strong> clears only the learned categories.</li>
<li><strong>Deleting the app</strong> removes all of its data from your iPhone, but not any copy in your iCloud.</li>
<li><strong>Your iCloud copy:</strong> see "Removing your iCloud copy" under iCloud sync.</li>
</ul>
<p>While iCloud sync is on, deleting receipts in the app also deletes them from iCloud and your other synced devices.</p>
<p>Deleting receipts doesn’t reset your monthly free-scan count, which also stays on your device.</p>
<h2>Children</h2>
<p>Receiptly is designed for adults keeping track of their purchases. It is not directed at children. We don’t knowingly collect personal information from anyone, including children.</p>
<h2>Your privacy rights</h2>
<p>Depending on where you live, privacy laws such as the EU and UK GDPR, California’s CCPA/CPRA, Canada’s PIPEDA and Hong Kong’s PDPO may give you rights over personal data a business holds about you.</p>
<p>Receiptly sends no personal data to us, so we hold none about you to access, correct, delete or transfer. If you use iCloud sync, that copy is held by Apple in your own iCloud account, not by us. You can see and delete everything on your device and in your iCloud using the steps above. We do not sell or share personal information.</p>
<p>If you have a privacy question, email <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a>.</p>
<h2>Changes to this policy</h2>
<p>If we change how Receiptly handles data, we’ll update this policy and its effective date before the change ships, and update the App Store privacy label.</p>
<h2>Contact</h2>
<p>Email us at <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a>. See also <a href="https://yuzastudios.com/receiptly/support/">https://yuzastudios.com/receiptly/support/</a>.</p>
""".strip()

# The ported policy named Calgary in "nursing-room listings in Calgary."
# That city reference is now neutral. The rest of this policy is unchanged.
ATLAS_PRIVACY = """
<h1>Little Atlas — Privacy Policy</h1>
<p class="meta"><strong>Effective date:</strong> 7 October 2026<br>
<strong>Contact:</strong> <a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
<h2>What Little Atlas is</h2>
<p>Little Atlas is an offline family explorer for curated activities and nursing-room listings. Catalog data and photos ship inside the app.</p>
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
        "hide_seller_footer": True,
    },
    {
        "slug": "littleatlas",
        "name": "Little Atlas",
        "mark": "LA",
        "blurb": ATLAS_WHAT,
        "summary": ATLAS_WHAT,
        "privacy": ATLAS_PRIVACY,
        "published": True,
    },
    {
        "slug": "receiptly",
        "name": "Receiptly",
        "mark": "RC",
        "blurb": "Snap receipts and keep your spending organised.",
        "summary": "Snap receipts and keep your spending organised.",
        "privacy": RECEIPTLY_PRIVACY,
        "published": True,
        "described": True,
        "hide_seller_footer": True,
    },
    {
        "slug": "chromaclear",
        "name": "ChromaClear",
        "mark": "CC",
        "blurb": "A bright, satisfying colour-matching puzzle game.",
        "summary": "A bright, satisfying colour-matching puzzle game.",
        "privacy": None,
        "published": False,
        "described": True,
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
        "card_shot": 0,
        "features": [
            "Browse family-friendly places, playgrounds, and nursing rooms",
            "Filter for indoor places, free places, and nursing rooms",
            "View places on a map",
            "Read nursing-room notes. The catalog ships inside the app",
        ],
        "shots": [
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
        "speed": "0.2",
        "lazy": False,
        "priority": True,
        "extra": "",
    },
    {
        "src": "assets/apps/chroma-clear/04-level-start.webp",
        "w": 552,
        "h": 1200,
        "alt": "Chroma Clear on iPhone. Level 12 starts with a goal of 20 tiles on a grid of red, blue, and yellow.",
        "speed": "0.34",
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


def lockup(prefix: str) -> str:
    light = href(prefix, "svg/yuza-lockup-light.svg")
    dark = href(prefix, "svg/yuza-lockup-dark.svg")
    return (
        f'<img class="lockup lockup-light" src="{esc(light)}" alt="YuZa" width="1260" height="512">'
        f'<img class="lockup lockup-dark" src="{esc(dark)}" alt="YuZa" width="1260" height="512">'
    )


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
    seller_footer: bool = True,
) -> str:
    prefix = prefix_for(depth, absolute)
    home = href(prefix, "")
    privacy = href(prefix, "privacy/")
    support = href(prefix, "support/")
    css = href(prefix, "css/site.css")
    script = href(prefix, "js/site.js")
    icon_ico = href(prefix, "favicon.ico")
    icon_16 = href(prefix, "favicon-16.png")
    icon_32 = href(prefix, "favicon-32.png")
    icon_48 = href(prefix, "favicon-48.png")
    icon_svg = href(prefix, "svg/yuza-favicon-tile.svg")
    apple_icon = href(prefix, "apple-touch-icon.png")
    brand = lockup(prefix)
    copyright_line = (
        "© 2026 YuZa Studio. YuZa Studio is the studio name of Clay Cavanagh, the developer listed on the App Store."
        if seller_footer
        else "© 2026 YuZa Studio."
    )

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
  <meta name="theme-color" content="#1B2440">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="https://yuzastudios.com/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://yuzastudios.com/og-image.png">
  <title>{esc(title)}</title>
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" href="{esc(icon_ico)}" sizes="16x16 32x32 48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="{esc(icon_32)}">
  <link rel="icon" type="image/png" sizes="16x16" href="{esc(icon_16)}">
  <link rel="icon" type="image/png" sizes="48x48" href="{esc(icon_48)}">
  <link rel="icon" type="image/svg+xml" href="{esc(icon_svg)}">
  <link rel="apple-touch-icon" sizes="180x180" href="{esc(apple_icon)}">{robots}
  <link rel="stylesheet" href="{esc(css)}">
  <script src="{esc(script)}" defer></script>
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <div class="stripe" aria-hidden="true"></div>
  <header class="site-header">
    <div class="wrap bar">
      <a class="wordmark" href="{esc(home)}">
        {brand}
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
        <a class="footer-brand" href="{esc(home)}">{brand}</a>
        <p><a href="mailto:support@yuzastudios.com">support@yuzastudios.com</a></p>
        <p>This website does not use cookies or trackers.</p>
        <p class="copyright">{copyright_line}</p>
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
<p><strong>Phone:</strong> +1 587-858-4643 (business line)</p>
<p>YuZa Studio is the studio name of Clay Cavanagh. On the App Store, our apps are listed under the seller name “Clay Cavanagh”.</p>
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
    if not app["published"] and not app.get("described"):
        extra = "\n        <p>A product description has not been published yet.</p>"
    hero_class = "app-hero reveal"
    shot_html = ""
    if media["shots"]:
        hero_class += " has-shot"
        shot = media["shots"][media["card_shot"]]
        shot_html = (
            '\n      <div class="parallax hero-shot" data-parallax="0.18">\n        '
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
        <div class="hero-hold">
        <div class="hero-pin">
        <section class="hero">
          <div class="hero-copy reveal">
            <p class="kicker">YuZa Studio</p>
            <h1>Thoughtfully crafted apps for everyday life.</h1>
            <p class="lede">We design polished iPhone apps for fitness, language learning, family adventures and play. Each one is built with care and respects your privacy.</p>
          </div>
          {home_hero_stage(prefix)}
        </section>
        </div>
        </div>
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
<p>These policies are provided by Clay Cavanagh, operating as YuZa Studio (Alberta, Canada).</p>
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
<p><strong>Phone:</strong> +1 587-858-4643 (business line)</p>
<p>YuZa Studio is the studio name of Clay Cavanagh. On the App Store, our apps are listed under the seller name “Clay Cavanagh”.</p>
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
            description="We design polished iPhone apps for fitness, language learning, family adventures and play. Each one is built with care and respects your privacy.",
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
                seller_footer=not app.get("hide_seller_footer", False),
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
