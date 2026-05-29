# PCI-DSS Compliance Requirements

## Scope

This document defines PCI-DSS requirements for systems handling payment card data within BMDR infrastructure.

**Cardholder Data Environment (CDE)**: All systems storing, processing, or transmitting cardholder data.

---

## 1. Build and Maintain a Secure Network

### 1.1 Firewall Configuration
- [ ] Firewall rules reviewed every 6 months
- [ ] Default-deny for all inbound traffic
- [ ] Explicit allow rules with business justification
- [ ] Firewall logs retained for 1 year

### 1.2 System Hardening
- [ ] No default passwords
- [ ] Unnecessary services disabled
- [ ] Security patches applied within 30 days
- [ ] Configuration standards documented

---

## 2. Protect Cardholder Data

### 2.1 Data Retention
- [ ] Cardholder data retention policy defined
- [ ] Data purged after business need expires
- [ ] Quarterly data retention audits

### 2.2 Encryption Requirements
- [ ] AES-256 for data at rest
- [ ] TLS 1.3 for data in transit
- [ ] Key management via HSM
- [ ] Key rotation every 90 days

### 2.3 PAN Display Masking
- [ ] Only last 4 digits displayed
- [ ] Full PAN only for authorized personnel
- [ ] Masking verified in all interfaces

---

## 3. Maintain a Vulnerability Management Program

### 3.1 Anti-Virus
- [ ] AV installed on all systems
- [ ] AV definitions updated daily
- [ ] AV logs reviewed weekly

### 3.2 Security Patches
- [ ] Critical patches within 15 days
- [ ] High patches within 30 days
- [ ] Patch management process documented

### 3.3 Vulnerability Scanning
- [ ] Quarterly external ASV scans
- [ ] Monthly internal vulnerability scans
- [ ] Remediation within 30 days

---

## 4. Implement Strong Access Control Measures

### 4.1 Need-to-Know Access
- [ ] Access based on job function
- [ ] Documented approval process
- [ ] Quarterly access reviews

### 4.2 Unique User IDs
- [ ] No shared accounts
- [ ] Unique ID per person
- [ ] ID disabled within 24 hours of termination

### 4.3 Physical Access
- [ ] Badge access to data center
- [ ] Visitor logs maintained
- [ ] Media destruction procedures

---

## 5. Regularly Monitor and Test Networks

### 5.1 Logging
- [ ] All CDE access logged
- [ ] Logs reviewed daily
- [ ] Logs retained for 1 year
- [ ] Log integrity protected

### 5.2 File Integrity Monitoring
- [ ] FIM on critical files
- [ ] Alerts on unauthorized changes
- [ ] Weekly FIM report review

### 5.3 Penetration Testing
- [ ] Annual external penetration test
- [ ] Annual internal penetration test
- [ ] Segmentation testing (if applicable)

---

## 6. Maintain an Information Security Policy

### 6.1 Security Policy
- [ ] Policy reviewed annually
- [ ] Policy communicated to all personnel
- [ ] Acknowledgment of policy

### 6.2 Risk Assessment
- [ ] Annual risk assessment
- [ ] Risk register maintained
- [ ] Risk treatment plans

### 6.3 Incident Response
- [ ] Incident response plan
- [ ] Annual IR plan testing
- [ ] Incident response team defined

---

## Compliance Validation

| Requirement | Method | Frequency | Responsible |
|---|---|---|---|
| SAQ/ROC | QSA assessment | Annual | CISO |
| ASV Scan | External scan | Quarterly | Security |
| Internal scan | Vulnerability scan | Monthly | DevOps |
| Pen test | External firm | Annual | CISO |
| Policy review | Document review | Annual | Compliance |

---

**Document Control**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2024-01-01 | Compliance Officer | Initial document |
