#!/usr/bin/env python3
from __future__ import annotations

import argparse
import functools
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - exercised through CLI tests
    Draft202012Validator = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"
MANIFEST_PATH = Path("governance/scaffold.manifest.json")
PROFILE_LABEL = "governance/starter.profile.json"

FAMILY_LAYER_COMPATIBILITY = {
    "policy_or_rules": {"truth_source"},
    "object": {"truth_source"},
    "workflow": {"truth_source"},
    "skill": {"truth_source"},
    "agent": {"truth_source"},
    "execution_object": {"execution_object"},
    "status_projection": {"status_projection"},
    "display_projection": {"display_projection"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate files-driven starter assets such as manifest, profile, registry, and routes.",
    )
    parser.add_argument("project_root", help="Root directory of a files engine starter or downstream project.")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@functools.lru_cache(maxsize=None)
def schema_validator(schema_filename: str) -> Draft202012Validator:
    if Draft202012Validator is None:
        raise RuntimeError("jsonschema package is required to validate files engine scaffolds")
    schema = load_json(SCHEMA_ROOT / schema_filename)
    return Draft202012Validator(schema)


def format_schema_path(path: list[object]) -> str:
    if not path:
        return "$"
    buffer = "$"
    for item in path:
        if isinstance(item, int):
            buffer += f"[{item}]"
        else:
            buffer += f".{item}"
    return buffer


def validate_against_schema(
    instance: dict,
    schema_filename: str,
    label: str,
    errors: list[str],
) -> None:
    validator = schema_validator(schema_filename)
    for issue in sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path)):
        errors.append(
            f"{label}: schema violation at {format_schema_path(list(issue.absolute_path))}: {issue.message}"
        )


def entry_annotations(entry: dict) -> dict:
    annotations = entry.get("annotations")
    return annotations if isinstance(annotations, dict) else {}


def tracked_files(project_root: Path, manifest: dict, errors: list[str]) -> list[Path]:
    tracked: dict[str, Path] = {}

    for relative in manifest["required_paths"]:
        path = project_root / relative
        if not path.exists():
            errors.append(f"governance/scaffold.manifest.json: required path missing `{relative}`")
            continue
        if path.is_file():
            tracked[relative] = path

    for pattern in manifest["tracked_globs"]:
        matches = sorted(path for path in project_root.glob(pattern) if path.is_file())
        if not matches:
            errors.append(f"governance/scaffold.manifest.json: tracked_glob matched nothing `{pattern}`")
            continue
        for match in matches:
            tracked[match.relative_to(project_root).as_posix()] = match

    return [tracked[key] for key in sorted(tracked)]


def load_declared_json(
    project_root: Path,
    relative_path: str | None,
    schema_filename: str,
    errors: list[str],
) -> dict | None:
    if not relative_path:
        return None
    path = project_root / relative_path
    if not path.exists():
        errors.append(f"{relative_path} not found")
        return None
    payload = load_json(path)
    validate_against_schema(payload, schema_filename, relative_path, errors)
    return payload


def ensure_required_paths(
    project_root: Path,
    errors: list[str],
) -> tuple[dict | None, dict | None, dict | None, dict | None]:
    manifest_path = project_root / MANIFEST_PATH
    if not manifest_path.exists():
        errors.append("governance/scaffold.manifest.json not found")
        return None, None, None, None

    manifest = load_json(manifest_path)
    validate_against_schema(manifest, "scaffold.manifest.schema.json", "governance/scaffold.manifest.json", errors)

    profile = load_declared_json(project_root, manifest.get("profile_path"), "starter.profile.schema.json", errors)
    registry = load_declared_json(project_root, manifest.get("registry_path"), "files.registry.schema.json", errors)
    routes = load_declared_json(project_root, manifest.get("routes_path"), "intent.routes.schema.json", errors)

    expected_project_id = manifest.get("project_id")
    if profile is not None and profile.get("project_id") != expected_project_id:
        errors.append("governance/starter.profile.json and governance/scaffold.manifest.json must share the same project_id")
    if registry is not None and registry.get("project_id") != expected_project_id:
        errors.append("governance/files.registry.json and governance/scaffold.manifest.json must share the same project_id")
    if routes is not None and routes.get("project_id") != expected_project_id:
        errors.append("governance/intent.routes.json and governance/scaffold.manifest.json must share the same project_id")

    return manifest, profile, registry, routes


def validate_registry_entries(
    project_root: Path,
    manifest: dict,
    profile: dict,
    registry: dict,
    routes: dict,
    errors: list[str],
) -> None:
    entries = registry.get("entries", [])
    routes_payload = routes.get("routes", [])

    by_id: dict[str, dict] = {}
    by_path: dict[str, dict] = {}
    route_ids: set[str] = set()

    for route in routes_payload:
        route_id = route.get("route_id")
        if route_id in route_ids:
            errors.append(f"governance/intent.routes.json: duplicate route_id `{route_id}`")
            continue
        route_ids.add(route_id)

    for index, entry in enumerate(entries, start=1):
        file_id = entry["file_id"]
        relative_path = entry["path"]
        layer = entry["layer"]
        family = entry["family"]

        if file_id in by_id:
            errors.append(f"governance/files.registry.json: duplicate file_id `{file_id}`")
        else:
            by_id[file_id] = entry

        if relative_path in by_path:
            errors.append(f"governance/files.registry.json: duplicate path `{relative_path}`")
        else:
            by_path[relative_path] = entry

        path = project_root / relative_path
        if not path.exists():
            errors.append(
                f"governance/files.registry.json: entries[{index}] points to missing path `{relative_path}`"
            )

        if layer not in FAMILY_LAYER_COMPATIBILITY.get(family, set()):
            errors.append(
                "governance/files.registry.json: "
                f"`{file_id}` uses incompatible family/layer `{family}` + `{layer}`"
            )

    tracked = {
        path.relative_to(project_root).as_posix()
        for path in tracked_files(project_root, manifest, errors)
    }
    registered = set(by_path)

    missing = sorted(tracked - registered)
    if missing:
        errors.append(
            "governance/files.registry.json: tracked files must be registered: "
            + ", ".join(missing)
        )

    for route in routes_payload:
        route_label = f"route `{route['route_id']}`"
        refs = [
            route["entrypoint_file_id"],
            *route["required_file_ids"],
            *route["write_targets"],
        ]
        for file_id in refs:
            if file_id not in by_id:
                errors.append(f"governance/intent.routes.json: {route_label} references unknown file_id `{file_id}`")

    for requirement in profile.get("required_work_posts", []):
        work_post = requirement["work_post"]
        expected_path = requirement["path"]
        matched = [
            entry
            for entry in entries
            if entry["work_post"] == work_post and entry["path"] == expected_path
        ]
        if not matched:
            errors.append(
                "governance/starter.profile.json: required work_post/path pair missing in governance/files.registry.json: "
                f"`{work_post}` -> `{expected_path}`"
            )

    for family in profile.get("required_family_entries", []):
        if not any(entry["family"] == family for entry in entries):
            errors.append(
                "governance/starter.profile.json: governance/files.registry.json must contain at least one "
                f"`{family}` entry"
            )

    for expectation in profile.get("required_entry_expectations", []):
        expected_path = expectation["path"]
        matched = by_path.get(expected_path)
        if matched is None:
            errors.append(
                "governance/starter.profile.json: expected registered path missing from governance/files.registry.json: "
                f"`{expected_path}`"
            )
            continue

        if matched["family"] != expectation["family"]:
            errors.append(
                "governance/starter.profile.json: path expectation mismatch for "
                f"`{expected_path}`: expected family `{expectation['family']}`, got `{matched['family']}`"
            )

        if matched["layer"] != expectation["layer"]:
            errors.append(
                "governance/starter.profile.json: path expectation mismatch for "
                f"`{expected_path}`: expected layer `{expectation['layer']}`, got `{matched['layer']}`"
            )

        expected_work_post = expectation.get("work_post")
        if expected_work_post and matched["work_post"] != expected_work_post:
            errors.append(
                "governance/starter.profile.json: path expectation mismatch for "
                f"`{expected_path}`: expected work_post `{expected_work_post}`, got `{matched['work_post']}`"
            )

        for key, value in expectation.get("annotations", {}).items():
            actual = entry_annotations(matched).get(key)
            if actual != value:
                errors.append(
                    "governance/starter.profile.json: path expectation mismatch for "
                    f"`{expected_path}`: expected annotations.{key} = `{value}`, got `{actual}`"
                )


def load_scaffold_assets(project_root: Path) -> tuple[dict | None, dict | None, dict | None, dict | None, list[str]]:
    errors: list[str] = []
    manifest, profile, registry, routes = ensure_required_paths(project_root, errors)
    if manifest is not None and profile is not None and registry is not None and routes is not None:
        validate_registry_entries(project_root, manifest, profile, registry, routes, errors)
    return manifest, profile, registry, routes, errors


def categorize_error(error: str) -> str:
    if error.startswith("governance/scaffold.manifest.json"):
        return "manifest"
    if error.startswith("governance/starter.profile.json"):
        return "starter_profile"
    if error.startswith("governance/files.registry.json"):
        return "registry"
    if error.startswith("governance/intent.routes.json"):
        return "routes"
    return "scaffold"


def build_findings(errors: list[str]) -> list[dict]:
    return [
        {
            "category": categorize_error(error),
            "message": error,
        }
        for error in errors
    ]


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve()

    if not project_root.exists():
        print(f"error: project root does not exist: `{project_root}`", file=sys.stderr)
        return 1

    _, _, _, _, errors = load_scaffold_assets(project_root)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"files engine scaffold is valid: {project_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
