#!/usr/bin/env python3
"""compliance_questionnaire.py

Print the layered intake questionnaire and emit an empty structured intake
object for web-compliance-builder. Pure stdlib, no network, no file writes
unless --out is given.

The emitted JSON object is the single source of truth that
checklist_generator.py consumes. Fill it from the answers, then pipe it in.

Usage:
    python3 compliance_questionnaire.py            # print questions + skeleton
    python3 compliance_questionnaire.py --json     # print only the skeleton JSON
    python3 compliance_questionnaire.py --out intake.json
"""
import argparse
import json
import sys

# (layer, question, affects)
QUESTIONS = [
    ("Must ask", "What are you operating: store, SaaS, app, landing page, marketplace, affiliate site, newsletter page, or a mixed model?", "core page bundle + legal taxonomy"),
    ("Must ask", "Which countries/regions do you actively target, ship to, sell to, or advertise to?", "territorial scope: privacy, cookie, consumer, accessibility"),
    ("Must ask", "Do you sell physical goods, digital goods, software access, services, subscriptions, memberships, courses, or in-app purchases?", "ToS, RR, SP, ST, app notes"),
    ("Must ask", "Do you collect personal data? Which categories: contact, account, payment, device, location, support tickets, uploaded customer data?", "PP, DPA, rights checks"),
    ("Must ask", "Do you use cookies, analytics, pixels, session replay, ad tags, or retargeting? Name tools if known.", "CP, banner, tracking matrix"),
    ("Must ask", "Is the site/app account-based? Can users create, delete, or self-serve accounts?", "deletion, retention, app-store rules"),
    ("Must ask", "Who processes payments: Shopify, Stripe, PayPal, app stores, another PSP?", "ToS, RR, ST, platform notes"),
    ("Must ask", "Do you have subscriptions, auto-renewal, free trials, or introductory pricing?", "ST, billing checklist, gating"),
    ("Must ask", "Is the product likely to be accessed by children, or directly aimed at them?", "CH, parental-consent logic, legal review"),
    ("Conditional", "Do third parties sell, list, post, review, upload, or message on the platform?", "MP, seller ToS, complaint flows"),
    ("Conditional", "Do you act as a processor for customer data, or only as controller for your own website data?", "DPA, security annex"),
    ("Conditional", "Do you use AI to generate content, answer users, score users, moderate content, or support decisions?", "AI notice, red flag report"),
    ("Conditional", "Do you collect health, biometric, employment, financial, or precise-location data?", "red flag report, legal review"),
    ("Conditional", "Are orders fulfilled from a different country than the storefront suggests?", "SP, checkout disclosures, red flag"),
    ("Conditional", "Are returns sent to a different country or supplier address?", "RR, SP, product-page checklist"),
    ("Conditional", "Do you send email and SMS marketing, and to which regions?", "marketing language, suppression ops"),
    ("High risk", "Are you making health, diagnostic, financial, hiring, or legal-effect claims?", "high-risk legal + platform review"),
    ("High risk", "Do you share data with ad platforms using enhanced matching, customer lists, or server-side events?", "CP, PP, pixel checklist, Meta/Google notes"),
    ("Must chase if unclear", "Do you rely on any 'template' pages today, and are they accurate to your actual practices?", "red flag report"),
    ("Must chase if unclear", "Are you B2C, B2B, or mixed?", "ToS, RR, DPA, app notes"),
    ("Must chase if unclear", "Are you intentionally targeting EU/UK users or simply accessible there?", "scope + lawyer triggers; if unsure assume moderate exposure, mark Needs verification"),
]

INTAKE_SKELETON = {
    "business_type": [],
    "target_regions": [],
    "transaction_types": [],
    "platforms": [],
    "data_categories": [],
    "tracking_stack": [],
    "marketing_channels": [],
    "sensitive_data_flags": [],
    "children_flag": False,
    "ugc_flag": False,
    "marketplace_flag": False,
    "processor_flag": False,
    "subscription_flag": False,
    "cross_border_fulfilment_flag": False,
    "app_distribution": [],
    "risk_level": "low",  # low | medium | high | blocking
    "mode": "build",       # build | audit
    "existing_pages": [],  # audit mode: page types the site already has, e.g. ["Privacy Policy", "Cookie Policy"]
}


def print_questions():
    current = None
    for layer, q, affects in QUESTIONS:
        if layer != current:
            print("\n=== %s ===" % layer)
            current = layer
        print("- %s" % q)
        print("    affects: %s" % affects)


def main(argv=None):
    p = argparse.ArgumentParser(description="web-compliance-builder intake questionnaire")
    p.add_argument("--json", action="store_true", help="print only the intake skeleton JSON")
    p.add_argument("--out", metavar="PATH", help="write the intake skeleton JSON to PATH")
    args = p.parse_args(argv)

    skeleton = json.dumps(INTAKE_SKELETON, indent=2, ensure_ascii=False)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(skeleton + "\n")
        print("Wrote intake skeleton to %s" % args.out, file=sys.stderr)
        return 0

    if args.json:
        print(skeleton)
        return 0

    print("web-compliance-builder — layered intake questionnaire")
    print("Ask in order. Every answer feeds the structured intake object below.")
    print_questions()
    print("\n=== structured intake skeleton (fill, then pass to checklist_generator.py) ===")
    print(skeleton)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
