from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

VALID_STATUS = {"planned", "running", "succeeded", "failed", "inconclusive"}
CLOSED_STATUS = {"succeeded", "failed", "inconclusive"}
VALID_EVIDENCE = {"none", "self-test", "public-metrics", "verified-revenue"}
REQUIRED = {"id", "name", "status", "started_at", "revenue", "currency", "evidence_level", "report"}
ID_PATTERN = re.compile(r"^[0-9]{3}$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")


def manifests(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((root / "experiments").glob("*/experiment.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(item, dict):
            raise ValueError(f"{path}: manifest must contain a JSON object")
        records.append((path, item))
    return records


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    try:
        records = manifests(root)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]

    for path, item in records:
        missing = REQUIRED - item.keys()
        if missing:
            errors.append(f"{path}: missing {', '.join(sorted(missing))}")
            continue

        experiment_id = item["id"]
        if not isinstance(experiment_id, str) or not ID_PATTERN.fullmatch(experiment_id):
            errors.append(f"{path}: id must use three digits, for example 001")
        elif experiment_id in seen:
            errors.append(f"{path}: duplicate id {experiment_id}")
        seen.add(str(experiment_id))

        status = item["status"]
        if status not in VALID_STATUS:
            errors.append(f"{path}: invalid status {status}")

        started: date | None = None
        completed: date | None = None
        try:
            started = date.fromisoformat(item["started_at"])
            if item.get("completed_at"):
                completed = date.fromisoformat(item["completed_at"])
        except (TypeError, ValueError):
            errors.append(f"{path}: dates must use YYYY-MM-DD")
        if started and completed and completed < started:
            errors.append(f"{path}: completed_at cannot be before started_at")

        revenue = item["revenue"]
        if isinstance(revenue, bool) or not isinstance(revenue, (int, float)) or revenue < 0:
            errors.append(f"{path}: revenue must be a non-negative number")

        currency = item["currency"]
        if not isinstance(currency, str) or not CURRENCY_PATTERN.fullmatch(currency):
            errors.append(f"{path}: currency must be a three-letter uppercase code")

        evidence = item["evidence_level"]
        if evidence not in VALID_EVIDENCE:
            errors.append(f"{path}: invalid evidence_level")
        if isinstance(revenue, (int, float)) and not isinstance(revenue, bool) and revenue > 0 and evidence != "verified-revenue":
            errors.append(f"{path}: non-zero revenue requires verified-revenue evidence")
        if status == "succeeded" and evidence not in {"public-metrics", "verified-revenue"}:
            errors.append(f"{path}: succeeded status requires public-metrics or verified-revenue evidence")

        report = item["report"]
        if not isinstance(report, str) or not report.strip() or not (path.parent / report).is_file():
            errors.append(f"{path}: report does not exist: {report}")
        if status in CLOSED_STATUS and not item.get("completed_at"):
            errors.append(f"{path}: completed experiments need completed_at")
        if status in CLOSED_STATUS and not str(item.get("conclusion", "")).strip():
            errors.append(f"{path}: completed experiments need a conclusion")

    return errors


def summary(root: Path) -> dict[str, Any]:
    rows = [item for _, item in manifests(root)]
    completed = [item for item in rows if item["status"] in CLOSED_STATUS]
    currencies = sorted({item["currency"] for item in rows})
    verified_revenue = sum(
        float(item["revenue"])
        for item in rows
        if item.get("evidence_level") == "verified-revenue"
    )
    return {
        "experiments": len(rows),
        "completed": len(completed),
        "succeeded": sum(item["status"] == "succeeded" for item in rows),
        "failed": sum(item["status"] == "failed" for item in rows),
        "inconclusive": sum(item["status"] == "inconclusive" for item in rows),
        "verified_revenue": round(verified_revenue, 2),
        "currencies": currencies,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate AI Money Lab experiment records.")
    parser.add_argument("command", choices=["validate", "summary"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args(argv)
    errors = validate(args.root)
    if args.command == "validate":
        if errors:
            print("\n".join(errors))
            return 1
        print(f"OK: {len(manifests(args.root))} experiment manifests validated")
        return 0
    if errors:
        print(json.dumps({"errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(summary(args.root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
