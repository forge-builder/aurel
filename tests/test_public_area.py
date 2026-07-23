import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_public_area", ROOT / "scripts" / "validate_public_area.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PublicAreaValidationTests(unittest.TestCase):
    def test_checked_in_registry_passes(self):
        data = json.loads((ROOT / "registry" / "projects.json").read_text(encoding="utf-8"))
        failures: list[str] = []
        count = VALIDATOR.validate_registry_data(data, failures)
        self.assertEqual(8, count)
        self.assertEqual([], failures)

    def test_rejects_unknown_status(self):
        data = json.loads((ROOT / "registry" / "projects.json").read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        broken["entries"][0]["status"] = "production"
        failures: list[str] = []
        VALIDATOR.validate_registry_data(broken, failures)
        self.assertTrue(any("unknown status" in item for item in failures))

    def test_rejects_unrelated_public_url(self):
        data = json.loads((ROOT / "registry" / "projects.json").read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        broken["entries"][0]["url"] = "https://example.invalid/project"
        failures: list[str] = []
        VALIDATOR.validate_registry_data(broken, failures)
        self.assertTrue(any("non-GitHub public URL" in item for item in failures))

    def test_secret_scanner_fails_closed(self):
        synthetic = "token=" + "gh" + "p_" + ("A" * 24)
        findings = VALIDATOR.scan_text(synthetic)
        self.assertTrue(any("github-token" in item for item in findings))

    def test_local_path_scanner_fails_closed(self):
        synthetic = "/" + "Users" + "/someone/private.txt"
        findings = VALIDATOR.scan_text(synthetic)
        self.assertIn("local absolute path marker", findings)

    def test_safe_public_text_passes_scanner(self):
        self.assertEqual([], VALIDATOR.scan_text("Public evidence: https://github.com/forge-builder/aurel"))


if __name__ == "__main__":
    unittest.main()
