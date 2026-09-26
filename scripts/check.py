#!/usr/bin/env python3
"""Validate the portable profile; --sync updates only its plain-text export."""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"SKILL.md", "SHIFT_AGENT_PREFERENCES.md", "README.md", "EVALUATION.md",
           "LICENSE", ".gitignore", "agents/openai.yaml", "scripts/check.py",
           ".github/workflows/check.yml"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sync", action="store_true")
    args = parser.parse_args()
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    if not front:
        raise SystemExit("FAIL: missing skill frontmatter")
    expected = "# Shift 的长期协作偏好\n\n" + skill[front.end():].strip() + "\n"
    if args.sync:
        (ROOT / "SHIFT_AGENT_PREFERENCES.md").write_text(expected, encoding="utf-8")
    errors = []
    if "name: colleague-shift" not in front[1] or "description:" not in front[1]:
        errors.append("invalid skill identity")
    if (ROOT / "SHIFT_AGENT_PREFERENCES.md").read_text(encoding="utf-8") != expected:
        errors.append("plain-text export is stale; run --sync")
    # An allowlist prevents accidentally publishing local distillation datasets.
    found = set()
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__"} for part in rel.parts):
            continue
        if path.is_symlink():
            errors.append("symlink is not distributable: " + str(rel))
            continue
        if not path.is_file():
            continue
        name = rel.as_posix()
        found.add(name)
        if name not in ALLOWED:
            errors.append("unexpected file: " + name)
            continue
        text = path.read_text(encoding="utf-8")
        patterns = {
            "credential": r"(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{12,}|Bearer[ \t]+[A-Za-z0-9._-]{12,})",
            "private host": r"(?:192[.]168[.]\d+[.]\d+|10[.]\d+[.]\d+[.]\d+)",
            "personal filesystem": r"/(?:Users|home|Volumes)/[A-Za-z0-9]",
            "source identifier": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        }
        for label, pattern in patterns.items():
            if re.search(pattern, text):
                errors.append(label + " in " + name)
    if found != ALLOWED:
        errors.append("missing files: " + ", ".join(sorted(ALLOWED - found)))
    if errors:
        print("\n".join("FAIL: " + error for error in errors))
        return 1
    print("PASS: skill identity, synchronized export, file allowlist and privacy-pattern checks")
    print("NOTE: static checks do not establish live agent behavior")
    return 0

if __name__ == "__main__":
    sys.exit(main())
