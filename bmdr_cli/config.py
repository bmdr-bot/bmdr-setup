"""Configuration management for BMDR CLI."""

import json
import os
from pathlib import Path
from typing import Any, Optional

DEFAULT_CONFIG = {
    "github_org": "bmdr-bot",
    "default_branch": "main",
    "templates_dir": "templates",
    "skills_dir": "skills",
    "projects_base_dir": "~/projects",
    "deployment_targets": {
        "docker": {"type": "docker-compose", "file": "docker-compose.prod.yml"},
        "kubernetes": {"type": "kustomize", "dir": "k8s"},
        "cloudflare": {"type": "tunnel", "enabled": True},
    },
    "ci_cd": {
        "provider": "github-actions",
        "workflows": ["ci.yml", "deploy.yml"],
    },
    "project_defaults": {
        "license": "MIT",
        "python_version": "3.11",
        "fastapi_version": "0.109.0",
        "include_tests": True,
        "include_docker": True,
        "include_k8s": True,
        "include_cloudflare": True,
    },
}


class Config:
    """BMDR CLI configuration."""

    CONFIG_DIR = Path.home() / ".config" / "bmdr"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        self._data = {}
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE) as f:
                self._data = json.load(f)
        else:
            self._data = DEFAULT_CONFIG.copy()
            self.save()

    def save(self) -> None:
        """Save configuration to file."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        keys = key.split(".")
        data = self._data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
        self.save()

    @property
    def projects_dir(self) -> Path:
        """Get projects base directory."""
        return Path(self.get("projects_base_dir", "~/projects")).expanduser()

    @property
    def github_org(self) -> str:
        """Get GitHub organization."""
        return self.get("github_org", "bmdr-bot")


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
