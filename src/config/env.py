"""
Environment configuration for local (.env) and cloud (process env / GitHub Secrets).

Priority (highest first):
  1. Variables already set in the process (e.g. GitHub Actions `env:` / `secrets`)
  2. Values from `.env` file if it exists (local development only)
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_app_env(project_root: Path | None = None) -> bool:
    """
    Load `.env` when present. Never requires the file to exist.

    Uses override=False so CI secrets are not overwritten by a missing/empty .env.
    """
    root = project_root or PROJECT_ROOT
    env_file = root / ".env"
    if env_file.is_file():
        return load_dotenv(env_file, override=False)
    return False


def require_env_vars(*names: str, context: str = "runtime") -> dict[str, str]:
    """
    Ensure required variables are set. Returns name -> value for each.

    Raises:
        EnvironmentError: With guidance for local .env vs GitHub Secrets.
    """
    missing = [name for name in names if not os.getenv(name)]
    if not missing:
        return {name: os.environ[name] for name in names}

    missing_list = ", ".join(missing)
    raise EnvironmentError(
        f"Missing required environment variable(s): {missing_list}\n\n"
        "Local development:\n"
        "  - Copy .env.example to .env and set the values\n\n"
        "GitHub Actions:\n"
        "  - Repo → Settings → Secrets and variables → Actions → Repository secrets\n"
        "  - Add secrets with the exact names (e.g. OPENAI_API_KEY, TAVILY_API_KEY)\n"
        "  - Re-run the workflow (secrets are injected as env vars, not from .env)\n\n"
        f"Context: {context}"
    )


def env_status(*names: str) -> dict[str, bool]:
    """Check which variables are set (for logging; never prints values)."""
    return {name: bool(os.getenv(name)) for name in names}
