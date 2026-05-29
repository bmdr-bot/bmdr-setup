# BMDR Financial Institution IT Infrastructure

## Executive Summary

This document defines the IT infrastructure architecture, security policies, and operational procedures for BMDR as a financial technology company. All infrastructure decisions prioritize security, compliance, auditability, and operational resilience.

---

## 1. Infrastructure Architecture

### 1.1 Network Topology

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERNET                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  Cloudflare     │  ← DDoS, WAF, Zero Trust
              │  (Edge Layer)   │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐  ┌─────▼─────┐  ┌────▼────┐
   │   API   │  │   Web     │  │  Admin  │
   │ Gateway │  │  Portal   │  │  Panel  │
   └────┬────┘  └─────┬─────┘  └────┬────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
           ┌──────────▼──────────┐
           │   Load Balancer     │  ← HAProxy / Nginx
           │   (Internal)        │
           └──────────┬──────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │  App    │  │  App    │  │  App    │
   │Server 1 │  │Server 2 │  │Server 3 │  ← Kubernetes / Docker Swarm
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        └────────────┼────────────┘
                     │
          ┌──────────▼──────────┐
          │   Data Layer        │
          │  ┌───────────────┐  │
          │  │  PostgreSQL   │  │  ← Primary + 2 Replicas
          │  │  (Encrypted)  │  │
          │  └───────────────┘  │
          │  ┌───────────────┐  │
          │  │    Redis      │  │  ← Session + Cache
          │  │  (Encrypted)  │  │
          │  └───────────────┘  │
          │  ┌───────────────┐  │
          │  │   Vault       │  │  ← Secrets Management
          │  │  (HashiCorp)  │  │
          │  └───────────────┘  │
          └─────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   Backup Layer      │
          │  (Offsite + Airgap) │
          └─────────────────────┘
```

### 1.2 Environment Segregation

| Environment | Purpose | Network Isolation | Access Level |
|---|---|---|---|
| **Development** | Feature development | Isolated VLAN | Developers |
| **Testing** | QA, integration tests | Isolated VLAN | QA + Dev |
| **Staging** | Pre-production validation | DMZ | DevOps + QA |
| **Production** | Live services | Strict DMZ | SRE + On-call only |
| **Management** | Monitoring, logging, vault | Dedicated VLAN | Security + SRE |

### 1.3 Server Specifications

#### Production Tier
- **Compute**: Minimum 8 vCPU / 16GB RAM per node
- **Storage**: NVMe SSD with full-disk encryption (LUKS)
- **Network**: Dual NIC (public + private), 10Gbps minimum
- **Redundancy**: N+1 minimum, auto-failover

#### Management Tier
- **Jump Host**: Hardened bastion with MFA
- **Monitoring**: Dedicated Prometheus + Grafana
- **Logging**: Centralized ELK stack with 90-day retention
- **Backup**: Daily encrypted snapshots to offsite storage

---

## 2. Security Architecture

### 2.1 Defense in Depth

```
Layer 1: Perimeter Security
├── Cloudflare WAF with OWASP Top 10 rules
├── Rate limiting: 100 req/min per IP
├── Geo-blocking for non-operational regions
└── DDoS protection (always-on)

Layer 2: Network Security
├── VLAN segmentation
├── Firewall rules: default-deny
├── Intrusion Detection System (Suricata)
└── Network flow monitoring

Layer 3: Application Security
├── Input validation and sanitization
├── OWASP ASVS Level 3 compliance
├── Dependency vulnerability scanning
└── Static Application Security Testing (SAST)

Layer 4: Data Security
├── AES-256 encryption at rest
├── TLS 1.3 in transit
├── Database column-level encryption for PII
└── Key rotation every 90 days

Layer 5: Identity & Access
├── MFA required for all accounts
├── Role-Based Access Control (RBAC)
├── Just-in-Time (JIT) access for production
└── Privileged Access Management (PAM)
```

### 2.2 Encryption Standards

| Data State | Standard | Key Management |
|---|---|---|
| At Rest | AES-256-GCM | HashiCorp Vault |
| In Transit | TLS 1.3 (mandatory) | Let's Encrypt / Internal CA |
| In Memory | Secure zeroization | Application-level |
| Backups | AES-256 + GPG | Offline HSM |

### 2.3 Secret Management

All secrets managed via HashiCorp Vault:
- **Dynamic credentials**: Database passwords rotated every 24h
- **API keys**: Scoped, time-limited, audit-logged
- **TLS certificates**: Auto-renewal via cert-manager
- **Encryption keys**: HSM-backed, never leave secure enclave

---

## 3. Compliance Framework

### 3.1 Regulatory Requirements

| Regulation | Scope | Implementation |
|---|---|---|
| **PCI-DSS** | Payment card data | Level 1 compliance, quarterly scans |
| **SOC 2 Type II** | Service organization | Annual audit, continuous monitoring |
| **GDPR** | EU customer data | Data minimization, right to erasure |
| **PSD2** | Payment services | Strong Customer Authentication (SCA) |
| **MiFID II** | Investment services | Transaction reporting, audit trails |
| **DORA** | Digital operational resilience | ICT risk management, incident reporting |

### 3.2 Audit Requirements

- **Access Logs**: Retained for 7 years, tamper-proof
- **Transaction Logs**: Immutable, blockchain-anchored
- **Change Logs**: All infrastructure changes tracked in Git
- **Video Logs**: Physical data center access recorded

---

## 4. Operational Procedures

### 4.1 Change Management

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Request │ -> │  Review  │ -> │  Approve │ -> │  Deploy  │ -> │ Validate │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
    │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼
 Ticket      Security      CAB/CTO        Automated      Smoke tests
 Created      Review       Approval       Pipeline       + Rollback
```

### 4.2 Incident Response

| Severity | Response Time | Resolution Target | Escalation |
|---|---|---|---|
| **P0 - Critical** | 15 minutes | 2 hours | CEO + Board |
| **P1 - High** | 30 minutes | 4 hours | CTO + CISO |
| **P2 - Medium** | 2 hours | 24 hours | Engineering Lead |
| **P3 - Low** | 4 hours | 72 hours | Team Lead |

### 4.3 Backup & Recovery

- **RPO (Recovery Point Objective)**: 5 minutes for transactional data
- **RTO (Recovery Time Objective)**: 1 hour for critical services
- **Backup Schedule**:
  - Real-time: Database streaming replication
  - Hourly: Incremental filesystem snapshots
  - Daily: Full encrypted backups to offsite
  - Monthly: Air-gapped archive

---

## 5. Monitoring & Alerting

### 5.1 Metrics Collection

| Category | Metrics | Retention |
|---|---|---|
| Infrastructure | CPU, RAM, Disk, Network | 1 year |
| Application | Latency, Errors, Throughput | 1 year |
| Security | Failed logins, Anomalies | 7 years |
| Business | Transactions, Volume | 7 years |

### 5.2 Alerting Rules

```yaml
# Critical alerts
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
  severity: P1
  
- alert: DatabaseLag
  expr: pg_replication_lag_seconds > 30
  severity: P0
  
- alert: UnauthorizedAccess
  expr: increase(failed_auth_attempts[1m]) > 5
  severity: P0
  auto_block: true
```

---

## 6. Vendor Management

### 6.1 Critical Vendors

| Vendor | Service | Risk Level | Assessment Frequency |
|---|---|---|---|
| Cloudflare | CDN, WAF, Tunnel | High | Quarterly |
| Hetzner | Infrastructure | High | Quarterly |
| HashiCorp | Vault, Consul | Critical | Monthly |
| GitHub | Source Control | High | Quarterly |

### 6.2 Vendor Requirements

- SOC 2 Type II certification minimum
- Data Processing Agreement (DPA) signed
- Right to audit clause
- Incident notification within 24 hours
- Data residency guarantees

---

## 7. Disaster Recovery

### 7.1 DR Sites

| Site | Location | RTO | RPO | Status |
|---|---|---|---|---|
| Primary | Frankfurt, DE | - | - | Active |
| Secondary | Amsterdam, NL | 1h | 5min | Warm Standby |
| Tertiary | Zurich, CH | 4h | 1h | Cold Standby |

### 7.2 DR Procedures

1. **Detection**: Automated monitoring triggers failover
2. **Decision**: On-call engineer validates within 15 minutes
3. **Failover**: DNS switch + database promotion
4. **Verification**: Smoke tests + transaction validation
5. **Communication**: Status page update + stakeholder notification

---

## 8. Appendix

### 8.1 Reference Standards

- NIST Cybersecurity Framework
- ISO 27001:2022
- CIS Controls v8
- OWASP ASVS 4.0

### 8.2 Document Control

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2024-01-15 | Security Team | Initial release |
| 1.1 | 2024-06-01 | CISO | Added DORA compliance |

### 8.3 Approval

| Role | Name | Date | Signature |
|---|---|---|---|
| CTO | | | |
| CISO | | | |
| Compliance Officer | | | |
