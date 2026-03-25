# 1) Stakeholders

| ID     | Stakeholder name |                                                Description                                      | Role | Main concerns |
|:-------|:-----------------|:------------------------------------------------------------------------------------------------|:-----|:--------------|
| STK-## |                  |  |            |                |


---

# 2) Context Diagram

Attach your context diagram as an image under `../data/img/` and link it here:

- `![](../data/img/context-diagram.png)`

---

# 3) Interfaces

| ID     | Interface       | Actor                       | Physical interface                     | Logical interface     |
|:-------|:----------------|:----------------------------|:---------------------------------------|:----------------------|
| IF-01  |     |                    |  |   |

---

# 4) Personas

| ID     | Name | Role | Background / Context | Goals | Constraints | Devices / Usage setting | Accessibility / Additional needs |
|:-------|:-----|:-----|:---------------------|:------|:------------|:------------------------|:---------------------------------|
| PER-01 |      |      |                      |       |             |                         |                                  |

---

# 5) User Stories

| ID    | Persona/Role | User story (As a… I want… so that…) |
|:------|:-------------|:------------------------------------|
| US-XX |              |                                     |

---

# 6) Functional Requirements (FR)

| ID    | Requirement statement (The system shall…) | Priority | User story ID | Notes |
|:------|:------------------------------------------|:---------|:--------------|:------|
| FR-XX |                                           |          |               |       |


---

# 7) Non-Functional Requirements (NFR)

| ID     | Category | Requirement statement | Metric / Target | Verification                           | Priority | Notes |
|:-------|:---------|:----------------------|:----------------|:---------------------------------------|:---------|:------|
| NFR-01 | Performance | The system shall respond to user requests within an acceptable time | ≤ 2 seconds for 95% of requests | Performance testing | High | Applies to report browsing and submission |
| NFR-02 | Availability | The system shall be available to users at all times except scheduled maintenance | ≥ 99% uptime per month | Monitoring / logs | High | Critical for public access |
| NFR-03 | Usability | The system shall allow users to complete report submission with minimal effort | Report submission completed in ≤ 2 minutes by 90% of users | Usability testing | High | Based on citizen persona needs |
| NFR-04 | Security | The system shall protect user data and authentication credentials | Passwords encrypted and secure login enforced | Security testing / inspection | High | Includes authentication system |
| NFR-05 | Privacy | The system shall ensure that anonymous reports do not expose user identity publicly | 100% of anonymous reports hide user identity | Inspection / testing | High | Critical for user trust |
| NFR-06 | Reliability | The system shall ensure that notifications are delivered reliably | ≥ 95% notification delivery success rate | Monitoring / logs | Medium | Depends on notification service |
| NFR-07 | Scalability | The system shall handle increasing number of users and reports without degradation | Support at least 10,000 concurrent users | Load testing | Medium | Future scalability |
| NFR-08 | Compatibility | The system shall be accessible on common devices and browsers | Support latest versions of Chrome, Firefox, Safari | Testing | Medium | Web-based system |
| NFR-09 | Maintainability | The system shall be designed for easy maintenance and updates | Code modularity and documentation available | Code review / inspection | Medium | Important for long-term use |
| NFR-10 | Data Integrity | The system shall ensure accuracy and consistency of stored data | No data loss or corruption in normal operation | Testing / validation | High | Applies to reports and user data |