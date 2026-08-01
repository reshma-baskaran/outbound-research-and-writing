from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_TEMPLATE = REPOSITORY_ROOT / "workspace-template"
TEMPLATES_ROOT = REPOSITORY_ROOT / "templates"


def configured_workspace(config_path: Path) -> Path:
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"configuration file does not exist: {config_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"configuration file is not valid JSON: {config_path}") from error

    raw_path = config.get("workspace_path") if isinstance(config, dict) else None
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("configuration must contain a non-empty string: workspace_path")
    return Path(raw_path).expanduser()


def _safe_target(target: Path) -> Path:
    resolved = target.expanduser().resolve()
    repository = REPOSITORY_ROOT.resolve()
    if resolved == repository or repository in resolved.parents:
        raise ValueError("choose a workspace path outside this public repository")
    if resolved == WORKSPACE_TEMPLATE.resolve() or WORKSPACE_TEMPLATE.resolve() in resolved.parents:
        raise ValueError("the workspace path cannot be inside workspace-template")
    return resolved


def _copy_tree(source_root: Path, destination_root: Path, *, overwrite: bool) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    for source in sorted(source_root.rglob("*")):
        destination = destination_root / source.relative_to(source_root)
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        relative = str(destination.relative_to(destination_root))
        if destination.exists() and not overwrite:
            skipped.append(relative)
            continue
        shutil.copy2(source, destination)
        created.append(relative)
    return created, skipped


def install_workspace(target: Path, *, overwrite: bool = False) -> tuple[list[str], list[str]]:
    if not WORKSPACE_TEMPLATE.is_dir():
        raise ValueError(f"workspace template is missing: {WORKSPACE_TEMPLATE}")
    if not TEMPLATES_ROOT.is_dir():
        raise ValueError(f"template directory is missing: {TEMPLATES_ROOT}")
    if target.exists() and not target.is_dir():
        raise ValueError(f"workspace path is not a directory: {target}")

    target.mkdir(parents=True, exist_ok=True)
    created, skipped = _copy_tree(WORKSPACE_TEMPLATE, target, overwrite=overwrite)
    template_created, template_skipped = _copy_tree(
        TEMPLATES_ROOT,
        target / "templates",
        overwrite=overwrite,
    )
    return created + template_created, skipped + [f"templates/{item}" for item in template_skipped]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a blank outbound research and writing workspace.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--workspace", type=Path, help="destination path for the workspace")
    target.add_argument("--config", type=Path, help="local JSON config containing workspace_path")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace existing template files; never deletes files",
    )
    args = parser.parse_args()

    try:
        requested = args.workspace if args.workspace is not None else configured_workspace(args.config)
        destination = _safe_target(requested)
        created, skipped = install_workspace(destination, overwrite=args.overwrite)
    except ValueError as error:
        parser.error(str(error))

    print(f"Workspace ready: {destination}")
    print(f"Created: {len(created)} files")
    if skipped:
        print(f"Skipped existing files: {len(skipped)}")
    print("Use the skill to research and draft; run the validator before review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
