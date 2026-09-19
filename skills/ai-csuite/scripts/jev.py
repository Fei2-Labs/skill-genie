"""Optional Jev (TypeSafe System One) judgments for the debate pipeline.

This module is inert unless the caller passes --jev. Every function degrades to
None when the key is absent or the call fails, so run_debate.py keeps its
deterministic behavior and the skill makes no network call by default.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
TIMEOUT = 20

TOPIC_CRITERIA = {
    "pricing": "Price levels, discounts, plans, tiers, packaging, monetization.",
    "hiring": "Headcount, recruiting, contractors, team composition, roles.",
    "architecture": "System design, scaling, infrastructure, technical debt, platform choices.",
    "security": "Security posture, compliance, privacy, audits, incident risk.",
    "growth": "Go-to-market, acquisition channels, sales motion, marketing, pipeline.",
    "general": "Strategic questions that fit none of the other categories.",
}

REVERSIBILITY_CRITERIA = {
    "easily_reversible": "Can be undone within days at low cost if it underperforms.",
    "costly_to_reverse": "Can be undone, but only with meaningful rework, spend, or lost time.",
    "irreversible": "Commits the company in a way that cannot practically be undone.",
}

ESCALATIONS = {
    "legal_risk": "Does this decision carry legal, regulatory, or compliance exposure that a CISO would insist appears in the CEO brief?",
    "runway_risk": "Does this decision materially increase the risk of running out of money before the next milestone?",
    "customer_contradiction": "Does the customer evidence in the state contradict the consensus position?",
    "deadlock": "Do the executive positions in the state remain genuinely unresolved rather than converged?",
    "groupthink": "Did the executives converge without any substantive disagreement being aired?",
}


class JevUnavailable(RuntimeError):
    """Raised when Jev cannot be reached; callers fall back to static logic."""


def enabled() -> bool:
    return bool(os.environ.get("TYPESAFE_API_KEY"))


def _ask(state: object, questions: dict) -> dict:
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise JevUnavailable("TYPESAFE_API_KEY is not set")
    payload = json.dumps({"state": state, "model": MODEL, "questions": questions}).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - any failure must degrade, not propagate
        # urllib raises across several unrelated trees here: URLError/HTTPError,
        # bare OSError subclasses (ConnectionReset, BrokenPipe, SSLError), and
        # http.client errors (RemoteDisconnected, IncompleteRead) that are not
        # OSError at all. Falling back matters more than classifying the cause.
        raise JevUnavailable(f"Jev request failed: {type(exc).__name__}: {exc}") from exc
    if not isinstance(body, dict):
        raise JevUnavailable("Jev response was not a JSON object")
    answers = body.get("answers")
    if not isinstance(answers, dict):
        raise JevUnavailable("Jev response had no answers")
    return answers


def _choice(answers: dict, name: str, allowed: object = None) -> str:
    value = answers.get(name, {})
    if not isinstance(value, dict):
        raise JevUnavailable(f"{name}: answer was not an object")
    choice = value.get("choice")
    if not isinstance(choice, str) or not choice:
        raise JevUnavailable(f"{name}: choice was not a non-empty string")
    if allowed is not None and choice not in allowed:
        raise JevUnavailable(f"{name}: choice {choice!r} was not an offered option")
    return choice


def _number(answers: dict, name: str, field: str, low: float, high: float) -> float:
    value = answers.get(name, {})
    if not isinstance(value, dict):
        raise JevUnavailable(f"{name}: answer was not an object")
    number = value.get(field)
    if isinstance(number, bool) or not isinstance(number, (int, float)):
        raise JevUnavailable(f"{name}: {field} was not a number")
    if not low <= number <= high:
        raise JevUnavailable(f"{name}: {field} {number} outside [{low}, {high}]")
    return float(number)


def classify_topic(topic: str, company: dict) -> str | None:
    """Return a topic category, or None to fall back to keyword matching."""
    state = {
        "topic": topic,
        "company": company["company_name"],
        "product": company["product"],
        "stage": company["stage"],
    }
    questions = {
        "category": {
            "type": "choice",
            "instructions": "Which decision area does the topic in `topic` belong to?",
            "criteria": TOPIC_CRITERIA,
        }
    }
    try:
        return _choice(_ask(state, questions), "category", TOPIC_CRITERIA)
    except Exception:  # noqa: BLE001 - callers fall back to keyword matching
        return None


def judge_debate(topic: str, company: dict, positions: dict[str, str], signals: dict[str, str]) -> dict | None:
    """Judge the debate once round 1 positions exist.

    Returns a dict with consensus, reversibility, confidence (0-10) and the
    escalation flags, or None when Jev is unavailable.
    """
    options = sorted(set(positions.values()))
    if len(options) < 2:
        options = options + ["Hold the current course and re-evaluate after one cycle."]
    state = {
        "topic": topic,
        "company": company["company_name"],
        "stage": company["stage"],
        "runway_months": company["runway_months"],
        "constraints": company["constraints"],
        "executive_positions": positions,
        "customer_signal": signals["customer"],
        "financial_signal": signals["finance"],
    }
    questions = {
        "consensus": {
            "type": "choice",
            "instructions": (
                "Given the executive positions in `executive_positions` and the constraints in "
                "`constraints`, which course of action should the company take?"
            ),
            "criteria": {option: "A course of action proposed during the debate." for option in options},
        },
        "reversibility": {
            "type": "choice",
            "instructions": "How reversible is the course of action the executives are converging on?",
            "criteria": REVERSIBILITY_CRITERIA,
        },
        "confidence": {
            "type": "score",
            "instructions": "How much confidence do the positions and evidence in the state justify?",
            "criteria": [
                "Speculative: the evidence does not support committing.",
                "Tentative: plausible, but key assumptions are untested.",
                "Reasonable: the evidence supports acting with checkpoints.",
                "Strong: the evidence clearly supports this course of action.",
            ],
        },
    }
    for name, instructions in ESCALATIONS.items():
        questions[name] = {"type": "noul", "instructions": instructions}

    levels = len(questions["confidence"]["criteria"]) - 1
    try:
        answers = _ask(state, questions)
        return {
            "consensus": _choice(answers, "consensus", options),
            "consensus_confidence": _number(answers, "consensus", "confidence", 0.0, 1.0),
            "reversibility": _choice(answers, "reversibility", REVERSIBILITY_CRITERIA),
            "confidence": round(_number(answers, "confidence", "score", 0.0, levels) / levels * 10),
            "escalations": {
                name: _number(answers, name, "noul", 0.0, 1.0) for name in ESCALATIONS
            },
        }
    except Exception:  # noqa: BLE001 - callers fall back to the deterministic path
        return None
