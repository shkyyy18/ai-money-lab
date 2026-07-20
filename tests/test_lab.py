import json
import tempfile
import unittest
from pathlib import Path

from lab import render_leaderboard, summary, sync_readme_badges, validate


class LabTests(unittest.TestCase):
    def test_repository_manifests_are_valid(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate(root), [])
        stats = summary(root)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["verified_revenue"], 0)
        self.assertEqual(stats["currencies"], ["CNY"])

    def write_manifest(self, root: Path, manifest: dict, report: bool = True, slug: str = "001-demo") -> Path:
        folder = root / "experiments" / slug
        folder.mkdir(parents=True)
        if report:
            (folder / "result.md").write_text("result", encoding="utf-8")
        (folder / "experiment.json").write_text(json.dumps(manifest), encoding="utf-8")
        return folder

    def base_manifest(self) -> dict:
        return {
            "id": "001",
            "name": "demo",
            "status": "failed",
            "started_at": "2026-01-01",
            "completed_at": "2026-01-02",
            "revenue": 0,
            "currency": "USD",
            "evidence_level": "self-test",
            "report": "result.md",
            "conclusion": "The declared technical test failed.",
        }

    def test_missing_report_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_manifest(root, self.base_manifest(), report=False)
            self.assertTrue(any("report does not exist" in item for item in validate(root)))

    def test_completed_status_requires_date_and_conclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest()
            manifest.pop("completed_at")
            manifest.pop("conclusion")
            self.write_manifest(root, manifest)
            errors = validate(root)
            self.assertTrue(any("completed_at" in item for item in errors))
            self.assertTrue(any("conclusion" in item for item in errors))

    def test_nonzero_revenue_requires_verified_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest()
            manifest["revenue"] = 10
            self.write_manifest(root, manifest)
            self.assertTrue(any("non-zero revenue" in item for item in validate(root)))

    def test_completion_date_cannot_precede_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest()
            manifest["completed_at"] = "2025-12-31"
            self.write_manifest(root, manifest)
            self.assertTrue(any("cannot be before" in item for item in validate(root)))

    def test_summary_aggregates_manifests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_manifest(root, self.base_manifest())
            winner = self.base_manifest()
            winner.update({"id": "002", "status": "succeeded", "revenue": 25, "evidence_level": "verified-revenue"})
            self.write_manifest(root, winner, slug="002-winner")
            stats = summary(root)
            self.assertEqual(stats["experiments"], 2)
            self.assertEqual(stats["completed"], 2)
            self.assertEqual(stats["succeeded"], 1)
            self.assertEqual(stats["failed"], 1)
            self.assertEqual(stats["inconclusive"], 0)
            self.assertEqual(stats["verified_revenue"], 25)
            self.assertEqual(stats["currencies"], ["USD"])

    def test_leaderboard_renders_table_and_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_manifest(root, self.base_manifest())
            text = render_leaderboard(root)
            self.assertIn("| 001 | demo | Failed | USD 0 | `self-test` | The declared technical test failed. | [Result](experiments/001-demo/result.md) |", text)
            self.assertIn("- Experiments: **1**", text)
            self.assertIn("- Closed: **1**", text)
            self.assertIn("- Verified revenue recorded: **USD 0**", text)

    def test_sync_readme_badges_updates_static_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_manifest(root, self.base_manifest())
            readme = root / "README.md"
            readme.write_text(
                "![a](https://img.shields.io/badge/closed%20experiments-7-blue)\n"
                "![b](https://img.shields.io/badge/verified%20revenue-USD%2099-lightgrey)\n",
                encoding="utf-8",
            )
            self.assertTrue(sync_readme_badges(root))
            text = readme.read_text(encoding="utf-8")
            self.assertIn("badge/closed%20experiments-1-blue", text)
            self.assertIn("badge/verified%20revenue-USD%200-lightgrey", text)
            self.assertFalse(sync_readme_badges(root))

    def test_repository_leaderboard_is_current(self):
        root = Path(__file__).resolve().parents[1]
        expected = render_leaderboard(root)
        actual = (root / "leaderboard.md").read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
