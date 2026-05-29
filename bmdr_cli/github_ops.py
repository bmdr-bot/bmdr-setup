"""GitHub operations for BMDR CLI."""

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


class GitHubOps:
    """GitHub API operations."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if not self.token:
            raise ValueError("GitHub token not found. Set GITHUB_TOKEN environment variable.")

    def _request(self, method: str, path: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GitHub API request."""
        url = f"https://api.github.com{path}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        }

        req_data = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)

        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def get_user(self) -> str:
        """Get authenticated user login."""
        data = self._request("GET", "/user")
        return data["login"]

    def create_repo(self, name: str, description: str = "", private: bool = False, org: Optional[str] = None) -> Dict[str, Any]:
        """Create a new repository."""
        path = f"/orgs/{org}/repos" if org else "/user/repos"
        data = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": False,
        }
        return self._request("POST", path, data)

    def repo_exists(self, owner: str, repo: str) -> bool:
        """Check if repository exists."""
        try:
            self._request("GET", f"/repos/{owner}/{repo}")
            return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            raise

    def create_branch_protection(self, owner: str, repo: str, branch: str = "main") -> Dict[str, Any]:
        """Set up branch protection rules."""
        data = {
            "required_status_checks": {
                "strict": True,
                "contexts": ["ci/test", "ci/lint"],
            },
            "enforce_admins": False,
            "required_pull_request_reviews": {
                "required_approving_review_count": 1,
                "dismiss_stale_reviews": True,
            },
            "restrictions": None,
        }
        return self._request("PUT", f"/repos/{owner}/{repo}/branches/{branch}/protection", data)

    def create_secret(self, owner: str, repo: str, name: str, value: str) -> bool:
        """Create a repository secret."""
        # Get public key for encryption
        key_data = self._request("GET", f"/repos/{owner}/{repo}/actions/secrets/public-key")
        
        # Encrypt value
        from base64 import b64encode
        try:
            from nacl import encoding, public
            public_key = public.PublicKey(
                key_data["key"].encode("utf-8"), encoding.Base64Encoder
            )
            sealed_box = public.SealedBox(public_key)
            encrypted = sealed_box.encrypt(value.encode("utf-8"))
            encrypted_value = b64encode(encrypted).decode("utf-8")
        except ImportError:
            # Fallback: use gh CLI if available
            try:
                subprocess.run(
                    ["gh", "secret", "set", name, "--repo", f"{owner}/{repo}", "--body", value],
                    check=True,
                    capture_output=True,
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Warning: Cannot encrypt secret. Install PyNaCl or gh CLI.")
                return False

        # Create secret
        self._request(
            "PUT",
            f"/repos/{owner}/{repo}/actions/secrets/{name}",
            {"encrypted_value": encrypted_value, "key_id": key_data["key_id"]},
        )
        return True

    def create_pr(self, owner: str, repo: str, title: str, body: str, head: str, base: str = "main", draft: bool = False) -> Dict[str, Any]:
        """Create a pull request."""
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
            "draft": draft,
        }
        return self._request("POST", f"/repos/{owner}/{repo}/pulls", data)

    def request_reviewers(self, owner: str, repo: str, pr_number: int, reviewers: List[str]) -> Dict[str, Any]:
        """Request reviewers for a PR."""
        data = {"reviewers": reviewers}
        return self._request("POST", f"/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers", data)

    def merge_pr(self, owner: str, repo: str, pr_number: int, method: str = "squash") -> Dict[str, Any]:
        """Merge a pull request."""
        data = {"merge_method": method}
        return self._request("PUT", f"/repos/{owner}/{repo}/pulls/{pr_number}/merge", data)

    def get_pr(self, owner: str, repo: str, pr_number: int) -> Dict[str, Any]:
        """Get pull request details."""
        return self._request("GET", f"/repos/{owner}/{repo}/pulls/{pr_number}")

    def list_open_prs(self, owner: str, repo: str, head: Optional[str] = None) -> Any:
        """List open pull requests."""
        params = "?state=open"
        if head:
            params += f"&head={head}"
        return self._request("GET", f"/repos/{owner}/{repo}/pulls{params}")


def get_github_ops() -> GitHubOps:
    """Get GitHub operations instance."""
    return GitHubOps()
