#!/usr/bin/env python3
"""Validate a Shift delivery receipt before completion is claimed.

Usage:
    delivery_check.py <receipt.md>   validate one receipt file
    delivery_check.py --selftest     run built-in pass/fail cases

This gate cannot prove the work is correct; it enforces that a claim of
completion always arrives with checkable evidence instead of bare words.
"""
import re
import sys
import tempfile
from pathlib import Path

FIELD_RE = re.compile(
    r"^(?P<indent>\s*)[-*]\s*(?:\*\*)?\s*"
    r"(?P<name>结果|入口|验证|未验证与剩余|未验证)"
    r"(?:\*\*)?\s*[:：]\s*(?P<value>.*)$"
)
BULLET_RE = re.compile(r"^(?P<indent>\s*)[-*]\s+(?P<value>.+)$")
EVIDENCE_PATTERNS = [
    r"`[^`]+`",                      # inline command or code
    r"https?://",                    # link
    r"exit code[:：]?\s*\d+",        # command exit status
    r"\b(?:PASS|OK)\b",              # explicit checker verdict
    r"sha256",                       # artifact digest
    r"v?\d+\.\d+(?:\.\d+)?",         # version number
    r"[\w.-]+[.](?:png|jpe?g|webp|gif|mov|mp4)",  # screenshot or recording
]
EVIDENCE_RES = [re.compile(p, re.IGNORECASE) for p in EVIDENCE_PATTERNS]
PLACEHOLDER_RE = re.compile(r"[【\[][^】\]]*[】\]]|填写|占位|placeholder", re.IGNORECASE)


def parse_fields(text):
    """Split the receipt into top-level fields; '验证' keeps nested bullets."""
    fields = {}
    order = []
    for line in text.splitlines():
        m = FIELD_RE.match(line)
        if m and m.group("indent") == "":
            name = "未验证" if m.group("name").startswith("未验证") else m.group("name")
            fields[name] = {"value": m.group("value").strip(), "bullets": []}
            order.append(name)
        elif order and BULLET_RE.match(line):
            fields[order[-1]]["bullets"].append(BULLET_RE.match(line).group("value").strip())
    return fields


def has_evidence(text):
    return any(r.search(text) for r in EVIDENCE_RES) and not PLACEHOLDER_RE.search(text)


def validate(text):
    errors = []
    fields = parse_fields(text)
    for required in ("结果", "入口", "验证", "未验证"):
        if required not in fields:
            errors.append("缺少必填项: " + required)
    if errors:
        return errors
    result = fields["结果"]["value"]
    if not any(k in result for k in ("已完成", "部分完成", "未完成")):
        errors.append("结果必须写明 已完成 / 部分完成 / 未完成，并说明用户现在能否使用")
    entry = fields["入口"]["value"]
    if "已完成" in result or "部分完成" in result:
        if not entry or PLACEHOLDER_RE.search(entry):
            errors.append("入口缺失: 完成的工作必须给出 URL、路径或版本号")
        verify_items = ([fields["验证"]["value"]] if fields["验证"]["value"] else []) + fields["验证"]["bullets"]
        verify_items = [i for i in verify_items if i]
        if not verify_items:
            errors.append("验证为空: 声称完成必须至少有一条验证记录")
        for item in verify_items:
            if not has_evidence(item):
                errors.append("验证缺证据: " + item[:60] + " (需要命令、输出、截图、链接、版本或摘要至少其一)")
    return errors


GOOD = """## 交付回执
- 结果：已完成，用户现在可用
- 入口：https://example.invalid/app 版本 v1.2.0
- 验证：
  - `python3 scripts/check.py` 输出 PASS, exit code 0
  - 浏览器实测登录流程，截图见 receipt-home.png
- 未验证与剩余：无
"""

BAD_NO_EVIDENCE = """## 交付回执
- 结果：已完成
- 入口：见上
- 验证：
  - 全部功能都测试通过了
- 未验证与剩余：无
"""

BAD_MISSING_FIELD = """## 交付回执
- 结果：已完成
- 验证：
  - `pytest` PASS, exit code 0
"""

SELFTEST = [
    ("good receipt passes", GOOD, 0),
    ("claim without evidence fails", BAD_NO_EVIDENCE, 1),
    ("missing field fails", BAD_MISSING_FIELD, 1),
]


def selftest():
    failed = 0
    for label, text, expected in SELFTEST:
        got = 1 if validate(text) else 0
        status = "PASS" if got == expected else "FAIL"
        failed += status == "FAIL"
        print(status + ": " + label)
    if failed:
        print("selftest: %d case(s) failed" % failed)
        return 1
    print("selftest: all %d cases passed" % len(SELFTEST))
    return 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    text = Path(argv[1]).read_text(encoding="utf-8")
    errors = validate(text)
    if errors:
        print("\n".join("FAIL: " + e for e in errors))
        return 1
    print("PASS: receipt has required fields and checkable evidence")
    print("NOTE: this validates evidence format only, not that the work is correct")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
