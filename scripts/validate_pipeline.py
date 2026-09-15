#!/usr/bin/env python3
"""Validate enviro_veille strategic pipeline artifacts.

Legacy artifacts are checked and reported as warnings so the validator can be
introduced without rewriting history. Artifacts declaring schema_version=2.0
are strict: schema violations, broken references, missing lineage and invalid
BE offer gating fail the command.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - explicit developer feedback
    raise SystemExit(
        "Missing dependency 'jsonschema'. Run: pip install -r requirements-dev.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
V2 = "2.0"

STAGES = {
    "tendances": ("config/schemas/tendances.schema.json", "trends"),
    "opportunites": ("config/schemas/opportunites.schema.json", "opportunities"),
    "validation": ("config/schemas/validation.schema.json", "validations"),
    "offres": ("config/schemas/offres.schema.json", "offers"),
}

V2_TREND_LINEAGE = {
    "canonical_id",
    "first_seen",
    "last_seen",
    "previous_period_id",
    "previous_status",
    "previous_acceleration_score",
    "score_delta",
    "evolution_note",
}
V2_OPPORTUNITY_LINEAGE = {
    "canonical_id",
    "first_seen",
    "last_seen",
    "previous_period_id",
    "previous_confidence",
    "confidence_delta",
    "evolution_note",
}

READY_VERDICTS = {"signale_fort", "signale_modere"}
QUALIFYING_TYPES = {"appel_offres", "financement", "budget", "demande_explicite"}


class Reporter:
    def __init__(self, strict_legacy: bool = False) -> None:
        self.strict_legacy = strict_legacy
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def issue(self, message: str, *, strict: bool) -> None:
        if strict or self.strict_legacy:
            self.errors.append(message)
        else:
            self.warnings.append(message)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_v2(document: dict[str, Any]) -> bool:
    return document.get("schema_version") == V2


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def json_files(directory: str) -> list[Path]:
    base = ROOT / directory
    return sorted(base.glob("**/*.json")) if base.exists() else []


def unique_values(
    reporter: Reporter,
    path: Path,
    objects: Iterable[dict[str, Any]],
    key: str,
    *,
    strict: bool,
) -> None:
    seen: set[str] = set()
    for obj in objects:
        value = obj.get(key)
        if not value:
            continue
        if value in seen:
            reporter.issue(f"{rel(path)}: duplicate {key}={value!r}", strict=strict)
        seen.add(value)


def schema_validate(reporter: Reporter, path: Path, schema_path: Path) -> dict[str, Any] | None:
    try:
        document = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        reporter.errors.append(f"{rel(path)}: invalid JSON: {exc}")
        return None

    if not isinstance(document, dict):
        reporter.errors.append(f"{rel(path)}: root must be a JSON object")
        return None

    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    strict = is_v2(document)
    for error in sorted(validator.iter_errors(document), key=lambda err: list(err.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        reporter.issue(
            f"{rel(path)}: schema error at {location}: {error.message}",
            strict=strict,
        )
    return document


def build_daily_index(reporter: Reporter) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in json_files("data/daily"):
        try:
            document = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            reporter.errors.append(f"{rel(path)}: invalid daily JSON: {exc}")
            continue
        for item in document.get("items", []):
            item_id = item.get("id")
            if not item_id:
                continue
            if item_id in index:
                reporter.errors.append(f"Duplicate daily item id {item_id!r}")
            index[item_id] = item
    return index


def daily_urls(item: dict[str, Any]) -> set[str]:
    urls = set(item.get("urls") or [])
    primary = item.get("primary_source") or {}
    if primary.get("url"):
        urls.add(primary["url"])
    for source in item.get("secondary_sources") or []:
        if source.get("url"):
            urls.add(source["url"])
    return urls


def require_v2_fields(
    reporter: Reporter,
    path: Path,
    obj: dict[str, Any],
    fields: set[str],
    context: str,
) -> None:
    missing = sorted(field for field in fields if field not in obj)
    if missing:
        reporter.errors.append(
            f"{rel(path)}: {context} missing v2 fields: {', '.join(missing)}"
        )


def resolve_repo_path(reference: str | None) -> Path | None:
    if not reference:
        return None
    candidate = (ROOT / reference).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def validate_trends(
    reporter: Reporter,
    path: Path,
    document: dict[str, Any],
    daily_index: dict[str, dict[str, Any]],
) -> None:
    strict = is_v2(document)
    trends = document.get("trends") or []
    unique_values(reporter, path, trends, "id", strict=strict)
    unique_values(reporter, path, trends, "canonical_id", strict=strict)

    for trend in trends:
        trend_id = trend.get("id", "<missing-id>")
        if strict:
            require_v2_fields(reporter, path, trend, V2_TREND_LINEAGE, f"trend {trend_id}")
            previous_score = trend.get("previous_acceleration_score")
            delta = trend.get("score_delta")
            if previous_score is None and delta is not None:
                reporter.errors.append(
                    f"{rel(path)}: trend {trend_id}: score_delta must be null when previous_acceleration_score is null"
                )
            if previous_score is not None and delta != trend.get("acceleration_score", 0) - previous_score:
                reporter.errors.append(
                    f"{rel(path)}: trend {trend_id}: score_delta does not match current - previous score"
                )

        for evidence in trend.get("evidence") or []:
            item_id = evidence.get("daily_item_id")
            if not item_id or item_id not in daily_index:
                reporter.issue(
                    f"{rel(path)}: trend {trend_id}: unknown daily_item_id {item_id!r}",
                    strict=strict,
                )
                continue
            url = evidence.get("url")
            if url and url not in daily_urls(daily_index[item_id]):
                reporter.issue(
                    f"{rel(path)}: trend {trend_id}: evidence URL for {item_id} is not present in the daily item",
                    strict=strict,
                )


def load_reference(
    reporter: Reporter,
    owner_path: Path,
    reference: str | None,
    *,
    strict: bool,
) -> dict[str, Any] | None:
    target = resolve_repo_path(reference)
    if target is None or not target.is_file():
        reporter.issue(
            f"{rel(owner_path)}: referenced file not found or unsafe: {reference!r}",
            strict=strict,
        )
        return None
    try:
        loaded = load_json(target)
    except (OSError, json.JSONDecodeError) as exc:
        reporter.issue(
            f"{rel(owner_path)}: cannot read referenced file {reference!r}: {exc}",
            strict=strict,
        )
        return None
    return loaded if isinstance(loaded, dict) else None


def validate_opportunities(reporter: Reporter, path: Path, document: dict[str, Any]) -> None:
    strict = is_v2(document)
    opportunities = document.get("opportunities") or []
    unique_values(reporter, path, opportunities, "id", strict=strict)
    unique_values(reporter, path, opportunities, "canonical_id", strict=strict)

    reference = (document.get("based_on_trends") or {}).get("file")
    trends_doc = load_reference(reporter, path, reference, strict=strict)
    trend_ids = {trend.get("id") for trend in (trends_doc or {}).get("trends", [])}

    for opportunity in opportunities:
        opp_id = opportunity.get("id", "<missing-id>")
        if strict:
            require_v2_fields(
                reporter, path, opportunity, V2_OPPORTUNITY_LINEAGE, f"opportunity {opp_id}"
            )
            previous_confidence = opportunity.get("previous_confidence")
            delta = opportunity.get("confidence_delta")
            if previous_confidence is None and delta is not None:
                reporter.errors.append(
                    f"{rel(path)}: opportunity {opp_id}: confidence_delta must be null when previous_confidence is null"
                )
            if previous_confidence is not None and delta != opportunity.get("confidence", 0) - previous_confidence:
                reporter.errors.append(
                    f"{rel(path)}: opportunity {opp_id}: confidence_delta does not match current - previous confidence"
                )
        for trend_id in opportunity.get("linked_trends") or []:
            if trends_doc is not None and trend_id not in trend_ids:
                reporter.issue(
                    f"{rel(path)}: opportunity {opp_id}: linked trend {trend_id!r} absent from {reference}",
                    strict=strict,
                )


def validate_market(reporter: Reporter, path: Path, document: dict[str, Any]) -> None:
    strict = is_v2(document)
    validations = document.get("validations") or []
    unique_values(reporter, path, validations, "opportunity_id", strict=strict)

    reference = (document.get("based_on_opportunities") or {}).get("file")
    opp_doc = load_reference(reporter, path, reference, strict=strict)
    opp_ids = {opp.get("id") for opp in (opp_doc or {}).get("opportunities", [])}

    for validation in validations:
        opp_id = validation.get("opportunity_id", "<missing-id>")
        if opp_doc is not None and opp_id not in opp_ids:
            reporter.issue(
                f"{rel(path)}: validation references unknown opportunity {opp_id!r}",
                strict=strict,
            )
        if strict:
            for index, evidence in enumerate(validation.get("evidence") or [], start=1):
                if "demand_signal" not in evidence:
                    reporter.errors.append(
                        f"{rel(path)}: validation {opp_id} evidence #{index} missing v2 demand_signal"
                    )


def evidence_key(evidence: dict[str, Any]) -> tuple[Any, Any, Any]:
    return evidence.get("title"), evidence.get("url"), evidence.get("type")


def qualifying_market_evidence(evidence: dict[str, Any]) -> bool:
    evidence_type = evidence.get("type")
    signal = evidence.get("demand_signal")
    if evidence_type in QUALIFYING_TYPES and signal in {"direct", "externalisable"}:
        return True
    return evidence_type == "obligation" and signal == "externalisable"


def validate_offers(reporter: Reporter, path: Path, document: dict[str, Any]) -> None:
    strict = is_v2(document)
    offers = document.get("offers") or []
    unique_values(reporter, path, offers, "id", strict=strict)

    reference = (document.get("based_on_validation") or {}).get("file")
    validation_doc = load_reference(reporter, path, reference, strict=strict)
    validation_by_opp = {
        item.get("opportunity_id"): item
        for item in (validation_doc or {}).get("validations", [])
        if item.get("opportunity_id")
    }

    for offer in offers:
        offer_id = offer.get("id", "<missing-id>")
        opp_id = offer.get("linked_opportunity_id")
        validation = validation_by_opp.get(opp_id)
        if validation_doc is not None and validation is None:
            reporter.issue(
                f"{rel(path)}: offer {offer_id}: no validation for opportunity {opp_id!r}",
                strict=strict,
            )
            continue
        if not strict or validation is None:
            continue

        required = {"linked_validation_verdict", "price_signal", "first_action_this_month"}
        require_v2_fields(reporter, path, offer, required, f"offer {offer_id}")

        verdict = validation.get("verdict")
        if offer.get("linked_validation_verdict") != verdict:
            reporter.errors.append(
                f"{rel(path)}: offer {offer_id}: linked_validation_verdict does not match validation"
            )

        validation_evidence = validation.get("evidence") or []
        allowed_refs = {evidence_key(ev) for ev in validation_evidence}
        for ref_item in offer.get("evidence_refs") or []:
            if evidence_key(ref_item) not in allowed_refs:
                reporter.errors.append(
                    f"{rel(path)}: offer {offer_id}: evidence_ref is not an exact validation evidence: {ref_item.get('title')!r}"
                )

        if offer.get("status") == "pret_a_prototyper":
            if verdict not in READY_VERDICTS:
                reporter.errors.append(
                    f"{rel(path)}: offer {offer_id}: pret_a_prototyper requires signale_fort or signale_modere"
                )
            if (offer.get("be_fit") or 0) < 4:
                reporter.errors.append(
                    f"{rel(path)}: offer {offer_id}: pret_a_prototyper requires be_fit >= 4"
                )
            if not any(qualifying_market_evidence(ev) for ev in validation_evidence):
                reporter.errors.append(
                    f"{rel(path)}: offer {offer_id}: pret_a_prototyper lacks direct/externalisable market evidence"
                )

        if offer.get("status") != "hors_metier_be" and len(offer.get("deliverables") or []) < 2:
            reporter.errors.append(
                f"{rel(path)}: offer {offer_id}: actionable BE offers require at least 2 concrete deliverables"
            )

        price_signal = offer.get("price_signal")
        if price_signal and price_signal != "non chiffré":
            if not any((ev.get("amount_or_scale") or "").strip() for ev in validation_evidence):
                reporter.errors.append(
                    f"{rel(path)}: offer {offer_id}: priced price_signal has no amount_or_scale in validation evidence"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate enviro_veille pipeline artifacts")
    parser.add_argument(
        "--strict-legacy",
        action="store_true",
        help="Treat schema/reference issues in pre-v2 artifacts as errors instead of warnings.",
    )
    args = parser.parse_args()

    reporter = Reporter(strict_legacy=args.strict_legacy)
    daily_index = build_daily_index(reporter)

    documents: dict[Path, dict[str, Any]] = {}
    for stage, (schema_rel, _) in STAGES.items():
        schema_path = ROOT / schema_rel
        for path in json_files(stage):
            document = schema_validate(reporter, path, schema_path)
            if document is not None:
                documents[path] = document

    for path, document in documents.items():
        top = path.relative_to(ROOT).parts[0]
        if top == "tendances":
            validate_trends(reporter, path, document, daily_index)
        elif top == "opportunites":
            validate_opportunities(reporter, path, document)
        elif top == "validation":
            validate_market(reporter, path, document)
        elif top == "offres":
            validate_offers(reporter, path, document)

    print(
        f"Validated {len(documents)} strategic JSON files and {len(daily_index)} daily items."
    )
    if reporter.warnings:
        print(f"\nWarnings ({len(reporter.warnings)} legacy/non-blocking):")
        for warning in reporter.warnings:
            print(f"  - {warning}")
    if reporter.errors:
        print(f"\nErrors ({len(reporter.errors)} blocking):", file=sys.stderr)
        for error in reporter.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("\nPipeline validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
