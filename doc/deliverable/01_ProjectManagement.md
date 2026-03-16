# Product Breakdown Structure (PBS)

| ID  | Deliverable                             | Type           | Notes                                         |
|:----|:----------------------------------------|:---------------|:----------------------------------------------|
| S1  | Report management service               | Software       | Backend: Core report life-cycle logic         |
| S2  | User account management service         | Software       | Backend: Auth and RBAC logic                  |
| S3  | Notification service                    | Software       | Backend: Email and in-app alert engine        |
| S4  | Messaging service                       | Software       | Backend: Communication logic                  |           |
| S5  | Portal interface                        | Software       | Main landing page and private sections                    |
| S6  | registration and login system           | Software       | UI for authentication                |
| S7  | profile management                      | Software       | Profile and preferences settings     |
| S8  | Report submission interface             | Software       | Geo-location and photo workflow      |
| S9  | Map-based report visualization          | Software       | Interactive OSM visualization        |
| S10 | Report search and filtering interface   | Software       | Table view with filters              |
| S11 | Report detail page                      | Software       | Full report history and media        |
| S12 | Report following system                 | Software       | Subscription to report updates       |
| S13 | Notification interface                  | Software       | User-side alert dashboard            |
| S14 | Report status management system         | Software       | Operator: Status transition tools             |
| S15 | Messaging interface                     | Software       | Users communication UI                        |
| S16 | System configuration panel              | Software       | Global system parameters               |
| S17 | Category management module              | Software       | Dynamic report category tools          |
| S18 | CSV export functionality                | Software       | Transparency: Open Data extraction tools      |
| S19 | Private statistics dashboard            | Software       | Transparency: Public trend charts             |
| S20 | Public statistics dashboard             | Software       | Transparency: Private trend charts        |
| I1  | Cloud deployment platform               | Infrastructure | Deployment: CI/CD and hosting setup           |
| I2  | Application hosting environment         | Infrastructure | Deployment: Web/App server configuration      |
| I3  | Database server system                  | Infrastructure | Deployment: Managed DB instance: User accounts database, Reports database, Messaging database, Notifications database               |
| I4  | Media storage system                    | Infrastructure | Deployment: Blob/File server for media: Photos/media storage for reports        |
| I5  | Backup and disaster recovery system     | Infrastructure | Deployment: Data safety protocols             |
| I6  | Map service integration                 | Infrastructure | Deployment: OSM API/Proxy integration         |
| D1  | System requirements document            | Documentation  | Deliverable: Functional/Technical specs       |
| D2  | System architecture and design document | Documentation  | Deliverable: ERD and Architectural diagrams   |
| D3  | API documentation                       | Documentation  | Deliverable: Backend technical reference      |
| D4  | Test Documentation                      | Documentation  | Deliverable: QA and testing strategy          |
| D5  | User Manual and Documentation           | Documentation  | Deliverable: End-user manual, Municipal manual and Administrator                  |


**Software** <br>

ID Deliverable <br>
S1 Report management service <br>
S2 User account management service <br>
S3 Notification service <br>
S4 Messaging service <br>
S5 Portal interface <br>
S6 registration and login system <br>
S7 profile management <br>
S8 Report submission interface <br>
S9 Map-based report visualization <br>
S10 Report search and filtering interface <br>
S11 Report detail page <br>
S12 Report following system <br>
S13 Notification interface <br>
S14 Report status management system <br>
S15 Messaging interface  <br>
S16 System configuration panel  <br>
S17 Category management module <br>
S18 CSV export functionality <br>
S19 Public statistics dashboard <br>
S20 Private statistics dashboard <br>
<br>

**Infrastructure** <br>

ID Deliverable <br>
I1 Cloud deployment platform <br>
I2 Application hosting environment <br>
I3 Database server system <br>
I4 Media storage system <br>
I5 Backup and disaster recovery system <br>
I6 Map service integration <br>
<br>

**Documentation** <br>

ID Deliverable <br>
D1 System requirements document <br>
D2 System architecture and design document <br>
D3 API documentation <br>
D4 Test documentation <br>
D5 User manual and documentation <br>
<br>

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


