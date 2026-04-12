#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER_ROOT = ROOT / "starters" / "minimal-files-engine"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap the official minimal files engine starter into a target directory.",
    )
    parser.add_argument("target_dir", help="Directory where the starter should be created.")
    parser.add_argument(
        "--project-id",
        default="example-project",
        help="Project id written into governance/files.registry.json and governance/intent.routes.json.",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rewrite_project_ids(target_dir: Path, project_id: str) -> None:
    manifest_path = target_dir / "governance" / "scaffold.manifest.json"
    profile_path = target_dir / "governance" / "starter.profile.json"
    registry_path = target_dir / "governance" / "files.registry.json"
    routes_path = target_dir / "governance" / "intent.routes.json"

    manifest = load_json(manifest_path)
    manifest["project_id"] = project_id
    manifest["manifest_id"] = f"scaffold.{project_id}"
    dump_json(manifest_path, manifest)

    profile = load_json(profile_path)
    profile["project_id"] = project_id
    profile["profile_id"] = f"starter.{project_id}"
    dump_json(profile_path, profile)

    registry = load_json(registry_path)
    registry["project_id"] = project_id
    registry["registry_id"] = f"registry.{project_id}"
    dump_json(registry_path, registry)

    routes = load_json(routes_path)
    routes["project_id"] = project_id
    routes["routes_id"] = f"routes.{project_id}"
    dump_json(routes_path, routes)


def main() -> int:
    args = parse_args()
    target_dir = Path(args.target_dir).expanduser().resolve()

    if not STARTER_ROOT.exists():
        print(f"error: starter not found at `{STARTER_ROOT}`", file=sys.stderr)
        return 1

    if target_dir.exists() and any(target_dir.iterdir()):
        print(
            "error: target directory must not already contain files; choose an empty directory",
            file=sys.stderr,
        )
        return 1

    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(STARTER_ROOT, target_dir)
    rewrite_project_ids(target_dir, args.project_id)

    print(f"bootstrapped files engine starter into {target_dir}")
    print("next: run `python3 scripts/validate_files_engine_scaffold.py <target_dir>`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
