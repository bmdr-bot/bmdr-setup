# BMDR Access Control Policy

## 1. Purpose

This policy defines the access control requirements for all BMDR systems, ensuring that only authorized individuals can access resources based on their role and need-to-know.

**Scope**: All employees, contractors, vendors, and automated systems.

**Owner**: CISO
**Approver**: CTO

---

## 2. Access Control Principles

### 2.1 Core Principles
- **Least Privilege**: Minimum access necessary for job function
- **Need-to-Know**: Access granted only for specific business need
- **Segregation of Duties**: Critical functions split between individuals
- **Default Deny**: No access unless explicitly granted

### 2.2 Access Control Models

| System Type | Model | Implementation |
|---|---|---|
| Applications | RBAC | Role-based permissions |
| Infrastructure | ABAC | Attribute-based (team, project, env) |
| Databases | RBAC + Row-level | Schema permissions + data filtering |
| APIs | OAuth 2.0 + scopes | Token-based authorization |

---

## 3. Identity Management

### 3.1 Identity Lifecycle

```
Onboarding
├── Background check completed
├── Manager requests access
├── Security approves based on role
├── Accounts provisioned
└── User acknowledges policy

Employment
├── Quarterly access review
├── Role change → access review
├── Privileged access → quarterly re-certification
└── Termination → immediate revocation

Offboarding
├── Manager notifies HR
├── HR triggers access revocation
├── All accounts disabled within 1 hour
├── Final access review completed
└── Assets returned
```

### 3.2 Account Types

| Type | Creation | MFA | Review Cycle |
|---|---|---|---|
| Standard user | HR onboarding | Required | Quarterly |
| Privileged admin | CISO approval | Hardware key | Monthly |
| Service account | DevOps request | N/A | Quarterly |
| Emergency access | Break-glass procedure | Hardware key | Per use |

---

## 4. Privileged Access Management (PAM)

### 4.1 Privileged Accounts
- Production system access
- Database administrative access
- Security tool administration
- Infrastructure management

### 4.2 PAM Requirements
- Just-in-Time (JIT) access only
- Session recording for all privileged sessions
- Time-limited access (maximum 4 hours)
- Approval required for each session
- Activity logging and alerting

### 4.3 Break-Glass Procedure
1. Emergency declared by on-call manager
2. Break-glass account activated
3. Security team notified immediately
4. Session recorded in full
5. Post-incident review within 24 hours
6. Break-glass account disabled

---

## 5. Access Reviews

### 5.1 Review Schedule

| Access Type | Frequency | Reviewer | Evidence |
|---|---|---|---|
| Standard user access | Quarterly | Manager | Review documentation |
| Privileged access | Monthly | CISO | Review documentation |
| Service accounts | Quarterly | DevOps Lead | Review documentation |
| Third-party access | Quarterly | Security | Review documentation |

### 5.2 Review Process
1. Generate access report
2. Manager validates each access
3. Remove unnecessary access
4. Document decisions
5. Security team audits reviews

---

## 6. Policy Enforcement

### 6.1 Technical Controls
- Automated provisioning/deprovisioning
- MFA enforcement on all systems
- Session timeout after 15 minutes
- Concurrent session limits
- IP-based restrictions for admin access

### 6.2 Violations
| Violation | Consequence |
|---|---|
| Sharing credentials | Immediate termination |
| Unauthorized access attempt | Written warning + access review |
| Bypassing MFA | Written warning |
| Failure to report compromised credentials | Written warning |

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2024-01-01 | CISO | Initial policy |

**Approved By:**
- [ ] CISO: _________________ Date: _______
- [ ] CTO: _________________ Date: _______
