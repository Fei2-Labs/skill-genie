#!/usr/bin/env python3
"""Offline documentation and regression tests for the conditional original-rewrite mode.

These tests read files only. They never perform a network call and never touch the
WeChat API. They check that the documented contract matches the recorded screening
policy, that every verified source-preservation conflict site carries a conditional
boundary, and that the unrelated delivery CLI is unchanged.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES = SKILL_DIR / "references"
SCRIPTS = SKILL_DIR / "scripts"
ORIGINAL_REWRITE = REFERENCES / "original-rewrite.md"

MODE_NAME = "rewriteMode: methodology-only"
POLICY_VERSION = "screening-policy-1"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ReferenceExistsTest(unittest.TestCase):
    def test_reference_file_exists(self) -> None:
        self.assertTrue(ORIGINAL_REWRITE.is_file(), f"missing {ORIGINAL_REWRITE}")

    def test_reference_names_the_mode(self) -> None:
        self.assertIn(MODE_NAME, read(ORIGINAL_REWRITE))


class RoutingLinkTest(unittest.TestCase):
    """The reference must be reachable from the documents that route execution."""

    ROUTING_DOCS = (
        SKILL_DIR / "SKILL.md",
        REFERENCES / "execution-contract.md",
        REFERENCES / "style-engine.md",
        REFERENCES / "capability-map.md",
        SKILL_DIR / "README.md",
        SKILL_DIR / "docs" / "EXAMPLES.md",
    )

    def test_every_routing_document_links_the_reference(self) -> None:
        for doc in self.ROUTING_DOCS:
            with self.subTest(doc=doc.name):
                self.assertTrue(doc.is_file(), f"missing {doc}")
                self.assertIn("original-rewrite.md", read(doc))

    def test_changelog_records_the_mode(self) -> None:
        self.assertIn("original-rewrite.md", read(SKILL_DIR / "CHANGELOG.md"))


class ConflictSiteBoundaryTest(unittest.TestCase):
    """Each conflict site verified in research/screening-policy.md must be conditional.

    The original instruction must survive (nothing is globally deleted or weakened),
    and it must be followed closely by an exception scoped to this mode only.
    """

    # (file, unconditional instruction that must still be present)
    CONFLICT_SITES = (
        (
            SKILL_DIR / "SKILL.md",
            "Treat source capture as a runtime boundary: preserve title, author, "
            "description, body text, and image list before rewriting.",
        ),
        (
            SKILL_DIR / "SKILL.md",
            "goal: preserve the useful source core, then rebuild it for WeChat "
            "reading and distribution",
        ),
        (
            REFERENCES / "execution-contract.md",
            "preserve title, author, description, content, and image list before rewriting",
        ),
        (
            REFERENCES / "execution-contract.md",
            "what must be preserved verbatim or semantically",
        ),
        (
            REFERENCES / "execution-contract.md",
            "preserve statistics, named sources, and substantive paragraphs unless "
            "they are demonstrably wrong",
        ),
        (
            REFERENCES / "style-engine.md",
            "preserve all data points and named sources from original material",
        ),
        (
            REFERENCES / "capability-map.md",
            "requirement: preserve title, author, description, body text, image list, "
            "and source subtype when available",
        ),
        # Source-figure reuse is the "原图" half of the same conflict.
        (
            SKILL_DIR / "SKILL.md",
            "prefer source figures over generated visuals when they support the claim",
        ),
        (
            REFERENCES / "execution-contract.md",
            "prefer extracted source figures when they directly support the surrounding claim",
        ),
    )

    # How far after the instruction the scoped exception may appear.
    WINDOW = 1200

    def test_original_instruction_is_not_deleted(self) -> None:
        for path, instruction in self.CONFLICT_SITES:
            with self.subTest(path=path.name, instruction=instruction[:40]):
                self.assertIn(instruction, read(path))

    def test_each_conflict_site_carries_a_scoped_exception(self) -> None:
        for path, instruction in self.CONFLICT_SITES:
            with self.subTest(path=path.name, instruction=instruction[:40]):
                text = read(path)
                start = text.index(instruction) + len(instruction)
                window = text[start : start + self.WINDOW]
                self.assertIn("Exception", window)
                self.assertIn(MODE_NAME, window)
                self.assertIn("original-rewrite.md", window)

    def test_inline_visuals_source_figure_preference_is_overridden(self) -> None:
        """capability-map keeps the preference; its exception must name that capability."""
        text = read(REFERENCES / "capability-map.md")
        self.assertIn("prefer source figures extracted from PDFs when they support the claim", text)
        exception = next(line for line in text.splitlines() if "**Exception" in line)
        self.assertIn("inline-visuals", exception)
        self.assertIn("does not apply in this mode", exception)

    def test_exceptions_are_always_scoped_to_this_mode(self) -> None:
        """No exception marker may appear without naming the mode it is scoped to."""
        for path in {p for p, _ in self.CONFLICT_SITES}:
            with self.subTest(path=path.name):
                for line in read(path).splitlines():
                    if "**Exception" in line:
                        self.assertIn(MODE_NAME, line)
                        self.assertIn("only**", line)


class ActivationContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read(ORIGINAL_REWRITE)

    def test_both_conditions_are_required(self) -> None:
        self.assertIn("both", self.text.lower())
        self.assertIn("rewrite_intent", self.text)
        self.assertIn("source_body_obtained", self.text)

    def test_intake_record_fields_documented(self) -> None:
        for field in (
            "request_text",
            "source_inventory",
            "source_body_obtained",
            "rewrite_intent",
            "no_rewrite_restriction",
        ):
            with self.subTest(field=field):
                self.assertIn(field, self.text)

    def test_negative_triggers_documented(self) -> None:
        lowered = self.text.lower()
        for negative in (
            "topic only",
            "render-only",
            "save-only",
            "translation-only",
            "reference-only",
            "voice-samples-only",
        ):
            with self.subTest(negative=negative):
                self.assertIn(negative, lowered)

    def test_explicit_no_rewrite_restriction_is_honoured(self) -> None:
        self.assertIn("不要改写", self.text)

    def test_ambiguity_requires_clarification_not_keyword_matching(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("Keyword matching alone never classifies a request", collapsed)
        self.assertIn("ask one clarifying question and wait", collapsed)

    def test_capture_failure_blocks_instead_of_topic_fallback(self) -> None:
        self.assertIn("blocked", self.text)
        self.assertIn("fall back to topic-only generation", self.text)

    def test_negative_trigger_examples_are_published(self) -> None:
        examples = read(SKILL_DIR / "docs" / "EXAMPLES.md")
        self.assertIn("must NOT trigger", examples)
        for marker in (
            "topic only",
            "render-only",
            "save-only",
            "translation-only",
            "reference-only",
            "voice-samples-only",
            "no-rewrite restriction",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, examples)


class SourceSeparationAndResearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read(ORIGINAL_REWRITE)

    def test_captured_images_excluded_from_deliverable(self) -> None:
        self.assertIn("excluded", self.text)
        self.assertIn("manifest.json.outputs.wechat.images", self.text)

    def test_methodology_brief_and_exclusion_ledger(self) -> None:
        self.assertIn("methodology.md", self.text)
        self.assertIn("Exclusion ledger", self.text)

    def test_research_ledger_fields(self) -> None:
        for field in (
            "publisher",
            "URL or DOI",
            "publication date",
            "access date",
            "verified supporting passage",
            "applicability",
            "uncertainty",
        ):
            with self.subTest(field=field):
                self.assertIn(field, self.text)

    def test_substitute_citation_is_banned(self) -> None:
        self.assertIn("substitute", self.text)
        self.assertIn(
            "finding the same number elsewhere does not make the original's data reusable",
            " ".join(self.text.split()),
        )

    def test_persona_resolved_separately_with_declared_assumptions(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("persona", collapsed.lower())
        self.assertIn("declare the working assumptions", collapsed)
        self.assertIn("The original's author is never treated as the user", collapsed)


class EvaluationDimensionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read(ORIGINAL_REWRITE)

    def test_five_dimensions_documented(self) -> None:
        for dimension in (
            "Expression infringement risk",
            "Homogeneity",
            "Article potential",
            "Title potential",
            "Cover-direction potential",
        ):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, self.text)

    def test_shared_topic_is_not_infringement_evidence(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn(
            "shared abstract method is **not** evidence of infringement", collapsed
        )

    def test_cover_dimension_judges_a_text_brief_not_pixels(self) -> None:
        self.assertIn("not pixels", self.text)

    def test_scores_are_expected_level_indices_not_percentages(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("probability-weighted **expected** level index", collapsed)
        self.assertIn("not a percentage and not the most likely single level", collapsed)

    def test_editorial_tail_is_not_reported_as_severe(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("`top_tail_probability`", collapsed)
        self.assertIn("desirable end of an editorial scale", collapsed)

    def test_jev_does_not_author_prose_advice(self) -> None:
        self.assertIn("Jev does not write prose advice", self.text)
        self.assertIn("insufficient_evidence", self.text)


class PolicyNumbersTest(unittest.TestCase):
    """Documented policy numbers must match research/screening-policy.md."""

    def setUp(self) -> None:
        self.text = read(ORIGINAL_REWRITE)

    def test_policy_version(self) -> None:
        self.assertIn(POLICY_VERSION, self.text)

    def test_risk_mean_and_tail(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("expected score at most `1.0`", collapsed)
        self.assertIn("probability of levels 3 and 4 at most `0.05`", collapsed)

    def test_homogeneity_uses_the_same_two_conditions(self) -> None:
        self.assertIn("the same two conditions, evaluated independently", self.text)

    def test_confidence_floor_applies_to_risk_only(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("Confidence floor `0.50` on the two risk dimensions only", collapsed)
        self.assertIn("No confidence floor applies to these three", collapsed)

    def test_editorial_minimum(self) -> None:
        self.assertIn("at least `2.0` each", " ".join(self.text.split()))

    def test_revision_budget_is_three(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("Default budget: three assessed revisions", collapsed)
        self.assertIn("retries are not revisions", collapsed)

    def test_editorial_never_offsets_risk(self) -> None:
        self.assertIn("never offset a risk failure", self.text)

    def test_exhaustion_never_passes(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("`needs_revision` with an exhaustion reason, never `passed`", collapsed)

    def test_thresholds_declared_as_local_policy(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("not calibrated legal probabilities", collapsed)


class DocumentedCliTest(unittest.TestCase):
    """Documented CLI surface must match the contract in research/screening-policy.md."""

    def setUp(self) -> None:
        self.text = read(ORIGINAL_REWRITE)

    def test_offline_flags(self) -> None:
        for flag in ("--help", "--policy", "--example-input", "--example-output"):
            with self.subTest(flag=flag):
                self.assertIn(flag, self.text)

    def test_no_undocumented_flag_is_invented(self) -> None:
        import re

        allowed = {"--help", "--policy", "--example-input", "--example-output"}
        section = self.text[self.text.index("## 8. Evaluator CLI") :]
        found = set(re.findall(r"--[a-z][a-z-]+", section))
        self.assertEqual(found - allowed, set())

    def test_stdin_stdout_json_contract(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("reads one UTF-8 JSON object on standard input", collapsed)
        self.assertIn("prints one JSON object on standard output", collapsed)

    def test_input_fields(self) -> None:
        for field in (
            "`intake`",
            "`original`",
            "`draft`",
            "`title`",
            "`cover_brief`",
            "`audience`",
            "`persona_assumptions`",
            "`proposed_issues`",
            "`round`",
        ):
            with self.subTest(field=field):
                self.assertIn(field, self.text)

    def test_verify_only_recheck_is_documented(self) -> None:
        """The re-check input the evaluator accepts must not be an undocumented feature."""
        collapsed = " ".join(self.text.split())
        self.assertIn("`verify_only: true`", collapsed)
        self.assertIn("`previous_result`", collapsed)
        self.assertIn("the recorded `status` string is **not** trusted on its own", collapsed)

    def test_output_fields(self) -> None:
        for field in (
            "`ok`",
            "`status`",
            "`policy_version`",
            "`input_identity`",
            "`dimensions`",
            "`gaps`",
        ):
            with self.subTest(field=field):
                self.assertIn(field, self.text)

    def test_status_values(self) -> None:
        for status in ("`passed`", "`needs_revision`", "`blocked`", "`stale`"):
            with self.subTest(status=status):
                self.assertIn(status, self.text)

    def test_credential_source_is_the_environment(self) -> None:
        self.assertIn("TYPESAFE_API_KEY", self.text)
        self.assertIn("no vault call", self.text)

    def test_errors_are_sanitized(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("never a raw provider body, exception text, or credential value", collapsed)

    def test_oversized_input_blocks_instead_of_truncating(self) -> None:
        self.assertIn("never silently truncated", self.text)


class RoundRecordsAndBindingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = read(ORIGINAL_REWRITE)

    def test_round_directory_and_report(self) -> None:
        self.assertIn("rewrite-review/round-NNN/", self.text)
        self.assertIn("rewrite-report.md", self.text)

    def test_distributions_are_always_reported(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("Always show the full distribution, confidence, and scale", collapsed)
        self.assertIn(
            "Never describe a model probability as a real infringement probability", collapsed
        )

    def test_scores_are_never_copied_across_revisions(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("must refer to distinct input identities", collapsed)

    def test_render_normalization_precedes_final_check(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("`render` normalizes Markdown links", collapsed)
        self.assertIn("before** the final version check", collapsed)

    def test_unpassed_draft_cannot_be_delivered_as_accepted(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("must not enter draft delivery as accepted", collapsed)

    def test_manifest_entry_is_additive(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn("Existing `outputs.wechat` keys and `media_id` handling are unchanged", collapsed)

    def test_non_triggered_workflow_needs_no_credential_or_call(self) -> None:
        collapsed = " ".join(self.text.split())
        self.assertIn(
            "Non-triggered requests require no Jev credential, no review artifact, and no API call",
            collapsed,
        )

    def test_mock_never_reported_as_real(self) -> None:
        self.assertIn("A mock is never reported as a real", self.text)


class DeliveryCliUnchangedTest(unittest.TestCase):
    """Regression: the unrelated delivery CLI still parses with unchanged defaults.

    No network call and no WeChat write happens here — only argument parsing.
    """

    @classmethod
    def setUpClass(cls) -> None:
        if str(SCRIPTS) not in sys.path:
            sys.path.insert(0, str(SCRIPTS))
        import wechat_delivery  # noqa: PLC0415

        cls.parser = wechat_delivery.build_parser()

    def test_subcommands_unchanged(self) -> None:
        actions = [
            a
            for a in self.parser._subparsers._group_actions  # noqa: SLF001
            if hasattr(a, "choices")
        ]
        self.assertTrue(actions)
        self.assertEqual(
            sorted(actions[0].choices),
            sorted(
                [
                    "check",
                    "design-catalog",
                    "render",
                    "upload-images",
                    "save-draft",
                    "update-cover",
                ]
            ),
        )

    def test_render_defaults_unchanged(self) -> None:
        args = self.parser.parse_args(["render", "article-formatted.md", "-o", "article.html"])
        self.assertEqual(args.command, "render")
        self.assertEqual(args.design, "")
        self.assertEqual(args.color_mode, "auto")
        self.assertIsNone(args.upload_map)
        self.assertTrue(args.design_pen.endswith("design.pen"))

    def test_save_draft_defaults_unchanged(self) -> None:
        args = self.parser.parse_args(
            ["save-draft", "--html", "article.html", "--markdown", "article-formatted.md"]
        )
        self.assertEqual(args.cover_type, "image")
        self.assertEqual(args.cover_image, "")
        self.assertEqual(args.content_source_url, "")
        self.assertEqual(args.title, "")
        self.assertEqual(args.author, "")
        self.assertEqual(args.digest, "")
        self.assertIsNone(args.media_id)
        self.assertFalse(args.dry_run)
        self.assertFalse(args.settings_already_set)

    def test_update_cover_defaults_unchanged(self) -> None:
        args = self.parser.parse_args(["update-cover", "--cover-image", "imgs/cover.png"])
        self.assertEqual(args.cover_type, "thumb")
        self.assertIsNone(args.media_id)
        self.assertFalse(args.dry_run)

    def test_upload_images_defaults_unchanged(self) -> None:
        args = self.parser.parse_args(["upload-images", "imgs/cover.png"])
        self.assertEqual(args.images, ["imgs/cover.png"])
        self.assertIsNone(args.appid)
        self.assertIsNone(args.secret)
        self.assertIsNone(args.access_token)
        self.assertIsNone(args.output)
        self.assertFalse(args.dry_run)

    def test_delivery_script_has_no_rewrite_mode_coupling(self) -> None:
        source = read(SCRIPTS / "wechat_delivery.py")
        self.assertNotIn("TYPESAFE", source)
        self.assertNotIn("jev_rewrite", source)


class NoLeakedLocalIdentityTest(unittest.TestCase):
    """Shipped skill files must carry no author path, vault name or machine endpoint."""

    FORBIDDEN = ("/home/", "/Users/", "op://", "TYPESAFE_API_KEY=")

    def test_shipped_documents_are_portable(self) -> None:
        docs = [
            ORIGINAL_REWRITE,
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "README.md",
            SKILL_DIR / "CHANGELOG.md",
            SKILL_DIR / "docs" / "EXAMPLES.md",
            REFERENCES / "execution-contract.md",
            REFERENCES / "style-engine.md",
            REFERENCES / "capability-map.md",
        ]
        for doc in docs:
            text = read(doc)
            for token in self.FORBIDDEN:
                with self.subTest(doc=doc.name, token=token):
                    self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
