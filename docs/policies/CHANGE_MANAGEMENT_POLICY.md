# BMDR Change Management Policy

## 1. Purpose

This policy defines the procedures for managing changes to BMDR's IT infrastructure, applications, and services. All changes must follow this policy to ensure stability, security, and auditability.

**Scope**: All changes to production systems, including code deployments, infrastructure changes, configuration updates, and security patches.

**Owner**: Change Advisory Board (CAB)
**Approver**: CTO

---

## 2. Change Classification

### 2.1 Change Types

| Type | Definition | Examples | Approval Required |
|---|---|---|---|
| **Standard** | Low-risk, pre-approved | Routine patches, config updates | Engineering Lead |
| **Normal** | Medium-risk, requires review | Feature deployments, schema changes | CAB |
| **Emergency** | Critical, immediate action needed | Security patches, outage fixes | On-call + Post-hoc CAB |
| **Major** | High-risk, significant impact | Architecture changes, vendor swaps | CTO + Board |

### 2.2 Risk Assessment Matrix

| Impact | Low Probability | Medium Probability | High Probability |
|---|---|---|---|
| **High** | Normal | Normal | Major |
| **Medium** | Standard | Normal | Normal |
| **Low** | Standard | Standard | Normal |

---

## 3. Change Request Process

### 3.1 Request Submission

All changes require a Change Request (CR) ticket containing:
- Change description and justification
- Risk assessment
- Implementation plan
- Rollback plan
- Testing results
- Approval signatures

### 3.2 Review and Approval

```
Step 1: Technical Review
├── Code review (2+ reviewers)
├── Security review (if applicable)
├── Architecture review (if applicable)
└── Test results verification

Step 2: CAB Review (for Normal/Major)
├── Impact assessment
├── Resource requirements
├── Scheduling conflicts
└── Approval vote

Step 3: Authorization
├── Standard: Engineering Lead
├── Normal: CAB Chair
├── Emergency: On-call Manager
└── Major: CTO
```

### 3.3 Implementation Windows

| Environment | Allowed Windows | blackout Periods |
|---|---|---|
| **Staging** | Anytime | None |
| **Production** | Tue-Thu 10:00-16:00 UTC | Fridays, month-end, quarter-end |
| **Emergency** | Anytime | None (with approval) |

---

## 4. Emergency Changes

### 4.1 Criteria for Emergency Change
- Active security vulnerability with known exploit
- Service outage affecting customers
- Data corruption or loss in progress
- Regulatory compliance deadline

### 4.2 Emergency Procedure
1. **Assess**: On-call engineer validates emergency
2. **Notify**: Page on-call manager + security (if applicable)
3. **Approve**: Verbal approval from on-call manager
4. **Implement**: Execute with minimum viable testing
5. **Document**: Create retroactive CR within 24 hours
6. **Review**: CAB review within 72 hours

---

## 5. Post-Implementation Review

### 5.1 Review Requirements

| Change Type | Review Timing | Participants |
|---|---|---|
| Standard | Within 1 week | Implementer + Lead |
| Normal | Within 3 days | CAB subset |
| Emergency | Within 24 hours | Full CAB |
| Major | Within 1 week | CAB + Stakeholders |

### 5.2 Review Content
- Was the change successful?
- Were there any issues?
- Was the rollback plan adequate?
- Lessons learned
- Process improvements

---

## 6. Policy Enforcement

### 6.1 Automated Enforcement
- All production changes via CI/CD
- Branch protection on main/production
- Required reviewers based on change type
- Automated security scanning

### 6.2 Violations
| Violation | Consequence |
|---|---|
| Unauthorized production change | Written warning + access review |
| Change without CR | Revert + incident review |
| Failed to document emergency change | Manager notification |

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2024-01-01 | CAB | Initial policy |

**Approved By:**
- [ ] CAB Chair: _________________ Date: _______
- [ ] CTO: _________________ Date: _______
