# BMDR Deployment Policy

## 1. Purpose

This policy defines the deployment procedures, approval gates, and rollback mechanisms for all BMDR production systems. All deployments must follow these procedures to ensure system stability, security, and auditability.

**Scope**: All production deployments, infrastructure changes, and configuration updates.

**Owner**: DevOps Lead / SRE Manager
**Approver**: CTO (for production), Engineering Lead (for staging)

---

## 2. Deployment Environments

### 2.1 Environment Definitions

| Environment | Purpose | Data Classification | Approval Required |
|---|---|---|---|
| **Local** | Developer testing | Synthetic data | None |
| **Dev** | Integration testing | Synthetic data | None |
| **Test** | QA validation | Anonymized production | QA Lead |
| **Staging** | Pre-production validation | Production mirror | Engineering Lead |
| **Production** | Live customer-facing | Real customer data | CTO + Security |

### 2.2 Environment Isolation
- No direct network access between production and non-production
- Separate credentials per environment
- Separate monitoring and alerting
- Production data never copied to lower environments

---

## 3. Deployment Approval Matrix

### 3.1 Approval Requirements by Change Type

| Change Type | Staging | Production | Emergency |
|---|---|---|---|
| **Application code** | Engineering Lead | CTO + Security | On-call + CTO (post) |
| **Infrastructure** | Engineering Lead | CTO + CISO | On-call + CISO (post) |
| **Configuration** | Engineering Lead | CTO | On-call + CTO (post) |
| **Security patch** | Security Lead | CISO | On-call + CISO (post) |
| **Database schema** | DBA + Engineering | CTO + DBA + Security | On-call + CTO (post) |
| **Secret rotation** | Security Lead | CISO + Security | CISO |

### 3.2 Approval Gate Implementation

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy-staging:
    environment: staging
    # Auto-deploy after CI passes

  deploy-production:
    environment: production
    needs: deploy-staging
    # Requires manual approval via GitHub Environments
```

---

## 4. Deployment Procedures

### 4.1 Standard Deployment (Blue-Green)

```
Step 1: Pre-Deployment
├── Verify all tests pass (CI green)
├── Security scan passed (Snyk, Trivy)
├── Database migration plan reviewed
├── Rollback plan documented
└── Maintenance window communicated

Step 2: Deployment
├── Deploy to green environment
├── Run smoke tests on green
├── Database migrations (if needed)
├── Switch traffic (blue → green)
├── Monitor for 30 minutes
└── Verify error rates < 0.1%

Step 3: Post-Deployment
├── Monitor for 4 hours
├── Performance baseline comparison
├── Log review for anomalies
└── Update runbooks if needed
```

### 4.2 Canary Deployment

For high-risk changes:
```
Phase 1: 5% traffic → Monitor 15 min
Phase 2: 25% traffic → Monitor 15 min
Phase 3: 50% traffic → Monitor 30 min
Phase 4: 100% traffic → Monitor 1 hour
```

**Auto-rollback triggers:**
- Error rate > 1%
- P95 latency > 2x baseline
- Any P0/P1 alert fired
- Manual abort command

### 4.3 Database Deployment

- **Always** backup before migration
- Migrations run before app deployment
- Backward-compatible migrations only
- No destructive changes without 2-phase deployment
- DBA approval required for schema changes

---

## 5. Emergency Deployment (Hotfix)

### 5.1 Hotfix Criteria
- Active security vulnerability (CVE with exploit)
- Data corruption or loss in progress
- Complete service outage
- Regulatory compliance issue

### 5.2 Hotfix Procedure

```
1. PAGE on-call engineer + manager
2. Create hotfix branch from production tag
3. Fix + test locally (minimum viable)
4. Security review (if security-related)
5. Deploy with expedited approval
6. Post-deployment review within 24 hours
7. Retroactive CAB approval
```

### 5.3 Hotfix Approval
- On-call engineer can approve emergency fix
- CTO/CISO notified within 1 hour
- Full review within 24 hours
- Documentation updated

---

## 6. Rollback Procedures

### 6.1 Automatic Rollback
Triggered when:
- Health checks fail for 5 minutes
- Error rate exceeds threshold
- Critical alert fires

### 6.2 Manual Rollback
```bash
# Application rollback
kubectl rollout undo deployment/app

# Database rollback (if migration failed)
# Restore from pre-deployment backup
# Apply down-migration (if exists)

# Infrastructure rollback
terraform apply -var="version=PREVIOUS"
```

### 6.3 Rollback Decision Matrix

| Scenario | Action | Time Limit |
|---|---|---|
| Health check failure | Auto-rollback | 5 minutes |
| Elevated errors | Manual decision | 10 minutes |
| Performance degradation | Manual decision | 15 minutes |
| Data inconsistency | Immediate rollback | Immediate |
| Security concern | Immediate rollback | Immediate |

---

## 7. Deployment Monitoring

### 7.1 Key Metrics

| Metric | Baseline | Alert Threshold | Rollback Threshold |
|---|---|---|---|
| Error rate | < 0.1% | > 0.5% | > 1% |
| P50 latency | < 100ms | > 200ms | > 500ms |
| P95 latency | < 500ms | > 1000ms | > 2000ms |
| CPU usage | < 50% | > 80% | > 95% |
| Memory usage | < 70% | > 85% | > 95% |
| DB connections | < 80% | > 90% | > 95% |

### 7.2 Monitoring Dashboard
- Real-time deployment status
- Traffic split (for canary)
- Error rate comparison (old vs new)
- Resource utilization
- Business metrics (transactions, revenue)

---

## 8. Audit and Compliance

### 8.1 Deployment Logs
All deployments logged with:
- Who deployed
- What was deployed (commit SHA)
- When deployed
- Approval evidence
- Deployment duration
- Post-deployment verification results

### 8.2 Required Documentation
- Change ticket number
- Risk assessment
- Test results
- Rollback plan
- Post-deployment review

### 8.3 Compliance Requirements
- PCI-DSS: All changes to cardholder data environment documented
- SOC 2: Change management controls tested
- SOX: Segregation of duties enforced

---

## 9. Tools and Automation

### 9.1 Deployment Pipeline
```
GitHub PR → CI Tests → Security Scan → Approval Gate → Deploy Staging → 
Smoke Tests → Approval Gate → Deploy Production → Monitor → Done
```

### 9.2 Required Tools
- **GitHub Actions**: CI/CD pipeline
- **ArgoCD / Flux**: GitOps for Kubernetes
- **Terraform**: Infrastructure as Code
- **Vault**: Secret injection
- **Prometheus/Grafana**: Monitoring
- **PagerDuty**: Incident escalation

---

## 10. Policy Enforcement

### 10.1 Automated Enforcement
- No direct production access without approval ticket
- All deployments via CI/CD (no manual deploys)
- Branch protection on main/production branches
- Required reviewers based on change type
- Automated security scanning gates

### 10.2 Violations
| Violation | Consequence |
|---|---|
| Unauthorized production deploy | Written warning + access review |
| Deploy without approval | Revert + incident review |
| Skip security scan | Pipeline blocked + manager notification |
| Deploy outside window | Revert + policy review |

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2024-01-01 | DevOps Lead | Initial policy |
| 1.1 | 2024-06-01 | SRE Manager | Added canary deployment |

**Approved By:**
- [ ] DevOps Lead: _________________ Date: _______
- [ ] Engineering Lead: _________________ Date: _______
- [ ] CTO: _________________ Date: _______
