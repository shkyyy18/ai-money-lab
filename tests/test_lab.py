import json
import tempfile
import unittest
from pathlib import Path

from lab import summary, validate


class LabTests(unittest.TestCase):
    def test_repository_manifests_are_valid(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate(root), [])
        stats = summary(root)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["verified_revenue"], 0)
        self.assertEqual(stats["currencies"], ["CNY"])

    def write_manifest(self, root: Path, manifest: dict, report: bool = True) -> Path:
        folder = root / "experiments" / "001-demo"
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


if __name__ == "__main__":
    unittest.main()
