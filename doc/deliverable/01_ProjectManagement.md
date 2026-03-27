# Product Breakdown Structure (PBS)

| ID  | Deliverable                           | Type           | Notes                                            |
|:----|:--------------------------------------|:---------------|:-------------------------------------------------|
| S1  | Report management service             | Software       | Backend: Core report life-cycle logic            |
| S2  | User account management service       | Software       | Backend: Authentication logic                    |
| S3  | Notification service                  | Software       | Backend: Email and in-app alert engine           |
| S4  | Messaging service                     | Software       | Backend: Communication logic                     |           
| S5  | Portal interface                      | Software       | Frontend: Main landing page and private sections |
| S6  | Registration and login interface      | Software       | Frontend: UI for authentication                  |
| S7  | Profile management                    | Software       | Frontend: Profile and preferences settings       |
| S8  | Report submission interface           | Software       | Frontend: UI for Report Submission.            |
| S9  | Map-based report visualization        | Software       | Frontend: Interactive OSM visualization        |
| S10 | Report search and filtering interface | Software       | Frontend: Table view with filters              |
| S11 | Report detail page                    | Software       | Frontend: Full report history and media        |
| S12 | Report following system               | Software       | Frontend: Subscription to report updates       |
| S13 | Notification interface                | Software       | Frontend: User-side alert dashboard            |
| S14 | Report status management system       | Software       | Frontend: Status transition tools             |
| S15 | Messaging interface                   | Software       | Frontend: Users communication UI                        |
| S16 | System configuration panel            | Software       | Frontend: Global system parameters               |
| S17 | Category management module            | Software       | Frontend: Dynamic report category tools          |
| S18 | CSV export functionality              | Software       | Transparency: Open Data extraction tools      |
| S19 | Private statistics dashboard          | Software       | Transparency: Public trend charts             |
| S20 | Public statistics dashboard           | Software       | Transparency: Private trend charts        |
| I1  | Cloud deployment platform             | Infrastructure | Deployment: CI/CD and hosting setup           |
| I2  | Application hosting environment       | Infrastructure | Deployment: Web/App server configuration      |
| I3  | Database server system                | Infrastructure | Deployment: Managed DB instance: User accounts database, Reports database, Messaging database, Notifications database               |
| I4  | Media storage system                  | Infrastructure | Deployment: Blob/File server for media: Photos/media storage for reports        |
| I5  | Backup and disaster recovery system   | Infrastructure | Deployment: Data safety protocols             |
| I6  | Map service integration               | Infrastructure | Deployment: OSM API/Proxy integration         |
| D1  | Requirements document                 | Documentation  | Deliverable: Functional/Technical specs       |
| D2  | Architecture and design document      | Documentation  | Deliverable: ERD and Architectural diagrams   |
| D3  | API documentation                     | Documentation  | Deliverable: Backend technical reference      |
| D4  | Test Documentation                    | Documentation  | Deliverable: QA and testing strategy          |
| D5  | User Manual and Documentation         | Documentation  | Deliverable: End-user manual, Municipal manual and Administrator                  |


**Software** <br>

ID Deliverable <br>
S1 Report management service <br>
S2 User account management service <br>
S3 Notification service <br>
S4 Messaging service <br>
S5 Portal interface <br>
S6 registration and login interface <br>
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
D1 Requirements document <br>
D2 Architecture and design document <br>
D3 API documentation <br>
D4 Test documentation <br>
D5 User manual and documentation <br>
<br>

**Description** <br>
The first breakdown concerns the project’s main areas, namely the technical, infrastructure and documentation aspects; this breakdown enables us to allocate resources to individual modules, particularly the ‘software’ section, where functionalities need to be developed using different development environments and independent working groups; for this reason, and given the considerable number of tasks involved, it was decided to further divide it into three sections: ‘Back-end’, ‘Front-end’ and ‘Transparency’.
Each deliverable is intended as a package of tasks required to develop a product component that provides a service to the user, as specified in the project documentation.

---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID   | Work package               | Traced PBS outputs (IDs)                    |
|:-----|:---------------------------|:--------------------------------------------|
| WP1  | PROJECT MANAGEMENT         | D1                                          |
| WP2  | REQUIREMENTS               | D1                                          |
| WP3  | DESIGN AND ARCHITECTURES   | S5, S8, S10, S13, S15, I1, I2, D2           |
| WP4  | IMPLEMENTATION             | S1-20, I3-6                                 |
| WP5  | TESTING                    | D4                                          |
| WP6  | DEPLOYMENT                 | D3, D5                                      |
| WP7  | MAINTENANCE                | S1-20, I5                                   |


**Description** <br>
The division into project phases followed the incremental software development model, which places great emphasis on avoiding a monolithic, one-way process. For this reason, it was decided to include the ‘Maintenance’ phase as a fundamental element for the future of the project. Furthermore, importance was attached to the project’s design phases, understood as business decisions, by initially including the ‘Project Management’ phase, which is useful as the client is no longer merely a client but is involved in the process steps, engaging in constant dialogue with the project manager.

---

# Gantt, dependencies, and critical path

## Activity table
| ID    | Activity                              | Duration   | Dependencies   | Start           | End               | Critical | Milestone |
|:------|:--------------------------------------|:-----------|:---------------|:----------------|:------------------|:---------|:----------|
| WP1.1 | DEFINITION OF BUSINESS REQUIREMENTS   | 1 week     | No dependecies | Start of week 1 | End of week 1     | Yes      | Yes       |
| WP1.2 | DEFINITION OF TIME AND RESOURCE       | 1 week     | WP1.1          | Start of week 1 | End of week 1     | No       | No        |
| WP1.3 | PLANNING                              | 1 week     | WP1.2          | Start of week 1 | End of week 1     | No       | Yes       |
| WP2.1 | DEFINITION OF FUNCTIONAL REQUIREMENTS | 1 week     | WP1.1          | Start of week 2 | End of week 2     | Yes      | No        |
| WP2.2 | DEFINITION OF TECHNICAL REQUIREMENTS  | 1 week     | WP2.1          | Start of week 2 | End of week 2     | Yes      | Yes       |
| WP3.1 | DEFINITION OF ARCHITECTURE            | 3 weeks    | WP2.2          | Start of week 3 | End of week 5     | Yes      | No        |
| WP3.2 | DATABASE DESIGN                       | 3 weeks    | WP2.2          | Start of week 3 | End of week 5     | No       | No        | 
| WP3.3 | WEB AND MOBILE DESIGN                 | 3 weeks    | WP2.2          | Start of week 3 | End of week 5     | No       | Yes       |
| WP4.1 | IMPLEMENTATION OF BACK-END            | 20 weeks   | WP3.1, WP3.2   | Start of week 6 | End of week 25    | Yes      | No        |
| WP4.2 | IMPLEMENTATION OF FRONT-END           | 23 weeks   | WP3.3          | Start of week 6 | End of week 28    | Yes      | No        |
| WP4.3 | STATISTICS REPORTS                    | 21 weeks   | WP4.1, WP4.2   | Start of week 8 | End of week 28    | No       | Yes       |
| WP5.1 | UNIT TESTING                          | 2 weeks    | WP4.3          | Start of week 28 | End of week 29   | Yes      | No        |
| WP5.2 | INTEGRATION TESTING                   | 2 weeks    | WP5.1          | Start of week 30 | End of week 31   | Yes      | No        |
| WP5.3 | SYSTEM TESTING                        | 2 weeks    | WP5.2          | Start of week 32 | End of week 33   | Yes      | No        |
| WP5.4 | UAT                                   | 2 weeks    | WP5.3          | Start of week 34 | End of week 35   | Yes      | Yes       |
| WP6.1 | PLANNING SESSION WITH USER            | 1 week     | WP5.4          | Start of week 36 | End of week 36   | No       | No        |
| WP6.2 | TICKETING AND GO LIVE                 | 1 week     | WP5.4          | Start of week 37 | End of week 37   | Yes      | No        |
| WP6.3 | DEPLOY IN PROD ENVIRONMENT            | 1 week     | WP6.2          | Start of week 38 | End of week 38   | Yes      | Yes       |
| WP7.1 | ADJUSTMENTS OR BUG FIXES              | 2 weeks    | WP6.3          | Start of week 39 | End of week 40   | No       | No        | 

## Critical path
`WP1.1 → WP2.1 → WP2.2 → WP3.1 → WP4.1 → WP4.2 → WP5.1 → WP5.2 → WP5.3 → WP5.4 → WP6.2 → WP6.3`

**Description** <br>
The Gantt chart strictly follows the structure defined in the WBS table, where tasks from the same area have been grouped together and timelines and dependencies have been defined. This is particularly the case during the implementation and initial testing phases, given the strong interdependencies and overlapping work involved. The project timeline has been set at 10 working months, and the metric used to define ‘Critical’ steps involves prioritising the task that allows the team to move on to the next area of the WBS, i.e. to proceed with the agreed schedule. Finally, regarding the ‘Maintenance’ section, only the ‘adjustments or bug fixes’ task has been included, as it is the only activity that could be part of the first delivery; the rest concerns future phases of the project.


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
| ID  | Risk                         | Category            | P  | I  | P×I | Level     | Mitigation / Response strategy                     |
|:----|:------------------------|:--------------------|---:|---:|----:|:----------|:---------------------------------------------------|
| R1  | Staff retention              | Organizational        | 4  | 3  | 12  | High      | assign appropriate tasks to staff and ensure they receive benefits and training |
| R2  | Optimistic estimates         | Organizational        | 3  | 4  | 12  | High      | increase efforts from every member of the project and negotiate a new deadline |
| R3  | Budget cut                   | Organizational        | 4  | 5  | 20  | Very High | consider to reduce the profit margin     |
| R4  | Content switch               | Organizational        | 4  | 2  | 8   | Medium    | define staff-group assignment and increase staff assumption    |
| R5  | Communication                | Operational           | 3  | 3  | 9   | Medium    | use proper language for each stakeholder  |
| R6  | Standard procedure lack      | Operational           | 2  | 3  | 6   | Medium    | invest more time to align every stakeholder and use same operational tools  |
| R7  | Know-how lack                | Operational/Technical | 2  | 4  | 8   | Medium    | promote more intensive courses and training sessions  |
| R8  | Scope creep                  | Requirements/Scope    | 4  | 4  | 16  | High      | rewrite scheduled activities with business and make precise requirements  |
| R9  | Unclear requirements         | Requirements/Scope    | 3  | 4  | 12  | High      | schedule frequently calls with business in order to prevent misunderstandings  |
| R10 | Instability of Dev platform  | Technical             | 2  | 3  | 6   | Medium    | if happen often, consider to reallocate resources to another part of the project meanwhile platform is not avaible  |
| R11 | Technical debit              | Technical             | 3  | 4  | 12  | High      | make it simple but think for the future feature and for scalability  |
| R12 | Test coverage                | Technical             | 4  | 5  | 20  | Very High | follow a well-established methodology, such as Scrum, to avoid releasing untested code  |
| R13 | Resources consumption        | Technical             | 3  | 3  | 9   | Medium    | focus on the quality of the code and not the quantity, consider pair programming  |
| R14 | Data breach                  | Security/Privacy      | 2  | 5  | 10  | High      | creation of backup data and if necessary block access to app  |
| R15 | COTS instability             | External/Third-party  | 2  | 2  | 4   | Low       | using always the latest version of components and if necessary change it  |


**Description** <br>
The two more critical risks are 'Budget cut' and 'Test coverage' not only because they affect everyone’s work within the project, whatever their role, but also because they are activities for which we are accountable to the business and that part is always critical. Then it is not always possible to know which risks will materialise, particularly unforeseen ones; for this reason, the project manager should constantly assess the resources at their disposal and determine the appropriate measures to mitigate the problem, like 'early validation' and 'adding buffer', especially if time and staff are running short.