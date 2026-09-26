"""Ecosystem detector for tool-dependabot-sentinel."""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class Ecosystem(str, Enum):
    PIP = "pip"
    NPM = "npm"
    GITHUB_ACTIONS = "github-actions"
    CARGO = "cargo"
    GOMOD = "gomod"
    DOCKER = "docker"

@dataclass
class ManifestLocation:
    ecosystem: Ecosystem
    directory: str
    manifest_file: str

def detect_ecosystems(root_dir: str | Path) -> List[ManifestLocation]:
    root = Path(root_dir).resolve()
    manifests: List[ManifestLocation] = []

    # 1. GitHub Actions (if .github/workflows exists)
    wf_dir = root / ".github" / "workflows"
    if wf_dir.is_dir() and any(wf_dir.glob("*.y*ml")):
        manifests.append(ManifestLocation(
            ecosystem=Ecosystem.GITHUB_ACTIONS,
            directory="/",
            manifest_file=".github/workflows"
        ))

    # 2. Python (pip / poetry)
    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists() or (root / "Pipfile").exists():
        manifests.append(ManifestLocation(
            ecosystem=Ecosystem.PIP,
            directory="/",
            manifest_file="requirements.txt / pyproject.toml"
        ))

    # 3. Node.js (npm / yarn / pnpm)
    if (root / "package.json").exists():
        manifests.append(ManifestLocation(
            ecosystem=Ecosystem.NPM,
            directory="/",
            manifest_file="package.json"
        ))

    # 4. Rust (cargo)
    if (root / "Cargo.toml").exists():
        manifests.append(ManifestLocation(
            ecosystem=Ecosystem.CARGO,
            directory="/",
            manifest_file="Cargo.toml"
        ))

    # 5. Go (gomod)
    if (root / "go.mod").exists():
        manifests.append(ManifestLocation(
            ecosystem=Ecosystem.GOMOD,
            directory="/",
            manifest_file="go.mod"
        ))

    # 6. Docker (Dockerfile)
    if (root / "Dockerfile").exists() or (root / "docker-compose.yml").exists():
        manifests.append(ManifestLocation(
            ecosystem=Ecosystem.DOCKER,
            directory="/",
            manifest_file="Dockerfile"
        ))

    return manifests
