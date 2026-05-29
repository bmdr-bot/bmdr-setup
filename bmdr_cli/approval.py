"""Approval gate system for BMDR CLI.

Implements human-in-the-loop approval for PRs and deployments,
especially critical for financial institutions requiring
manual approval for production changes.
"""

import json
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalType(Enum):
    PR_MERGE = "pr_merge"
    DEPLOY_STAGING = "deploy_staging"
    DEPLOY_PRODUCTION = "deploy_production"
    SECRET_CHANGE = "secret_change"
    INFRA_CHANGE = "infra_change"


@dataclass
class ApprovalRequest:
    id: str
    type: ApprovalType
    title: str
    description: str
    requester: str
    timestamp: float
    expires_at: float
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver: Optional[str] = None
    approval_timestamp: Optional[float] = None
    rejection_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ApprovalStore:
    """Store for approval requests."""

    def __init__(self, store_dir: Optional[Path] = None):
        self.store_dir = store_dir or Path.home() / ".config" / "bmdr" / "approvals"
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self._requests: Dict[str, ApprovalRequest] = {}
        self._load()

    def _get_path(self, request_id: str) -> Path:
        return self.store_dir / f"{request_id}.json"

    def _load(self) -> None:
        """Load all approval requests from disk."""
        for file in self.store_dir.glob("*.json"):
            try:
                with open(file) as f:
                    data = json.load(f)
                req = self._deserialize(data)
                self._requests[req.id] = req
            except Exception:
                continue

    def _save(self, request: ApprovalRequest) -> None:
        """Save approval request to disk."""
        path = self._get_path(request.id)
        with open(path, "w") as f:
            json.dump(self._serialize(request), f, indent=2)

    def _serialize(self, req: ApprovalRequest) -> Dict[str, Any]:
        return {
            "id": req.id,
            "type": req.type.value,
            "title": req.title,
            "description": req.description,
            "requester": req.requester,
            "timestamp": req.timestamp,
            "expires_at": req.expires_at,
            "status": req.status.value,
            "approver": req.approver,
            "approval_timestamp": req.approval_timestamp,
            "rejection_reason": req.rejection_reason,
            "metadata": req.metadata,
        }

    def _deserialize(self, data: Dict[str, Any]) -> ApprovalRequest:
        return ApprovalRequest(
            id=data["id"],
            type=ApprovalType(data["type"]),
            title=data["title"],
            description=data["description"],
            requester=data["requester"],
            timestamp=data["timestamp"],
            expires_at=data["expires_at"],
            status=ApprovalStatus(data["status"]),
            approver=data.get("approver"),
            approval_timestamp=data.get("approval_timestamp"),
            rejection_reason=data.get("rejection_reason"),
            metadata=data.get("metadata", {}),
        )

    def create(
        self,
        approval_type: ApprovalType,
        title: str,
        description: str,
        requester: str = "bmdr-cli",
        expires_in: int = 3600,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ApprovalRequest:
        """Create a new approval request."""
        request_id = f"{approval_type.value}_{int(time.time())}"
        now = time.time()

        req = ApprovalRequest(
            id=request_id,
            type=approval_type,
            title=title,
            description=description,
            requester=requester,
            timestamp=now,
            expires_at=now + expires_in,
            metadata=metadata or {},
        )

        self._requests[req.id] = req
        self._save(req)

        return req

    def get(self, request_id: str) -> Optional[ApprovalRequest]:
        """Get approval request by ID."""
        req = self._requests.get(request_id)
        if req and req.status == ApprovalStatus.PENDING and time.time() > req.expires_at:
            req.status = ApprovalStatus.EXPIRED
            self._save(req)
        return req

    def approve(self, request_id: str, approver: str) -> bool:
        """Approve a request."""
        req = self.get(request_id)
        if not req:
            return False

        if req.status != ApprovalStatus.PENDING:
            print(f"Request {request_id} is not pending (status: {req.status.value})")
            return False

        if time.time() > req.expires_at:
            req.status = ApprovalStatus.EXPIRED
            self._save(req)
            print(f"Request {request_id} has expired")
            return False

        req.status = ApprovalStatus.APPROVED
        req.approver = approver
        req.approval_timestamp = time.time()
        self._save(req)

        return True

    def reject(self, request_id: str, approver: str, reason: str = "") -> bool:
        """Reject a request."""
        req = self.get(request_id)
        if not req or req.status != ApprovalStatus.PENDING:
            return False

        req.status = ApprovalStatus.REJECTED
        req.approver = approver
        req.approval_timestamp = time.time()
        req.rejection_reason = reason
        self._save(req)

        return True

    def list_pending(self) -> List[ApprovalRequest]:
        """List all pending requests."""
        pending = []
        for req in self._requests.values():
            if req.status == ApprovalStatus.PENDING:
                if time.time() > req.expires_at:
                    req.status = ApprovalStatus.EXPIRED
                    self._save(req)
                else:
                    pending.append(req)
        return pending

    def cleanup_expired(self) -> int:
        """Remove expired requests. Return count removed."""
        removed = 0
        for req_id, req in list(self._requests.items()):
            if req.status == ApprovalStatus.EXPIRED or (
                req.status == ApprovalStatus.PENDING and time.time() > req.expires_at
            ):
                path = self._get_path(req_id)
                if path.exists():
                    path.unlink()
                del self._requests[req_id]
                removed += 1
        return removed


class ApprovalGate:
    """Approval gate for critical operations."""

    # Operations requiring approval
    REQUIRED_APPROVALS = {
        ApprovalType.DEPLOY_PRODUCTION: True,
        ApprovalType.SECRET_CHANGE: True,
        ApprovalType.INFRA_CHANGE: True,
        ApprovalType.PR_MERGE: False,  # Can be configured
        ApprovalType.DEPLOY_STAGING: False,
    }

    def __init__(self, store: Optional[ApprovalStore] = None):
        self.store = store or ApprovalStore()

    def requires_approval(self, approval_type: ApprovalType) -> bool:
        """Check if approval type requires human approval."""
        return self.REQUIRED_APPROVALS.get(approval_type, False)

    def request(
        self,
        approval_type: ApprovalType,
        title: str,
        description: str,
        requester: str = "bmdr-cli",
        expires_in: int = 3600,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[ApprovalRequest]:
        """Request approval for an operation."""
        if not self.requires_approval(approval_type):
            return None

        req = self.store.create(
            approval_type=approval_type,
            title=title,
            description=description,
            requester=requester,
            expires_in=expires_in,
            metadata=metadata,
        )

        # Print approval request details
        print("\n" + "=" * 60)
        print("🛡️  APPROVAL REQUIRED")
        print("=" * 60)
        print(f"Request ID: {req.id}")
        print(f"Type: {req.type.value}")
        print(f"Title: {req.title}")
        print(f"Description: {req.description}")
        print(f"Requester: {req.requester}")
        print(f"Expires: {req.expires_at - time.time():.0f} seconds")
        print("\nTo approve:")
        print(f"  bmdr approve {req.id}")
        print("To reject:")
        print(f"  bmdr reject {req.id} --reason 'reason here'")
        print("=" * 60 + "\n")

        return req

    def check(self, request_id: str) -> bool:
        """Check if a request is approved."""
        req = self.store.get(request_id)
        if not req:
            return False
        return req.status == ApprovalStatus.APPROVED

    def wait_for_approval(
        self,
        request_id: str,
        timeout: int = 3600,
        poll_interval: int = 10,
    ) -> bool:
        """Wait for approval with polling."""
        start = time.time()
        while time.time() - start < timeout:
            req = self.store.get(request_id)
            if not req:
                return False

            if req.status == ApprovalStatus.APPROVED:
                print(f"✅ Request {request_id} approved by {req.approver}")
                return True

            if req.status == ApprovalStatus.REJECTED:
                print(f"❌ Request {request_id} rejected by {req.approver}")
                if req.rejection_reason:
                    print(f"Reason: {req.rejection_reason}")
                return False

            if req.status == ApprovalStatus.EXPIRED:
                print(f"⏰ Request {request_id} expired")
                return False

            time.sleep(poll_interval)

        print(f"⏰ Timeout waiting for approval of {request_id}")
        return False


# Global approval gate instance
_gate: Optional[ApprovalGate] = None


def get_approval_gate() -> ApprovalGate:
    """Get global approval gate instance."""
    global _gate
    if _gate is None:
        _gate = ApprovalGate()
    return _gate
