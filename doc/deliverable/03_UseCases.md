# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.

<br>

| Use Case | UC-01 User authentication and profile management |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The visitor wants to register, log in, and manage their profile |
| Primary actor | Visitor |
| Supporting actors | - |
| Stakeholder's Interests | User: wants secure access <br> System: ensures authentication |
| Precondition | - |
| Minimum guarantees | User data is protected |
| Success guarantees | The user is authenticated successfully |
| Trigger | The visitor selects login/register |
| Main success scenario | 1. The visitor selects authentication <br> 2. The system shows form <br> 3. The visitor enters details <br> 4. The system validates data <br> 5. The system logs in/registers user <br><br> The use case terminates with success |
| Extensions | 3a.1 Invalid input <br> 3a.2 The system shows error and restarts |

<br>

| Use Case | UC-02 Submit report |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The citizen wants to submit a report |
| Primary actor | Citizen |
| Supporting actors | Map System |
| Stakeholder's Interests | Citizen: report issue <br> System: collect valid reports |
| Precondition | User is authenticated |
| Minimum guarantees | Partial report is saved |
| Success guarantees | Report is submitted successfully |
| Trigger | Citizen selects submit report |
| Main success scenario | 1. Citizen selects submit report <br> 2. System shows form <br> 3. Citizen enters details and location <br> 4. System validates <br> 5. System saves report <br><br> The use case terminates with success |
| Extensions | 3a.1 Invalid data <br> 3a.2 System shows error |

<br>

| Use Case | UC-03 Track and view report |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The citizen wants to track and view reports |
| Primary actor | Citizen |
| Supporting actors | - |
| Stakeholder's Interests | Citizen: track progress |
| Precondition | Reports exist |
| Minimum guarantees | Reports remain accessible |
| Success guarantees | Reports are displayed |
| Trigger | Citizen selects view reports |
| Main success scenario | 1. Citizen selects reports <br> 2. System retrieves data <br> 3. System displays reports <br><br> The use case terminates with success |
| Extensions | 2a.1 No reports <br> 2a.2 System shows message |

<br>

| Use Case | UC-04 Export reports (CSV) |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The operator wants to export reports |
| Primary actor | Operator |
| Supporting actors | - |
| Stakeholder's Interests | Operator: data access |
| Precondition | Reports exist |
| Minimum guarantees | Data integrity maintained |
| Success guarantees | Reports exported successfully |
| Trigger | Operator selects export |
| Main success scenario | 1. Operator selects export <br> 2. System generates CSV <br> 3. System provides download <br><br> The use case terminates with success |
| Extensions | 2a.1 Export fails <br> 2a.2 System shows error |

<br>

| Use Case | UC-05 View notifications |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The citizen wants to view notifications |
| Primary actor | Citizen |
| Supporting actors | Notification System |
| Stakeholder's Interests | Citizen: stay informed |
| Precondition | Notifications exist |
| Minimum guarantees | Notifications stored |
| Success guarantees | Notifications displayed |
| Trigger | Citizen opens notifications |
| Main success scenario | 1. Citizen opens notifications <br> 2. System retrieves data <br> 3. System displays notifications <br><br> The use case terminates with success |
| Extensions | 2a.1 System unavailable <br> 2a.2 Show error |

<br>

| Use Case | UC-06 Exchange messages |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The citizen wants to exchange messages |
| Primary actor | Citizen |
| Supporting actors | Notification System |
| Stakeholder's Interests | Users: communication |
| Precondition | Users exist |
| Minimum guarantees | Messages stored |
| Success guarantees | Message sent successfully |
| Trigger | Citizen sends message |
| Main success scenario | 1. Citizen writes message <br> 2. System sends message <br> 3. Receiver gets notification <br><br> The use case terminates with success |
| Extensions | 2a.1 Failure <br> 2a.2 Error shown |

<br>

| Use Case | UC-07 Review report |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The operator wants to review reports |
| Primary actor | Operator |
| Supporting actors | - |
| Stakeholder's Interests | System: validate reports |
| Precondition | Report exists |
| Minimum guarantees | Report retained |
| Success guarantees | Report reviewed |
| Trigger | Operator selects report |
| Main success scenario | 1. Operator opens report <br> 2. System shows details <br> 3. Operator reviews <br><br> The use case terminates with success |
| Extensions | 2a.1 Error <br> 2a.2 System shows error |

<br>

| Use Case | UC-08 Update report status |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The operator wants to update report status |
| Primary actor | Operator |
| Supporting actors | - |
| Stakeholder's Interests | Citizen: track progress |
| Precondition | Report exists |
| Minimum guarantees | Previous data preserved |
| Success guarantees | Status updated |
| Trigger | Operator selects update |
| Main success scenario | 1. Operator selects report <br> 2. Operator updates status <br> 3. System saves update <br><br> The use case terminates with success |
| Extensions | 2a.1 Invalid update <br> 2a.2 System shows error |

<br>

| Use Case | UC-09 Manage system config |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The administrator wants to manage system configuration |
| Primary actor | Administrator |
| Supporting actors | - |
| Stakeholder's Interests | System: proper functioning |
| Precondition | Admin logged in |
| Minimum guarantees | Config saved |
| Success guarantees | Configuration updated |
| Trigger | Admin selects config |
| Main success scenario | 1. Admin opens settings <br> 2. Admin updates config <br> 3. System saves <br><br> The use case terminates with success |
| Extensions | 2a.1 Invalid config <br> 2a.2 Error shown |

<br>

| Use Case | UC-10 Download private stats |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The administrator wants to download private statistics |
| Primary actor | Administrator |
| Supporting actors | - |
| Stakeholder's Interests | Admin: data access |
| Precondition | Data exists |
| Minimum guarantees | Data integrity maintained |
| Success guarantees | Stats downloaded |
| Trigger | Admin selects download |
| Main success scenario | 1. Admin selects stats <br> 2. System prepares data <br> 3. System downloads file <br><br> The use case terminates with success |
| Extensions | 2a.1 Failure <br> 2a.2 Error shown |

<br>

| Use Case | UC-11 Follow report |
|:----------|:----------------------|
| Scope | Participium System |
| Level | User-goal |
| Intention in context | The citizen wants to follow a report to receive updates |
| Primary actor | Citizen |
| Supporting actors | Notification System |
| Stakeholder's Interests | Citizen: stay informed |
| Precondition | Report exists |
| Minimum guarantees | Follow preference saved |
| Success guarantees | User receives updates |
| Trigger | Citizen selects follow |
| Main success scenario | 1. Citizen selects report <br> 2. System shows follow option <br> 3. Citizen confirms <br> 4. System registers follow <br><br> The use case terminates with success |
| Extensions | 3a.1 Cancel <br> 3a.2 Not saved |




# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-XX | FR-XX  |
