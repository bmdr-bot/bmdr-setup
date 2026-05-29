# DORA (Digital Operational Resilience Act) Compliance

## Overview

The Digital Operational Resilience Act (DORA) is an EU regulation that sets requirements for the digital operational resilience of financial entities. This document outlines BMDR's compliance framework.

**Applicable Articles**: 6-16 (ICT Risk Management)
**Effective Date**: January 17, 2025
**Review Cycle**: Quarterly

---

## 1. ICT Risk Management Framework (Article 6)

### 1.1 Governance
- [ ] Board-level oversight of ICT risk
- [ ] Dedicated ICT risk management function
- [ ] Three lines of defense model:
  - **Line 1**: Business units (own the risk)
  - **Line 2**: Risk management (oversight)
  - **Line 3**: Internal audit (independent assurance)

### 1.2 Risk Assessment
- [ ] Annual ICT risk assessment
- [ ] Risk appetite statement approved by board
- [ ] Risk register maintained and reviewed quarterly
- [ ] Scenario analysis for critical services

### 1.3 Risk Mitigation
- [ ] Control framework mapped to risks
- [ ] Control testing schedule
- [ ] Remediation tracking
- [ ] Risk reporting to board (quarterly)

---

## 2. ICT-Related Incident Management (Article 10)

### 2.1 Incident Classification

| Classification | Criteria | Reporting Timeline |
|---|---|---|
| **Major** | Significant disruption, data breach | Within 4 hours to regulator |
| **Significant** | Service degradation, limited impact | Within 24 hours to regulator |
| **Minor** | No customer impact, contained | Internal reporting only |

### 2.2 Incident Response Process
```
1. DETECT (Automated monitoring)
   └── Alert fired → On-call notified

2. ASSESS (Triage)
   └── Impact assessment → Classification

3. CONTAIN (Limit damage)
   └── Isolation → Evidence preservation

4. ERADICATE (Remove threat)
   └── Root cause analysis → Fix applied

5. RECOVER (Restore service)
   └── Service validation → Monitoring

6. REPORT (Regulatory)
   └── Initial report (4h) → Final report (72h)

7. LEARN (Improve)
   └── Post-incident review → Policy update
```

### 2.3 Reporting Requirements
- **Initial Report**: Within 4 hours of classification as major
- **Intermediate Report**: Within 72 hours with progress
- **Final Report**: Within 1 month with root cause and remediation
- **Annual Summary**: All incidents summarized for board

---

## 3. Digital Operational Resilience Testing (Article 11)

### 3.1 Testing Program

| Test Type | Frequency | Scope | Responsible |
|---|---|---|---|
| **Vulnerability scans** | Weekly | All systems | DevOps |
| **Penetration testing** | Annual | External + internal | External firm |
| **Scenario testing** | Quarterly | Critical services | Risk Team |
| **Tabletop exercises** | Semi-annual | Incident response | Security |
| **Full DR test** | Annual | All critical systems | SRE |
| **Chaos engineering** | Quarterly | Non-production | SRE |

### 3.2 Threat-Led Penetration Testing (TLPT)
- Required every 3 years for critical entities
- Conducted by external tester
- Scope: All critical ICT systems
- Report submitted to regulator

---

## 4. Third-Party Risk Management (Article 12)

### 4.1 Critical ICT Third-Party Providers

| Provider | Service | Risk Level | Contract Review |
|---|---|---|---|
| Cloudflare | CDN, WAF, Tunnel | Critical | Quarterly |
| Hetzner | Infrastructure | Critical | Quarterly |
| HashiCorp | Vault, Consul | Critical | Quarterly |
| GitHub | Source control | High | Semi-annual |

### 4.2 Contract Requirements
- [ ] Right to audit clause
- [ ] Incident notification within 24 hours
- [ ] Subcontractor notification requirement
- [ ] Exit strategy and data portability
- [ ] Service level agreements (SLAs)
- [ ] Business continuity requirements

### 4.3 Concentration Risk
- [ ] No single provider > 40% of critical services
- [ ] Alternative provider identified for each critical service
- [ ] Quarterly concentration risk assessment

---

## 5. Information Sharing (Article 13)

### 5.1 Threat Intelligence
- [ ] Membership in financial sector ISAC
- [ ] Regular threat intelligence briefings
- [ ] Anonymous incident sharing with peers
- [ ] Government liaison for critical threats

### 5.2 Information Sharing Agreements
- [ ] Legal review of all sharing agreements
- [ ] Data anonymization before sharing
- [ ] No customer-identifiable information shared

---

## 6. ICT Risk Management Policy

### 6.1 Policy Requirements
- [ ] Board-approved ICT risk management policy
- [ ] Annual policy review
- [ ] Policy communicated to all staff
- [ ] Policy violation consequences defined

### 6.2 Key Performance Indicators (KPIs)

| KPI | Target | Measurement |
|---|---|---|
| System availability | 99.99% | Monthly |
| Mean time to detect (MTTD) | < 5 minutes | Per incident |
| Mean time to respond (MTTR) | < 30 minutes | Per incident |
| Patch deployment (critical) | < 24 hours | Monthly |
| DR test success rate | 100% | Per test |
| Third-party risk assessment | 100% coverage | Quarterly |

---

## 7. Compliance Checklist

### 7.1 Governance
- [ ] ICT risk management policy approved
- [ ] Board ICT risk oversight established
- [ ] Three lines of defense implemented
- [ ] Risk appetite defined

### 7.2 Risk Management
- [ ] ICT risk register maintained
- [ ] Risk assessment completed annually
- [ ] Control testing schedule active
- [ ] Risk reporting to board quarterly

### 7.3 Incident Management
- [ ] Incident classification scheme defined
- [ ] Incident response plan documented
- [ ] Reporting procedures established
- [ ] Post-incident review process active

### 7.4 Testing
- [ ] Testing program established
- [ ] Testing schedule maintained
- [ ] Test results reported to board
- [ ] Remediation tracked

### 7.5 Third-Party Management
- [ ] Critical providers identified
- [ ] Contract requirements defined
- [ ] Concentration risk monitored
- [ ] Exit strategies documented

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2024-01-01 | Compliance Officer | Initial document |
| 1.1 | 2024-06-01 | CISO | Added TLPT requirements |

**Approved By:**
- [ ] CISO: _________________ Date: _______
- [ ] CTO: _________________ Date: _______
- [ ] Board Representative: _________________ Date: _______
