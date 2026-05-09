from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkspacePaths:
    root: Path
    sessions_dir: Path
    config_file: Path


def default_workspace_root() -> Path:
    return Path.home() / ".meowbot"


def get_workspace_paths(root: Path | None = None) -> WorkspacePaths:
    root = (root or default_workspace_root()).expanduser()
    return WorkspacePaths(
        root=root,
        sessions_dir=root / "sessions",
        config_file=root / "config.json",
    )


def ensure_workspace(root: Path | None = None) -> WorkspacePaths:
    paths = get_workspace_paths(root=root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.sessions_dir.mkdir(parents=True, exist_ok=True)
    return paths

