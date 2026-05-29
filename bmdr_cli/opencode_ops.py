"""OpenCode operations for BMDR CLI."""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


class OpenCodeOps:
    """OpenCode CLI operations."""

    def __init__(self, binary: Optional[str] = None):
        self.binary = binary or self._find_binary()
        if not self.binary:
            raise RuntimeError(
                "OpenCode not found. Install with: npm i -g opencode-ai@latest"
            )

    def _find_binary(self) -> Optional[str]:
        """Find opencode binary."""
        try:
            result = subprocess.run(
                ["which", "opencode"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            for path in [
                "/usr/local/bin/opencode",
                "/usr/bin/opencode",
                os.path.expanduser("~/.opencode/bin/opencode"),
                os.path.expanduser("~/.local/bin/opencode"),
            ]:
                if os.path.exists(path):
                    return path
            return None

    def version(self) -> str:
        """Get OpenCode version."""
        result = subprocess.run(
            [self.binary, "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def auth_list(self) -> List[Dict[str, Any]]:
        """List authenticated providers."""
        try:
            result = subprocess.run(
                [self.binary, "auth", "list", "--format", "json"],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return []

    def run_task(
        self,
        prompt: str,
        workdir: Path,
        files: Optional[List[Path]] = None,
        model: Optional[str] = None,
        thinking: bool = False,
        timeout: int = 300,
    ) -> Dict[str, Any]:
        """Run a one-shot OpenCode task."""
        cmd = [self.binary, "run", prompt]

        if files:
            for f in files:
                cmd.extend(["-f", str(f)])

        if model:
            cmd.extend(["--model", model])

        if thinking:
            cmd.append("--thinking")

        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0,
        }

    def review_pr(
        self,
        pr_number: int,
        workdir: Path,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Review a pull request with OpenCode."""
        cmd = [self.binary, "pr", str(pr_number)]

        if model:
            cmd.extend(["--model", model])

        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=600,
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0,
        }

    def start_session(
        self,
        workdir: Path,
        title: Optional[str] = None,
        agent: Optional[str] = None,
        model: Optional[str] = None,
    ) -> subprocess.Popen:
        """Start an interactive OpenCode session."""
        args: List[str] = [self.binary]

        if title:
            args.append("--title")
            args.append(title)

        if agent:
            args.append("--agent")
            args.append(agent)

        if model:
            args.append("--model")
            args.append(model)

        return subprocess.Popen(
            args,
            cwd=workdir,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List OpenCode sessions."""
        try:
            result = subprocess.run(
                [self.binary, "session", "list", "--format", "json"],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return []

    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get OpenCode usage stats."""
        try:
            result = subprocess.run(
                [self.binary, "stats", "--days", str(days), "--format", "json"],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return {}


def get_opencode_ops() -> OpenCodeOps:
    """Get OpenCode operations instance."""
    return OpenCodeOps()
