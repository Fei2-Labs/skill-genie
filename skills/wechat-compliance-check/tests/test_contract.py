from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "compliance_scan.py"
WORDLIST = ROOT / "references" / "sensitive-words.md"
CONSUMER = ROOT.parent / "research-to-wechat" / "SKILL.md"
CONTRACT = ROOT.parent / "research-to-wechat" / "references" / "execution-contract.md"


class ContractTests(unittest.TestCase):
    def test_standalone_validator_and_clean_offline_diagnostic(self) -> None:
        validation = subprocess.run([sys.executable, str(SCANNER), "--validate-wordlist"], capture_output=True, text=True)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        with tempfile.TemporaryDirectory() as temporary:
            article = Path(temporary) / "article.md"
            article.write_text("ordinary prose without a deterministic term", encoding="utf-8")
            # Offline mode is deliberately a blocked diagnostic because policy requires
            # the whole-document Jev check; it must not be mistaken for a clean gate.
            result = subprocess.run([sys.executable, str(SCANNER), str(article), "--no-jev", "--wordlist", str(WORDLIST)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(__import__("json").loads(result.stdout)["status"], "blocked")

    def test_always_hit_is_reported_without_credential(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            article = Path(temporary) / "article.md"
            article.write_text("VPN", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCANNER), str(article), "--wordlist", str(WORDLIST)], capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
        self.assertEqual(result.returncode, 2)
        report = __import__("json").loads(result.stdout)
        self.assertEqual(len(report["deterministic_hits"]), 1)
        self.assertEqual(report["error"]["code"], "missing_credential")

    def test_research_consumer_has_blocking_installed_skill_command(self) -> None:
        consumer = CONSUMER.read_text(encoding="utf-8")
        contract = CONTRACT.read_text(encoding="utf-8")
        for text in (consumer, contract):
            self.assertIn("COMPLIANCE_SKILL_DIR", text)
            self.assertIn("compliance_scan.py", text)
            self.assertIn("exit 2", text)
        self.assertIn("非公众号流程", consumer)

    def test_no_machine_specific_paths_in_distributable_files(self) -> None:
        for path in (SCANNER, ROOT / "scripts" / "update_wordlist.py", ROOT / "SKILL.md", ROOT / "README.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("/home/", text)
            self.assertNotIn("/Users/", text)
            self.assertNotIn("op://", text)


if __name__ == "__main__":
    unittest.main()
