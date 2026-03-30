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
| PER-XX |      |      |                      |       |             |                         |                                  |

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
| NFR-XX |          |                       |                 |                                        |          |       |