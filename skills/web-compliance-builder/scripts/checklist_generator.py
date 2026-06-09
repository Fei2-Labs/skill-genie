#!/usr/bin/env python3
"""checklist_generator.py

Transform a filled intake object (from compliance_questionnaire.py) into a
required-pages list and gating checklist rows. Deterministic; performs NO legal
interpretation of its own — it only applies the trigger rules encoded in the
skill's reference files. Pure stdlib, no network.

Usage:
    python3 checklist_generator.py intake.json
    cat intake.json | python3 checklist_generator.py -
    python3 checklist_generator.py intake.json --format md
    python3 checklist_generator.py intake.json --format json
"""
import argparse
import json
import sys

LEGAL = "Legal requirement"
PLATFORM = "Platform requirement"
BEST = "Best practice"
RISK = "Risk-based recommendation"

DISCLAIMER = (
    "This output is not legal advice. Compliance requirements vary by "
    "jurisdiction, business model, and actual operational practice. High-risk, "
    "regulated, sensitive-data, or cross-border businesses should have final "
    "materials reviewed by qualified counsel. This skill provides drafting "
    "support, issue spotting, and checklisting only."
)


def _has(values, *needles):
    """True if any needle is a case-insensitive substring of any value."""
    blob = " ".join(str(v).lower() for v in (values or []))
    return any(n.lower() in blob for n in needles)


def region_flags(intake):
    regions = intake.get("target_regions", [])
    return {
        "eu": _has(regions, "eu", "eea", "europe", "germany", "france", "spain", "italy", "netherlands"),
        "uk": _has(regions, "uk", "united kingdom", "britain", "england"),
        "us": _has(regions, "us", "usa", "united states", "america", "california"),
        "ca_state": _has(regions, "california"),
        "canada": _has(regions, "canada"),
        "au": _has(regions, "australia"),
    }


def required_pages(intake):
    """Return list of (page, class, reason)."""
    rf = region_flags(intake)
    eu_uk = rf["eu"] or rf["uk"]
    pages = []

    data = intake.get("data_categories", [])
    tracking = intake.get("tracking_stack", [])
    tx = intake.get("transaction_types", [])

    if data:
        pages.append(("Privacy Policy", LEGAL, "personal data collected"))
    if tracking:
        cls = LEGAL if eu_uk else RISK
        pages.append(("Cookie Policy + banner + consent settings", cls,
                      "non-essential cookies/pixels/analytics"))

    sells_goods = _has(tx, "physical", "goods", "product")
    if sells_goods:
        pages.append(("Terms of Service", LEGAL, "consumer sale"))
        pages.append(("Refund & Return Policy", LEGAL, "physical goods sold to consumers"))
        pages.append(("Shipping Policy", RISK, "physical goods shipped"))
    elif tx:
        pages.append(("Terms of Service", LEGAL, "service/contract terms"))

    if _has(tx, "digital", "software", "course", "download", "template", "membership"):
        pages.append(("Digital product terms / licence", LEGAL,
                      "digital goods / software licence (incl. EU/UK withdrawal waiver)"))

    if intake.get("subscription_flag") or _has(tx, "subscription", "trial", "auto-renew", "membership"):
        pages.append(("Subscription Terms", LEGAL,
                      "recurring billing / trial-to-paid (ROSCA / ARL / region)"))

    if _has(data, "account") or "account" in " ".join(str(p) for p in intake.get("platforms", [])).lower():
        pages.append(("Account deletion / data-rights section", LEGAL,
                      "accounts with personal data"))

    if intake.get("processor_flag"):
        pages.append(("DPA outline", LEGAL, "SaaS acts as processor"))

    if intake.get("ugc_flag") or intake.get("marketplace_flag"):
        pages.append(("Seller terms + moderation + complaint workflow", LEGAL,
                      "UGC / marketplace (DSA / P2B / INFORM)"))

    if intake.get("children_flag"):
        pages.append(("Children's notice / age gate / parental consent", LEGAL,
                      "child-directed or likely child-accessed"))

    if _has(intake.get("business_type", []), "ai") or _has(tracking, "ai"):
        pages.append(("AI disclosure notice", RISK,
                      "AI system or AI marketing claims"))

    if eu_uk:
        pages.append(("Accessibility Statement + WCAG remediation checklist",
                      LEGAL if rf["eu"] else RISK,
                      "EU-covered service / litigation-sensitive"))

    if intake.get("marketing_channels"):
        pages.append(("Marketing consent language", LEGAL,
                      "email/SMS marketing (CAN-SPAM / PECR / CASL / Spam Act)"))

    if intake.get("app_distribution"):
        pages.append(("App Store / Google Play compliance notes", PLATFORM,
                      "app distribution"))

    if intake.get("sensitive_data_flags"):
        pages.append(("Red-flag report + legal-review notice", RISK,
                      "high-risk / sensitive data"))

    # de-duplicate, preserve order
    seen = set()
    out = []
    for page, cls, reason in pages:
        if page not in seen:
            seen.add(page)
            out.append((page, cls, reason))
    return out


def gating_rows(intake):
    """Return blocking/high-risk gating items triggered by the facts."""
    rf = region_flags(intake)
    eu_uk = rf["eu"] or rf["uk"]
    rows = []

    def add(sev, cls, req, why, when, evidence, owner):
        rows.append({
            "severity": sev, "class": cls, "requirement": req,
            "why_it_matters": why, "applies_when": when,
            "evidence_needed": evidence, "owner": owner,
            "pass_fail_status": "Unknown",
        })

    if eu_uk and intake.get("tracking_stack"):
        add("Blocking", LEGAL,
            "Non-essential cookies/pixels must not fire before consent in EU/UK flows",
            "Unlawful tracking can invalidate consent and trigger enforcement",
            "EU/UK visitors + analytics/ads tags active",
            ["CMP config", "tag audit", "network logs", "screenshots"], "Engineering")

    if intake.get("cross_border_fulfilment_flag"):
        add("Blocking", LEGAL,
            "State shipping origin and estimated fulfilment windows clearly",
            "Hidden origin/timing is a deceptive-practice and refund-dispute pattern",
            "dropshipping / cross-border fulfilment",
            ["product page", "shipping page", "checkout copy"], "Operations")
        add("Blocking", LEGAL,
            "State return address / return country and return process clearly",
            "Hidden overseas return address drives refund disputes",
            "goods sale with overseas supplier",
            ["returns page", "support SOP"], "Operations")
        add("High risk", RISK,
            "State whether duties / VAT / customs are included or borne by the buyer",
            "Undisclosed import charges are a top complaint vector",
            "cross-border shipping",
            ["checkout copy", "shipping page"], "Operations")

    if intake.get("subscription_flag"):
        add("Blocking", LEGAL,
            "Subscription signup must clearly state what renews, frequency, price, and cancellation path with express informed consent",
            "Negative-option rules (ROSCA / ARL) require clear disclosure + easy cancel",
            "recurring billing or trial-to-paid",
            ["signup screenshots", "pricing table", "cancellation flow"], "Product")

    if intake.get("data_categories") and ("account" in " ".join(str(d).lower() for d in intake["data_categories"]) or intake.get("app_distribution")):
        add("Blocking", PLATFORM,
            "Account deletion path must exist if accounts can be created",
            "Apple/Google require a deletion path; privacy law backs data deletion",
            "account creation possible",
            ["in-app flow or web deletion page", "help article"], "Engineering")

    if intake.get("app_distribution"):
        add("Blocking", PLATFORM,
            "Privacy policy and store disclosures must match actual SDK / data practices",
            "Mismatch causes app rejection and privacy violations",
            "app distribution",
            ["SDK inventory", "app listing", "PP draft"], "Product")

    if rf["eu"] and _has(intake.get("transaction_types", []), "physical", "goods"):
        add("High risk", LEGAL,
            "Validate discount / strike-through pricing against the prior 30-day lowest price",
            "EU Omnibus requires prior-price basis for promo claims",
            "EU pricing promotions",
            ["pricing evidence file"], "Marketing")

    if intake.get("sensitive_data_flags"):
        add("High risk", RISK,
            "Escalate to legal review for sensitive-data / regulated-domain processing",
            "Health, biometric, financial, employment, precise-location data carry sector-specific risk",
            "sensitive data present",
            ["data map", "purpose justification"], "Legal")

    return rows


# Aliases so existing_pages strings can be matched to required-page names.
PAGE_ALIASES = {
    "Privacy Policy": ["privacy"],
    "Cookie Policy + banner + consent settings": ["cookie", "consent", "banner"],
    "Terms of Service": ["terms", "tos", "t&c", "conditions"],
    "Refund & Return Policy": ["refund", "return"],
    "Shipping Policy": ["shipping", "delivery"],
    "Digital product terms / licence": ["licence", "license", "eula", "digital terms"],
    "Subscription Terms": ["subscription", "billing", "auto-renew", "renewal"],
    "Account deletion / data-rights section": ["deletion", "delete account", "data rights"],
    "DPA outline": ["dpa", "data processing"],
    "Seller terms + moderation + complaint workflow": ["seller", "moderation", "complaint"],
    "Children's notice / age gate / parental consent": ["children", "kids", "age", "parental"],
    "AI disclosure notice": ["ai disclosure", "ai notice", "ai transparency"],
    "Accessibility Statement + WCAG remediation checklist": ["accessibility", "wcag"],
    "Marketing consent language": ["marketing", "unsubscribe", "opt-in", "newsletter"],
    "App Store / Google Play compliance notes": ["app store", "google play", "app privacy", "data safety"],
    "Red-flag report + legal-review notice": ["red flag", "risk"],
}


def audit_gap(intake, pages):
    """Match required pages against intake['existing_pages']; mark Present vs Missing.

    Adequacy/Mismatch grading is left to the agent (interpretation), so Present
    rows are flagged for review rather than passed.
    """
    existing = " ".join(str(e).lower() for e in intake.get("existing_pages", []))
    gap = []
    for page, cls, reason in pages:
        aliases = PAGE_ALIASES.get(page, [page.split()[0].lower()])
        present = any(a in existing for a in aliases)
        if present:
            status = "Present — review for adequacy/mismatch"
            action = "Check mandatory sections + region/platform modules; verify it matches actual practice"
        else:
            status = "Missing"
            action = "Create this page (%s)" % reason
        gap.append({"required": page, "class": cls, "status": status,
                    "finding": reason, "action": action})
    return gap


def render_audit_md(intake, gap, rows):
    out = []
    out.append("# Web Compliance — AUDIT gap report\n")
    out.append("Existing pages provided: %s\n" % (
        ", ".join(intake.get("existing_pages", [])) or "(none)"))
    out.append("## Gap report\n")
    out.append("| Required item | Class | Status | Finding | Action |")
    out.append("|---|---|---|---|---|")
    for g in gap:
        out.append("| %s | %s | %s | %s | %s |" % (
            g["required"], g["class"], g["status"], g["finding"], g["action"]))
    missing = [g for g in gap if g["status"] == "Missing"]
    out.append("\n## Remediation gate (Missing legal/platform items + Blocking findings)\n")
    blocking = [r for r in rows if r["severity"] == "Blocking"]
    if missing or blocking:
        for g in missing:
            if g["class"] in (LEGAL, PLATFORM):
                out.append("- [ ] MISSING: %s" % g["required"])
        for r in blocking:
            out.append("- [ ] %s" % r["requirement"])
    else:
        out.append("- (none from deterministic checks — still grade Present pages for Inadequate/Mismatch)")
    out.append("\n> NOTE: This script only decides Present vs Missing. Grade each "
               "Present page for **Present-Inadequate** or **Mismatch** (page contradicts "
               "actual practice = Blocking) per references/audit-workflow.md.")
    out.append("\n---\n")
    out.append("> " + DISCLAIMER)
    return "\n".join(out)


def render_md(intake, pages, rows):
    out = []
    out.append("# Web Compliance — generated requirements\n")
    out.append("## Required pages\n")
    out.append("| Page | Class | Reason |")
    out.append("|---|---|---|")
    for page, cls, reason in pages:
        out.append("| %s | %s | %s |" % (page, cls, reason))
    out.append("\n## Gating checklist\n")
    if rows:
        out.append("| Severity | Class | Requirement | Why it matters | Applies when | Evidence needed | Owner | Status |")
        out.append("|---|---|---|---|---|---|---|---|")
        for r in rows:
            out.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
                r["severity"], r["class"], r["requirement"], r["why_it_matters"],
                r["applies_when"], "; ".join(r["evidence_needed"]), r["owner"],
                r["pass_fail_status"]))
    else:
        out.append("_No gating items triggered by the provided facts. Re-check the intake object._")
    blocking = [r for r in rows if r["severity"] == "Blocking"]
    out.append("\n## Go-live gate (Blocking only)\n")
    if blocking:
        for r in blocking:
            out.append("- [ ] %s" % r["requirement"])
    else:
        out.append("- (none)")
    out.append("\n---\n")
    out.append("> " + DISCLAIMER)
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description="web-compliance-builder checklist generator")
    p.add_argument("intake", help="path to filled intake JSON, or '-' for stdin")
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--audit", action="store_true",
                   help="audit mode: compare required pages against intake['existing_pages'] and emit a gap report")
    args = p.parse_args(argv)

    raw = sys.stdin.read() if args.intake == "-" else open(args.intake, encoding="utf-8").read()
    try:
        intake = json.loads(raw)
    except json.JSONDecodeError as e:
        print("Invalid intake JSON: %s" % e, file=sys.stderr)
        return 2

    audit = args.audit or intake.get("mode") == "audit"
    pages = required_pages(intake)
    rows = gating_rows(intake)

    if audit:
        gap = audit_gap(intake, pages)
        if args.format == "json":
            print(json.dumps({
                "mode": "audit",
                "existing_pages": intake.get("existing_pages", []),
                "gap_report": gap,
                "gating_checklist": rows,
                "disclaimer": DISCLAIMER,
            }, indent=2, ensure_ascii=False))
        else:
            print(render_audit_md(intake, gap, rows))
        return 0

    if args.format == "json":
        print(json.dumps({
            "required_pages": [{"page": p_, "class": c, "reason": r} for p_, c, r in pages],
            "gating_checklist": rows,
            "disclaimer": DISCLAIMER,
        }, indent=2, ensure_ascii=False))
    else:
        print(render_md(intake, pages, rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
