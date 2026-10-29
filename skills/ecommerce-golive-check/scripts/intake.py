#!/usr/bin/env python3
"""ecommerce-golive-check — intake questionnaire.

Prints the ecommerce-specific pre-launch questionnaire and emits an empty
structured intake object (JSON) to fill. Superset of web-compliance-builder's
intake, adding payment / webhook / fulfilment fields. The filled object is the
single source of truth fed to gate.py.

Usage:
    python3 intake.py            # print questions + empty intake JSON
    python3 intake.py --json     # emit only the empty intake JSON (for piping)
"""
from __future__ import annotations

import argparse
import json
import sys

QUESTIONNAIRE = [
    ("Store", [
        "Store name and public URL?",
        "Business model: own-stock / dropshipping / digital goods / subscription / marketplace / cross-border?",
        "Target markets (countries) — drives GDPR vs CCPA vs PIPEDA etc.?",
        "Release commit / tag being gated?",
    ]),
    ("Payment", [
        "Payment provider(s)? Hosted checkout or embedded?",
        "Currencies, tax handling, shipping cost rules?",
        "Is there a refund path? Automated or manual?",
    ]),
    ("Orders & webhooks", [
        "Does a webhook drive order state? Which events (order_created, payment_succeeded)?",
        "Is the webhook signature verified?",
    ]),
    ("Data & tracking", [
        "Cookies, analytics, ad pixels, third-party SDKs in use?",
        "Consent mechanism (banner / CMP)? Does anything fire before consent?",
    ]),
    ("Fulfilment & returns", [
        "Who ships, from where? Where do returns go?",
        "Subscription / recurring billing?",
    ]),
    ("Content & i18n", [
        "Which locales? Is meta localized per locale?",
        "Which pages are customer-facing and must pass CRO + responsive checks?",
    ]),
]

EMPTY_INTAKE = {
    "store": {
        "name": "",
        "url": "",
        "model": "",            # own-stock | dropshipping | digital | subscription | marketplace | cross-border
        "markets": [],           # ISO country codes
        "release_commit": "",
    },
    "payment": {
        "providers": [],
        "hosted_checkout": None,  # bool
        "currencies": [],
        "tax_handling": "",
        "shipping_rules": "",
        "refund_path": "",        # automated | manual | none
    },
    "webhook": {
        "drives_order_state": None,  # bool
        "events": [],                # e.g. order_created, payment_succeeded
        "signature_verified": None,  # bool
    },
    "data": {
        "cookies": None,             # bool
        "analytics": [],
        "ad_pixels": [],
        "third_party_sdks": [],
        "consent_mechanism": "",
        "fires_before_consent": None,  # bool — if true, Blocking
    },
    "fulfilment": {
        "ships_from": "",
        "returns_to": "",
        "subscription": None,        # bool
    },
    "content": {
        "locales": [],
        "meta_localized_per_locale": None,  # bool
        "customer_facing_pages": [],
    },
    # Filled by the conductor after running each block; consumed by gate.py.
    "blocks": [],
    "waivers": [],
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true",
                    help="emit only the empty intake JSON")
    args = ap.parse_args()

    if not args.json:
        print("# ecommerce-golive-check — intake questionnaire\n")
        print("Answer these, then fill the intake JSON below. It is the single")
        print("source of truth for every downstream block and the gate.\n")
        for section, questions in QUESTIONNAIRE:
            print(f"## {section}")
            for q in questions:
                print(f"- {q}")
            print()
        print("## Empty intake object (fill and feed to gate.py)\n")

    print(json.dumps(EMPTY_INTAKE, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
