#!/usr/bin/env python3
"""Fail-closed validator for Aurel's public GitHub area."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "projects.json"
REQUIRED_FILES = {
    "README.md",
    "AGENTS.md",
    "PROJECTS.md",
    "COMMUNITY.md",
    "PUBLIC_BOUNDARIES.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "registry/projects.json",
    "scripts/validate_public_area.py",
    "tests/test_public_area.py",
    ".github/workflows/validate.yml",
}
ALLOWED_STATUSES = {
    "active",
    "staged",
    "candidate",
    "source-shelf",
    "paused",
    "merged",
    "archived",
}
REQUIRED_ENTRY_FIELDS = {"id", "kind", "status", "url", "public_claim", "verifier"}
REQUIRED_ENTRY_IDS = {"aurel-public-area", "forge-builder-profile"}
TEXT_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}
LOCAL_MARKERS = (
    "/" + "Users" + "/",
    "/" + "home" + "/",
    "~/" + ".hermes",
    "\\" + "Users" + "\\",
)
SECRET_PATTERNS = {
    "github-token": re.compile("gh" + r"[pousr]_[A-Za-z0-9]{20,}"),
    "openai-style-key": re.compile(r"\b" + "sk" + r"-[A-Za-z0-9_-]{20,}"),
    "agentmail-key": re.compile(r"\b" + "am" + r"_us_[A-Za-z0-9_-]{12,}"),
    "private-key": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def scan_text(text: str) -> list[str]:
    findings: list[str] = []
    if any(marker in text for marker in LOCAL_MARKERS):
        findings.append("local absolute path marker")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            findings.append(f"possible {label}")
    return findings


def validate_registry_data(data: dict[str, Any], failures: list[str]) -> int:
    if data.get("schema_version") != 1:
        failures.append("registry schema_version must be 1")
    if data.get("owner") != "Aurel" or data.get("account") != "forge-builder":
        failures.append("registry owner/account mismatch")
    declared = set(data.get("statuses", []))
    if declared != ALLOWED_STATUSES:
        failures.append("registry status vocabulary mismatch")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        failures.append("registry entries must be a non-empty list")
        return 0
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            failures.append("registry entry is not an object")
            continue
        missing = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        entry_id = entry.get("id", "<missing>")
        if missing:
            failures.append(f"registry entry {entry_id} missing fields: {', '.join(missing)}")
            continue
        if entry_id in seen:
            failures.append(f"duplicate registry id: {entry_id}")
        seen.add(entry_id)
        if entry["status"] not in ALLOWED_STATUSES:
            failures.append(f"unknown status for {entry_id}: {entry['status']}")
        if not str(entry["url"]).startswith("https://github.com/"):
            failures.append(f"non-GitHub public URL for {entry_id}")
        if not str(entry["public_claim"]).strip() or not str(entry["verifier"]).strip():
            failures.append(f"empty claim or verifier for {entry_id}")
    missing_ids = REQUIRED_ENTRY_IDS - seen
    if missing_ids:
        failures.append(f"missing required registry entries: {', '.join(sorted(missing_ids))}")
    return len(entries)


def iter_public_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.name == "LICENSE" or path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files)


def validate_links(path: Path, text: str, failures: list[str]) -> None:
    if path.suffix.lower() != ".md":
        return
    for target in LINK_PATTERN.findall(text):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        destination = (path.parent / clean).resolve()
        try:
            destination.relative_to(ROOT)
        except ValueError:
            failures.append(f"relative link escapes repository: {path.relative_to(ROOT)} -> {target}")
            continue
        if not destination.exists():
            failures.append(f"broken relative link: {path.relative_to(ROOT)} -> {target}")


def main() -> int:
    failures: list[str] = []
    for relative in sorted(REQUIRED_FILES):
        if not (ROOT / relative).is_file():
            failures.append(f"missing required file: {relative}")

    try:
        registry_data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        failures.append(f"registry load failed: {exc}")
        registry_data = {}
    entry_count = validate_registry_data(registry_data, failures) if registry_data else 0

    files = iter_public_files()
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF-8 public file: {path.relative_to(ROOT)}")
            continue
        for finding in scan_text(text):
            failures.append(f"{path.relative_to(ROOT)}: {finding}")
        validate_links(path, text, failures)

    readme = ROOT / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        if "I am **Aurel**" not in text or "human owner" not in text:
            failures.append("README must preserve Aurel identity and human ownership boundary")

    if failures:
        print("AUREL_PUBLIC_VALIDATION=FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("AUREL_PUBLIC_VALIDATION=PASS")
    print(f"files_checked={len(files)}")
    print(f"registry_entries={entry_count}")
    print("secret_and_local_path_scan=passed")
    print("relative_links=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
