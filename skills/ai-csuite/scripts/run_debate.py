from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

import jev
from common import ensure_logs, load_company, profile_for_stage, to_float

PERSONA = {
    "CTO": ("technical correctness and delivery risk", "CPO"),
    "CPO": ("user value and time-to-market", "CTO"),
    "CFO": ("runway protection and ROI", "COO"),
    "CMO": ("market positioning and demand", "CRO"),
    "CRO": ("revenue velocity", "CMO"),
    "COO": ("execution capacity", "CPO"),
    "CSA": ("architecture integrity", "CTO"),
    "CISO": ("security and compliance risk", "CTO"),
    "CV": ("customer evidence", "CRO"),
}

TOPIC_KEYS = {
    "pricing": ["pricing", "discount", "plan", "tier", "price"],
    "hiring": ["hire", "headcount", "team", "recruit"],
    "architecture": ["architecture", "scale", "infra", "microservice", "technical"],
    "security": ["security", "compliance", "gdpr", "soc2", "breach"],
    "growth": ["gtm", "sales", "pipeline", "acquisition", "growth", "marketing"],
}

# Fallback position when a role has no category-specific stance below.
RECS = {
    "pricing": "Run a 90-day pricing experiment with strict guardrails.",
    "hiring": "Delay permanent hires and use scoped contract support first.",
    "architecture": "Ship with a modular monolith and isolate critical services.",
    "security": "Gate release on baseline controls, logging, and access hardening.",
    "growth": "Focus on one ICP and one repeatable acquisition channel.",
    "general": "Prioritize reversible bets with measurable checkpoints.",
}

# Per-role opening positions. These must genuinely conflict: a debate where every
# executive opens with the same recommendation is theater, and the quality
# guardrail "Round 1 cannot be uniform agreement" depends on this table.
STANCES: dict[str, dict[str, str]] = {
    "pricing": {
        "CFO": "Raise prices now on new customers only and protect gross margin.",
        "CRO": "Hold list price and close the pipeline before changing the offer.",
        "CMO": "Reposition on value first, then price to the new segment.",
        "CPO": "Repackage tiers so the price change lands as added value.",
        "CTO": "Do not ship price logic until billing and entitlements are safe.",
        "CV": "Grandfather existing customers or churn risk outweighs the gain.",
        "COO": "Sequence the change so support can absorb the contact volume.",
        "CSA": "Keep pricing rules out of the core domain model.",
        "CISO": "Price changes touch payment data; keep the audit trail intact.",
    },
    "hiring": {
        "CFO": "Freeze headcount; every hire shortens runway by a measurable amount.",
        "CRO": "Hire revenue roles now or the pipeline stalls next quarter.",
        "CMO": "Contract specialists per campaign instead of permanent hires.",
        "CPO": "One senior generalist beats three juniors at this stage.",
        "CTO": "Hire for the on-call gap first; the team cannot sustain the rotation.",
        "CV": "Support load is the binding constraint customers actually feel.",
        "COO": "Fix process before adding people, or add cost without output.",
        "CSA": "A bigger team without architecture ownership multiplies drift.",
        "CISO": "Any hire with production access needs vetting budget included.",
    },
    "architecture": {
        "CFO": "Defer the rewrite; capitalize nothing that does not ship revenue.",
        "CRO": "Whatever unblocks the enterprise deals in flight wins.",
        "CMO": "Only invest here if it becomes a credible differentiator.",
        "CPO": "Fix the top three user-visible failures before any refactor.",
        "CTO": "Extract the failing service now; the coupling is the real cost.",
        "CV": "Customers report reliability, not architecture; target the outages.",
        "COO": "Choose the option the current team can actually operate.",
        "CSA": "Set the boundary now or every later change pays the tax.",
        "CISO": "Isolation is a security control, not just an engineering nicety.",
    },
    "security": {
        "CFO": "Scope to the controls a buyer actually asks for; defer the rest.",
        "CRO": "Compliance gaps are already costing deals; close them now.",
        "CMO": "Publish the trust posture once it is real, not before.",
        "CPO": "Bake controls into the flows instead of bolting on a checklist.",
        "CTO": "Automate the controls or they decay within one quarter.",
        "CV": "Customers ask for the questionnaire answers, not the certificate.",
        "COO": "Write the runbook; an untested incident process is not a control.",
        "CSA": "Put the trust boundary in the design, not in review comments.",
        "CISO": "Gate the release; unlogged access is an unacceptable baseline.",
    },
    "growth": {
        "CFO": "Cap CAC and kill any channel without payback inside two quarters.",
        "CRO": "Double down on the one channel already producing pipeline.",
        "CMO": "Test two adjacent channels before declaring a winner.",
        "CPO": "Fix activation first; acquisition into a leaky product wastes spend.",
        "CTO": "Instrument the funnel before spending, or the data is worthless.",
        "CV": "Existing customers name the segment; expand where they already are.",
        "COO": "Only scale what delivery can fulfill without degrading service.",
        "CSA": "Multi-segment support has an architecture cost; scope it first.",
        "CISO": "New channels bring new data flows; check consent and residency.",
    },
    "general": {
        "CFO": "Take the lowest-burn reversible option and set a spend ceiling.",
        "CRO": "Choose the path that shortens time to revenue.",
        "CMO": "Choose the path that sharpens the story to the market.",
        "CPO": "Choose the path with the clearest user-visible outcome.",
        "CTO": "Choose the path the team can deliver and roll back.",
        "CV": "Choose the path customers have already asked for.",
        "COO": "Choose the path that fits current execution capacity.",
        "CSA": "Choose the path that does not foreclose future options.",
        "CISO": "Choose the path with the smallest new risk surface.",
    },
}

# What each role concedes and what it refuses to trade away in the final round.
FINAL_POSITIONS: dict[str, tuple[str, str]] = {
    "CFO": ("Accepts spend that has a measurable payback window.", "Will not accept an open-ended burn commitment."),
    "CRO": ("Accepts guardrails that do not slow the active pipeline.", "Will not accept a freeze on revenue motion."),
    "CMO": ("Accepts a narrower initial segment.", "Will not accept launching without a clear position."),
    "CPO": ("Accepts a smaller scope to hit the date.", "Will not accept shipping a known broken flow."),
    "CTO": ("Accepts shipping sooner behind a flag.", "Will not accept a change without a rollback path."),
    "CV": ("Accepts phasing the rollout by segment.", "Will not accept silently breaking existing customers."),
    "COO": ("Accepts a pilot before the full rollout.", "Will not accept load the team cannot staff."),
    "CSA": ("Accepts a pragmatic interim boundary.", "Will not accept new coupling into the core domain."),
    "CISO": ("Accepts a time-boxed exception with compensating controls.", "Will not accept unlogged privileged access."),
}


def classify_topic(topic: str) -> str:
    text = topic.lower()
    for category, keys in TOPIC_KEYS.items():
        if any(word in text for word in keys):
            return category
    return "general"


def confidence(agent: str, category: str) -> str:
    high = {
        "pricing": {"CFO", "CRO", "CMO"},
        "hiring": {"COO", "CFO", "CEO"},
        "architecture": {"CTO", "CSA"},
        "security": {"CISO", "CTO"},
        "growth": {"CMO", "CRO", "CV"},
        "general": {"CEO", "CoS"},
    }
    return "high" if agent in high.get(category, set()) else "medium"


def stance(agent: str, category: str) -> str:
    return STANCES.get(category, {}).get(agent) or RECS[category]


def round1(agent: str, topic: str, company: dict, category: str) -> tuple[str, str, str]:
    goal = PERSONA.get(agent, ("cross-functional alignment", "CFO"))[0]
    recommendation = stance(agent, category)
    analysis = (
        f"{agent} evaluates '{topic}' for {company['company_name']} through {goal}. "
        f"The current stage ({company['stage']}) and constraints shape execution options."
    )
    return analysis, recommendation, confidence(agent, category)


def round2(agent: str, agents: list[str], recommendation: str) -> tuple[str, str, str]:
    clash = PERSONA.get(agent, ("", "CFO"))[1]
    peers = [a for a in agents if a != agent and a not in {"CEO", "CoS"}]
    agree = peers[0] if peers else "team"
    challenge = clash if clash in peers else (peers[-1] if peers else "team")
    updated = "Holding position" if challenge == "team" else recommendation
    return agree, challenge, updated


def round3(agent: str, recommendation: str) -> tuple[str, str, str]:
    concession, hard_line = FINAL_POSITIONS.get(
        agent,
        ("Conceded speed where risk remains reversible.", "Will not accept unbounded cost or unmitigated risk."),
    )
    return concession, hard_line, recommendation


def data_brief(company: dict, category: str) -> tuple[str, str]:
    customer = f"Customer signal priority is {category}; validate with churn and support trend snapshots."
    runway = to_float(company["runway_months"])
    severity = "high" if runway < 6 else "normal"
    finance = f"Runway is {company['runway_months']} months; financial severity is {severity}."
    return customer, finance


def pick_consensus(recommendations: dict[str, str], runway: float, category: str) -> tuple[str, bool]:
    """Weighted pick across divergent positions.

    Returns the winning position and whether the debate is effectively deadlocked.
    Positions now differ per role, so a plain vote count ties at 1-1-1 and silently
    resolves by dict order. Weight each position by how much authority its owner
    has on this category, and report a tie as a deadlock instead of hiding it.
    """
    if runway < 6:
        return "Choose the lowest-burn reversible option and defer heavy commitments.", False

    tally: Counter[str] = Counter()
    for agent, position in recommendations.items():
        tally[position] += 2 if confidence(agent, category) == "high" else 1
    ranked = tally.most_common()
    if not ranked:
        return RECS[category], False
    top_position, top_weight = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0
    return top_position, top_weight == runner_up


def ceo_decision(consensus: str, runway: float, category: str) -> tuple[str, str, str, str, str, str]:
    decision = consensus
    if runway < 6 and category in {"hiring", "growth"}:
        decision = "Stabilize runway first, then run a constrained test before expansion."
    rationale = "Decision balances speed, risk, and reversibility against current constraints."
    weighed = "Runway, customer impact, technical feasibility, and execution capacity."
    overrides = "Overrode high-burn paths due to runway risk." if runway < 6 else "No major override."
    trigger = "Revisit if leading indicator misses target for two cycles."
    reversibility = "easily_reversible" if category in {"pricing", "growth", "general"} else "costly_to_reverse"
    return decision, rationale, weighed, overrides, trigger, reversibility


def escalation_lines(escalations: dict[str, float]) -> list[str]:
    """Render only the escalations Jev judged likely, with their probabilities."""
    labels = {
        "legal_risk": "CISO: legal or compliance exposure",
        "runway_risk": "CFO: runway risk from this decision",
        "customer_contradiction": "CV: customer evidence contradicts consensus",
        "deadlock": "Positions remain unresolved after the final round",
        "groupthink": "CoS: consensus formed without substantive disagreement",
    }
    flagged = [(labels[name], value) for name, value in escalations.items() if value >= 0.5]
    if not flagged:
        return ["- No escalation triggered."]
    return [f"- {label} (p={value:.2f})" for label, value in sorted(flagged, key=lambda item: -item[1])]


def build_output(
    topic: str, company: dict, agents: list[str], rounds: int, category: str, use_jev: bool = False
) -> str:
    runway = to_float(company["runway_months"])
    customer_signal, finance_signal = data_brief(company, category)
    debaters = [a for a in agents if a not in {"CEO", "CoS"}]
    r1: dict[str, tuple[str, str, str]] = {a: round1(a, topic, company, category) for a in debaters}
    r2: dict[str, tuple[str, str, str]] = {a: round2(a, debaters, r1[a][1]) for a in debaters}
    consensus, deadlocked = pick_consensus({a: r1[a][1] for a in debaters}, runway, category)
    decision, rationale, weighed, overrides, trigger, reversibility = ceo_decision(consensus, runway, category)
    ceo_confidence = 7
    escalations: dict[str, float] = {}

    verdict = (
        jev.judge_debate(
            topic,
            company,
            {a: r1[a][1] for a in debaters},
            {"customer": customer_signal, "finance": finance_signal},
        )
        if use_jev
        else None
    )
    if verdict:
        consensus = verdict["consensus"]
        decision, rationale, weighed, overrides, trigger, _ = ceo_decision(consensus, runway, category)
        reversibility = verdict["reversibility"]
        ceo_confidence = verdict["confidence"]
        escalations = verdict["escalations"]

    dissenters = [a for a in debaters if r1[a][1] != consensus]
    tensions = (
        f"{', '.join(dissenters)} argued against the winning position."
        if dissenters
        else "No substantive disagreement surfaced; treat this consensus with suspicion."
    )

    lines = ["**DATA BRIEF (Pre-Round):**", f"- Customer signals: {customer_signal}", f"- Financial context: {finance_signal}", ""]
    for agent in debaters:
        lines += [f"**{agent} (Round 1):**", r1[agent][0], f"Recommendation: {r1[agent][1]}", f"Confidence: {r1[agent][2]}", ""]
    for agent in debaters:
        lines += [f"**{agent} (Round 2):**", f"Agrees with: {r2[agent][0]}", f"Challenges: {r2[agent][1]}", f"Updated position: {r2[agent][2]}", ""]
    if rounds == 3:
        for agent in debaters:
            r3 = round3(agent, r1[agent][1])
            lines += [f"**{agent} (Round 3):**", f"Concessions: {r3[0]}", f"Hard line: {r3[1]}", f"Final recommendation: {r3[2]}", ""]
    lines += [
        "---", "**CEO BRIEF**", "", f"**Topic:** {topic}", f"**Consensus Position:** {consensus}",
        f"**Key Tensions:** {tensions}",
        f"**Recommended Option:** {consensus}", "**Risk Flags:**", f"- {finance_signal}",
        *([f"- Deadlock: positions remain split; the CEO is breaking the tie, not ratifying agreement."]
          if deadlocked else []),
        *(escalation_lines(escalations) if escalations else []),
        "**Decision Required:** Confirm execution start and owners.", "---", "",
        "---", "**CEO DECISION**", "", f"**DECISION:** {decision}", f"**RATIONALE:** {rationale}",
        f"**WHAT I WEIGHED:** {weighed}", f"**OVERRIDES:** {overrides}", "**NEXT STEPS:**",
        "- CTO: Deliver technical plan and rollback condition.", "- CFO: Track budget and runway variance weekly.",
        "- CPO: Define success metrics and user impact checks.", f"**REVIEW TRIGGER:** {trigger}",
        f"**CONFIDENCE:** {ceo_confidence}", f"**REVERSIBILITY:** {reversibility}", "---",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--company-file", default="config/company.yaml")
    parser.add_argument("--output")
    parser.add_argument(
        "--jev",
        action="store_true",
        help="Use Jev (TypeSafe) for topic classification, consensus, reversibility, "
        "confidence, and escalation checks. Requires TYPESAFE_API_KEY; falls back "
        "to the deterministic logic if unavailable.",
    )
    args = parser.parse_args()
    company = load_company(args.company_file)
    profile = profile_for_stage(company["stage"])
    if args.jev and not jev.enabled():
        print("warning: --jev requested but TYPESAFE_API_KEY is not set; using static logic")
    category = (jev.classify_topic(args.topic, company) if args.jev else None) or classify_topic(args.topic)
    body = build_output(args.topic, company, profile["agents"], profile["rounds"], category, use_jev=args.jev)
    if args.output:
        out_path = Path(args.output)
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = ensure_logs(Path.cwd()) / f"debate-{stamp}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
