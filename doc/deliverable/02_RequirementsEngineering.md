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
| PER-01 | Andrea Russo | Registered Citizen (Occasional Reporter) | Andrea is a 34-year-old employee in Turin who commutes daily using public transport and walking. He is comfortable with mobile apps but prefers quick and simple interactions. He often notices urban issues such as broken streetlights or waste while commuting. | Submit reports quickly with minimal steps, attach a photo, and track updates easily | Limited time, frequent distractions, uncertainty in choosing categories, low tolerance for complex workflows | Smartphone, mainly on mobile data while outdoors | Prefers simple UI, clear instructions, minimal typing |
| PER-02 | Giulia Bianchi | Active Citizen (Frequent Reporter) | Giulia is a 29-year-old resident actively involved in community improvement. She regularly reports issues and follows multiple reports to stay informed about city conditions. | Submit detailed reports, track multiple issues, receive timely updates | Needs efficient management of multiple reports, risk of notification overload | Smartphone and laptop | Needs organized dashboard, filtering options, notification control |
| PER-03 | Luca Ferraro | Municipal Operator | Luca is a 46-year-old municipal employee responsible for reviewing and managing reports related to infrastructure. He works in an office environment and handles a high volume of reports daily. | Review and validate reports efficiently, assign tasks, update status, communicate with citizens | High workload, time pressure, requires accurate and complete report information | Desktop computer in office | Needs structured data, filtering tools, efficient workflow interface |
| PER-04 | Alessia Conti | System Administrator | Alessia is a 37-year-old IT administrator responsible for maintaining the system and monitoring analytics. She ensures system reliability and supports decision-making through data insights. | Monitor system performance, access analytics, manage configurations | Requires reliable data, system stability, and clear analytics visualization | Desktop or laptop | Needs detailed dashboards and clear data visualization |
| PER-05 | Elena Greco | Visitor (Unregistered User) | Elena is a 31-year-old resident who occasionally checks city conditions online but does not want to create an account. She uses the platform mainly to stay informed about issues in her neighborhood. | Browse reports on the map, filter issues by category or status, view public statistics | Limited functionality without login, cannot submit or interact with reports, expects quick access to information | Smartphone or laptop, usually at home or on the go | Needs intuitive navigation, clear map visualization, and fast loading pages |
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