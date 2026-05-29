"""Template rendering engine for BMDR CLI."""

import shutil
from pathlib import Path
from string import Template
from typing import Any, Dict


class TemplateEngine:
    """Render templates with variable substitution."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = Path(templates_dir)

    def render_string(self, template_string: str, variables: Dict[str, Any]) -> str:
        """Render a template string."""
        return Template(template_string).safe_substitute(variables)

    def render_file(self, template_path: Path, variables: Dict[str, Any]) -> str:
        """Render a template file."""
        with open(template_path) as f:
            content = f.read()
        return self.render_string(content, variables)

    def copy_template(self, template_name: str, dest_dir: Path, variables: Dict[str, Any]) -> None:
        """Copy a template directory, rendering files as needed."""
        src_dir = self.templates_dir / template_name
        if not src_dir.exists():
            raise ValueError(f"Template '{template_name}' not found")

        for src_file in src_dir.rglob("*"):
            if src_file.is_file():
                # Calculate relative path
                rel_path = src_file.relative_to(src_dir)
                dest_file = dest_dir / rel_path

                # Render filename
                dest_file = Path(str(dest_file).replace("__project_name__", variables.get("project_name", "project")))

                dest_file.parent.mkdir(parents=True, exist_ok=True)

                # Check if file should be rendered
                if src_file.suffix in [".md", ".yml", ".yaml", ".json", ".txt", ".sh", ".py", ".toml", ".cfg", ".ini"]:
                    content = self.render_file(src_file, variables)
                    with open(dest_file, "w") as f:
                        f.write(content)
                else:
                    shutil.copy2(src_file, dest_file)

    def list_templates(self) -> list:
        """List available templates."""
        if not self.templates_dir.exists():
            return []
        return [d.name for d in self.templates_dir.iterdir() if d.is_dir()]
