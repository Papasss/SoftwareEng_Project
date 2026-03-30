# 1) Stakeholders

| ID     | Stakeholder name |                                                Description                                      | Role | Main concerns |
|:-------|:-----------------|:------------------------------------------------------------------------------------------------|:-----|:--------------|
| STK-01 | Visitor                 | Person who accesses the platform to browse public reports and statistics without authentication | End user            | Easy access to information, usability, transparency               |
| STK-02 | Citizen                 | Person who creates an account to submit reports, track their evolution, follow reports, and communicate with municipal operators | End user            | Easy report submission, tracking updates, receiving notifications |
| STK-03 | Municipal Operator      | Person who reviews reports, verifies them, updates their status, and communicates with citizens | Operational user    | Efficient report handling, clear communication, workload management |
| STK-04 | Administrator           | Person who manages system configuration and accesses advanced analytics and reporting features | Administrative user | System control, monitoring, access to detailed statistics         |
| STK-05 | Authentication system   | Service used to manage user registration, login, and email verification                      | External system     | Security, reliability of authentication                           |
| STK-06 | Map service             | Service used to provide geo-location and map visualization of reports                    | External system     | Accuracy of location data, availability                           |
| STK-07 | Notification service    | Service used to notify users through in-platform and email notifications                     | External system     | Timely delivery of notifications, reliability                     |
| STK-08 | Developer      | People work on the technical side of the project        | Technician      | Developing technical part of the project         |
| STK-9 | Project Manager      | People managing developers and activities         | Manager     | Interfacing between technical group and business     |

---

# 2) Context Diagram

Attach your context diagram as an image under `../data/img/` and link it here:

- `![](../data/img/context-diagram.png)`

---

# 3) Interfaces

| ID     | Interface       | Actor                       | Physical interface                     | Logical interface     |
|:-------|:----------------|:----------------------------|:---------------------------------------|:----------------------|
| IF-01  | User access     | Visitor                     | Smartphone/PC with internet connection | Web GUI               |
| IF-02  | User access     | Citizen                     | Smartphone/PC with internet connection | Web GUI               |
| IF-03  | User access     | Municipal Operator          | Smartphone/PC with internet connection | Web GUI               |
| IF-04  | User access     | Administrator               | Smartphone/PC with internet connection | Web GUI               |
| IF-05  | Authentication  | Authentication system       | Internet connection                    | Authentication APIs   |
| IF-06  | Map interaction | Map service (OpenStreetMap) | Internet connection                    | Map APIs              |
| IF-07  | Notifications   | Notification service        | Internet connection                    | Notification APIs     |

---

# 4) Personas

| ID     | Name | Role | Background / Context | Goals | Constraints | Devices / Usage setting | Accessibility / Additional needs |
|:-------|:-----|:-----|:---------------------|:------|:------------|:------------------------|:---------------------------------|
| PER-01 |      |      |                      |       |             |                         |                                  |

---

# 5) User Stories

| ID    | Persona/Role | User story (As a… I want… so that…) |
|:------|:--------------|:-------------------------------------|
| US-01 | Visitor | As a visitor, I want to browse reports on the map so that I can see issues in the city |
| US-02 | Visitor | As a visitor, I want to filter reports by category and status so that I can find relevant information easily |
| US-03 | Citizen | As a citizen, I want to register an account so that I can submit and track reports |
| US-04 | Citizen | As a citizen, I want to log in securely so that I can access my account and activities |
| US-05 | Citizen | As a citizen, I want to submit a report with location, description, category, and photos so that I can report urban issues effectively |
| US-06 | Citizen | As a citizen, I want to mark my report as anonymous so that my identity is not publicly visible |
| US-07 | Citizen | As a citizen, I want to track the status of my reports so that I know how they are being handled |
| US-08 | Citizen | As a citizen, I want to follow reports submitted by others so that I receive updates about issues I care about |
| US-09 | Citizen | As a citizen, I want to receive notifications when report status changes so that I stay informed |
| US-10 | Citizen | As a citizen, I want to communicate with municipal operators so that I can provide or receive additional information |
| US-11 | Municipal Operator | As a municipal operator, I want to review submitted reports so that I can verify their validity |
| US-12 | Municipal Operator | As a municipal operator, I want to assign reports to relevant departments so that issues are handled efficiently |
| US-13 | Municipal Operator | As a municipal operator, I want to update report statuses so that citizens are informed about progress |
| US-14 | Municipal Operator | As a municipal operator, I want to communicate with citizens so that I can request clarifications or provide updates |
| US-15 | Administrator | As an administrator, I want to manage system configurations and access analytics so that I can monitor and maintain the system effectively |
| US-16 | Citizen | As a citizen, I want to export report data in CSV format so that I can analyze or share information offline |
| US-17 | Visitor | As a visitor, I want to view public statistics so that I can understand trends in reported issues |

---

# 6) Functional Requirements (FR)

| ID | Requirement statement (The system shall…) | Priority  | User story ID | Notes |
|:---|:------------------------------------------|:----------|:----------------|:------|
| FR-01 | The system shall allow visitors to browse reports on a map interface | Critical  | US-01 | Public access feature |
| FR-02 | The system shall allow users to filter reports by category, status, and time | Critical  | US-02 | Applies to map and table views |
| FR-03 | The system shall allow users to register an account with email verification | Critical  | US-03 | Requires authentication system |
| FR-04 | The system shall allow registered users to log in securely | Critical  | US-04 | Authentication required |
| FR-05 | The system shall allow citizens to submit reports including location, description, category, and up to 3 images | Critical  | US-05 | Core functionality |
| FR-06 | The system shall allow citizens to mark reports as anonymous for public display | Important    | US-06 | Privacy feature |
| FR-07 | The system shall allow users to view and track the status of reports | Critical  | US-07 | Transparency requirement |
| FR-08 | The system shall allow users to follow reports submitted by others | Important    | US-08 | Engagement feature |
| FR-09 | The system shall send notifications to users when report status changes | Critical  | US-09 | Notification system dependency |
| FR-10 | The system shall allow communication between citizens and municipal operators through messaging | Critical  | US-10 | Two-way communication |
| FR-11 | The system shall allow municipal operators to review submitted reports | Critical  | US-11 | Validation process |
| FR-12 | The system shall allow municipal operators to assign reports to appropriate departments or units | Important    | US-12 | Assumed workflow |
| FR-13 | The system shall allow municipal operators to update the status of reports | Critical  | US-13 | Status lifecycle |
| FR-14 | The system shall allow municipal operators to communicate with citizens regarding reports | Important  | US-14 | Messaging feature |
| FR-15 | The system shall allow administrators to manage system configurations and access analytics | Important    | US-15 | Merged admin functionality |
| FR-16 | The system shall allow users to export report data in CSV format | Optional  | US-16 | Data export |
| FR-17 | The system shall provide public access to aggregated statistics about reports | Important | US-17 | Transparency feature |


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
| NFR-11 | Localization | The system shall support multiple languages for the user interface | Support at least English and Italian languages | Testing / inspection | Low | Optional feature for broader accessibility |