# SOC 2 Type II Controls

## Trust Services Criteria

### Security (CC6.1 - CC6.8)

| Control ID | Description | Implementation | Evidence |
|---|---|---|---|
| CC6.1 | Logical access security | RBAC, MFA, least privilege | Access review logs |
| CC6.2 | Prior to access | Background checks, NDA | HR records |
| CC6.3 | Access removal | Automated offboarding | IAM audit logs |
| CC6.4 | Access review | Quarterly access reviews | Review documentation |
| CC6.5 | System credentials | Vault dynamic credentials | Vault audit logs |
| CC6.6 | Encryption | AES-256, TLS 1.3 | Encryption configuration |
| CC6.7 | Security infrastructure | Firewalls, IDS, WAF | Network diagrams |
| CC6.8 | Security incident detection | SIEM, alerting | Incident tickets |

### Availability (A1.1 - A1.3)

| Control ID | Description | Implementation | Evidence |
|---|---|---|---|
| A1.1 | System availability | 99.99% uptime SLA | Monitoring dashboards |
| A1.2 | Recovery procedures | Documented DR plan | DR test results |
| A1.3 | Backup and recovery | Daily backups, tested quarterly | Backup logs |

### Confidentiality (C1.1 - C1.2)

| Control ID | Description | Implementation | Evidence |
|---|---|---|---|
| C1.1 | Confidential info identification | Data classification | Classification labels |
| C1.2 | Confidential info disposal | Secure deletion procedures | Disposal logs |

---

## Control Testing Schedule

| Control | Frequency | Tester | Last Tested |
|---|---|---|---|
| Access review | Quarterly | Security Team | |
| Penetration test | Annual | External | |
| DR test | Semi-annual | SRE | |
| Backup restore | Quarterly | SRE | |
| Vulnerability scan | Weekly | DevOps | |
| Code review | Per PR | Engineering | |
| Security training | Annual | HR | |
