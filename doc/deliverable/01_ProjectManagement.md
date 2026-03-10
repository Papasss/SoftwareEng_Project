# Product Breakdown Structure (PBS)

| ID  | Deliverable                                     | Type           | Notes                                         |
|:----|:------------------------------------------------|:---------------|:----------------------------------------------|
| S1  | Report management service                       | Software       | Backend: Core report life-cycle logic         |
| S2  | User account management service                 | Software       | Backend: Auth and RBAC logic                  |
| S3  | Notification service                            | Software       | Backend: Email and in-app alert engine        |
| S4  | Messaging service                               | Software       | Backend: Communication logic                  |
| S5  | Statistics and analytics service                | Software       | Backend: Data aggregation engine              |
| S6  | Public portal interface                         | Software       | Citizen: Main landing page                    |
| S7  | Citizen registration and login system           | Software       | Citizen: UI for authentication                |
| S8  | Citizen profile management                      | Software       | Citizen: Profile and preferences settings     |
| S9  | Report submission interface                     | Software       | Citizen: Geo-location and photo workflow      |
| S10 | Map-based report visualization                  | Software       | Citizen: Interactive OSM visualization        |
| S11 | Report search and filtering interface           | Software       | Citizen: Table view with filters              |
| S12 | Report detail page                              | Software       | Citizen: Full report history and media        |
| S13 | Report following system                         | Software       | Citizen: Subscription to report updates       |
| S14 | Notification interface for citizens             | Software       | Citizen: User-side alert dashboard            |
| S15 | Report review dashboard                         | Software       | Operator: Triage and verification console     |
| S16 | Report assignment tools                         | Software       | Operator: Routing to technical offices        |
| S17 | Report status management system                 | Software       | Operator: Status transition tools             |
| S18 | Citizen–operator messaging interface            | Software       | Operator: Staff-side communication UI         |
| S19 | System configuration panel                      | Software       | Admin: Global system parameters               |
| S20 | Category management module                      | Software       | Admin: Dynamic report category tools          |
| S21 | Private statistics dashboard                    | Software       | Admin: Secure analytical view                 |
| I1  | User accounts database                          | Infrastructure | Data: Persistent user profile storage         |
| I2  | Reports database                                | Infrastructure | Data: Geo-spatial report storage              |
| I3  | Photos/media storage for reports                | Infrastructure | Data: Binary storage for attachments          |
| I4  | Messaging database                              | Infrastructure | Data: Communication history storage           |
| I5  | Notifications database                          | Infrastructure | Data: Logs for alerts and notifications       |
| I6  | Cloud deployment platform                       | Infrastructure | Deployment: CI/CD and hosting setup           |
| I7  | Application hosting environment                 | Infrastructure | Deployment: Web/App server configuration      |
| I8  | Database server system                          | Infrastructure | Deployment: Managed DB instance               |
| I9  | Media storage system                            | Infrastructure | Deployment: Blob/File server for media        |
| I10 | Backup and disaster recovery system             | Infrastructure | Deployment: Data safety protocols             |
| I11 | Map service integration                         | Infrastructure | Deployment: OSM API/Proxy integration         |
| T1  | Interactive city map (Public)                   | Software       | Transparency: Spatial data visualization      |
| T2  | Report table view (Public)                      | Software       | Transparency: Filterable structured data      |
| T3  | CSV export functionality                        | Software       | Transparency: Open Data extraction tools      |
| T4  | Public statistics dashboard                     | Software       | Transparency: Public trend charts             |
| A1  | Reports by category charts                      | Software       | Analytics: Public distribution metrics        |
| A2  | Report trends over time                         | Software       | Analytics: Temporal growth analysis           |
| A3  | Reports by status                               | Software       | Analytics: Private operational metrics        |
| A4  | Reports by category and status                  | Software       | Analytics: Private cross-reference data       |
| A5  | Reports by reporter                             | Software       | Analytics: Private activity analytics         |
| A6  | Top 1% reporters statistics                     | Software       | Analytics: Private power-user engagement      |
| A7  | Top 5% reporters statistics                     | Software       | Analytics: Private engagement analysis        |
| D1  | System requirements document                    | Documentation  | Deliverable: Functional/Technical specs       |
| D2  | System architecture and design document         | Documentation  | Deliverable: ERD and Architectural diagrams   |
| D3  | API documentation                               | Documentation  | Deliverable: Backend technical reference      |
| D4  | Test plan                                       | Documentation  | Deliverable: QA and testing strategy          |
| D5  | Test reports                                    | Documentation  | Deliverable: Validation results               |
| D6  | Citizen user guide                              | Documentation  | Deliverable: End-user manual                  |
| D7  | Municipal operator user guide                   | Documentation  | Deliverable: Staff operational manual         |
| D8  | Administrator manual                            | Documentation  | Deliverable: System configuration guide       |


**Software** <br>

ID Deliverable <br>
S1 Report management service <br>
S2 User account management service <br>
S3 Notification service <br>
S4 Messaging service <br>
S5 Statistics and analytics service <br>
S6 Public portal interface <br>
S7 Citizen registration and login system <br>
S8 Citizen profile management <br>
S9 Report submission interface <br>
S10 Map-based report visualization <br>
S11 Report search and filtering interface <br>
S12 Report detail page <br>
S13 Report following system <br>
S14 Notification interface for citizens <br>
S15 Report review dashboard <br>
S16 Report assignment tools <br>
S17 Report status management system <br>
S18 Citizen–operator messaging interface <br>
S19 System configuration panel <br>
S20 Category management module <br>
S21 Private statistics dashboard <br>
<br>

**Data and Storage** <br>

ID Deliverable <br>
DT1 User accounts database <br>
DT2 Reports database <br>
DT3 Photos/media storage for reports <br>
DT4 Messaging database <br>
DT5 Notifications database <br>
<br>

**Infrastructure** <br>

ID Deliverable <br>
I1 Cloud deployment platform <br>
I2 Application hosting environment <br>
I3 Database server system <br>
I4 Media storage system <br>
I5 Backup and disaster recovery system <br>
I6 Map service integration (OSM) <br>
<br>

**Public Transparency & Analytics** <br>

ID Deliverable <br>
T1 Interactive city map displaying reports <br>
T2 Report table view with filters <br>
T3 CSV export functionality <br>
T4 Public statistics dashboard <br>
A1 Reports by category charts <br>
A2 Report trends over time <br>
A3 Reports by status <br>
A4 Reports by category and status <br>
A5 Reports by reporter <br>
A6 Top 1% reporters statistics <br>
A7 Top 5% reporters statistics <br>
<br>

**Documentation** <br>

ID Deliverable <br>
D1 System requirements document <br>
D2 System architecture and design document <br>
D3 API documentation <br>
D4 Test documentation (test plan, test report) <br>
D5 User manual and documentation (Citizen, Operator, Admin) <br>
---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID  | Work package | Traced PBS outputs (IDs) |
|:----|:-------------|:--------------------------|
| #.# |              |                           |


---

# Gantt, dependencies, and critical path

## Activity table
| ID | Activity | Duration | Dependencies | Start | End | Critical | Milestone |
|:---|:---------|:---------|:-------------|:------|:----|:------|:---------|
| R# |          |          |              |       |     |       |          |


## Critical path
`X → X → X → ...`



---

# Risk Management

**Scales and thresholds**
- **Probability (P)**: 1 (rare) … 5 (almost certain)
- **Impact (I)**: 1 (minor) … 5 (critical)
- **Exposure**: `P × I` (range 1–25)

Risk level thresholds (by exposure):
- **Low**: 1–5
- **Medium**: 6–10
- **High**: 11–16
- **Very High**: >16



## Risks table
| ID | Risk | Category | P | I | P×I | Level | Mitigation / Response strategy |
|:---|:-----|:---------|--:|--:|----:|:------|:-------------------------------|
|  |      |          |   |   |     |       |                                |


