# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.

| Use Case                   | Profile registration and management |
|:---------------------------|:------------------------------------|
| ID                         | UC-01 |
| Scope                      | Log in Component |
| Level                      | Subfunction | 
| Intention in Context       | To allow an unregistered user to create an account to become a Citizen, or a registered user to modify their personal data. |
| Primary actor              | Citizen, Operator, Administrator |
| Supporting actors          | None |
| Stakeholders' interests    | - Citizen: Wants to register or update their data quickly and securely.<br>- Administrator: Wants accurate user data compliant with privacy regulations to track the validity of reports. |
| Precondition               | The system must be online. The user must have a valid email address. |
| Minimum guarantees         | Partially entered data is not saved if the procedure is interrupted. Existing data is not overwritten in the event of a system error. |
| Success guarantees         | A new profile is created in the database, or existing profile data is updated. | 
| Trigger                    | The user clicks on "Register" or "Manage Profile". |
| Main success scenario      | 1. The Visitor requests access to the registration/profile area.<br>2. The system displays the form with data fields (name, email, password, etc.).<br>3. The Visitor fills out or modifies the required fields.<br>4. The Visitor submits the form.<br>5. The system validates the entered data (e.g., email format, secure password).<br>6. The system saves the data in the database.<br>7. The system confirms the completion of the operation. |
| Extensions                 | - 5a. Invalid or missing data: The system highlights the incorrect fields and asks the user to correct them.<br>- 5b. Email already registered (during registration): The system warns that the account already exists and suggests password recovery. |

<br>

| Use Case                   | Submit report |
|:---------------------------|:------------------------------------|
| ID                         | UC-02 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow a citizen to create and submit a detailed report, including its geographic location. |
| Primary actor              | Citizen |
| Supporting actors          | Map System External System |
| Stakeholders' interests    | - Citizen: Wants to accurately report a problem.<br>- Operator: Needs accurate and geolocated data to intervene. |
| Precondition               | The Citizen must be authenticated (handled via the inclusion of UC-01). The Map System must be reachable. |
| Minimum guarantees         | The report is not saved in case of a network failure; the user is notified of the error. |
| Success guarantees         | The report is saved in the system with a "New" status | 
| Trigger                    | The Citizen selects the "Submit new report" option. |
| Main success scenario      | 1. The Citizen starts the new report procedure.<br>2. The system executes `<<include>>` UC-01 (Profile registration and management) to verify the user's identity or prompt authentication.<br>3. The system displays the report form.<br>4. The Citizen enters the details of the problem (text, photos).<br>5. The Citizen requests to set the location on the map.<br>6. The system queries the Map System External System `<<support>>` to display the map and obtain the coordinates.<br>7. The Map System returns the positional data.<br>8. The Citizen confirms the submission.<br>9. The system saves the report and provides a ticket number. |
| Extensions                 | - 2a. Authentication failed: The process is aborted.<br>- 6a. Map System unavailable: The system allows text-based manual entry of the address as an alternative.<br>- 9a. Contextual tracking: The system proposes to execute `<<extend>>` UC-03 (Track and view report) to immediately view the status of the newly created report. |

<br>

| Use Case                   | Track and view report |
|:---------------------------|:------------------------------------|
| ID                         | UC-03 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow users to view the details of an existing report and track its progress. |
| Primary actor              | Visitor (public visibility) / Citizen (private/detailed visibility) |
| Supporting actors          | None |
| Stakeholders' interests    | - Visitor/Citizen: Wants to know if the reported problem has been addressed or resolved. |
| Precondition               | At least one report must exist in the system. |
| Minimum guarantees         | The system protects the sensitive data of the reporter if the actor is merely a Visitor. |
| Success guarantees         | The system displays the requested information based on the user's permission level. | 
| Trigger                    | The user enters a tracking code or clicks on a report in the public map/list. |
| Main success scenario      | 1. The Visitor/Citizen requests to view a specific report.<br>2. The system evaluates the access level. If the user requests private details, the system executes `<<include>>` UC-01 for authentication.<br>3. The system retrieves the report data from the database.<br>4. The system displays the current status (e.g., "In Progress"), the history, and the public (or full, if the author) details. |
| Extensions                 | - 3a. Report not found: The system displays an error message "Tracking code does not exist". |

<br>

| Use Case                   | Download report and stats |
|:---------------------------|:------------------------------------|
| ID                         | UC-04 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow anyone (even unregistered users) to download aggregated data and public reporting on platform usage. |
| Primary actor              | Visitor |
| Supporting actors          | None |
| Stakeholders' interests    | - Visitor/Citizen: Wants to obtain Open Data regarding citizen reports. |
| Precondition               | The system must have pre-calculated or generatable statistical data. |
| Minimum guarantees         | No personal or sensitive data is exported in this function. |
| Success guarantees         | The system provides a file (e.g., PDF, CSV) containing the requested statistics. | 
| Trigger                    | The Visitor clicks on "Download Stats". |
| Main success scenario      | 1. The Visitor navigates to the statistics section.<br>2. The Visitor selects the desired format and time frame.<br>3. The system aggregates the public data (number of reports, most affected areas, resolution rates).<br>4. The system generates the file.<br>5. The system initiates the download to the Visitor's device. |
| Extensions                 | - 3a. Data unavailable for the selected period: The system warns the user and suggests a different time frame. |

<br>

| Use Case                   | Check notifications |
|:---------------------------|:------------------------------------|
| ID                         | UC-05 |
| Scope                      | Notification Component |
| Level                      | User Goal/ Subfunction | 
| Intention in Context       | To allow a registered user to read automatic alerts regarding their activities (e.g., "Your report has been resolved"). |
| Primary actor              | Citizen |
| Supporting actors          | Notification External System |
| Stakeholders' interests    | - Citizen: Wants to stay updated passively without having to manually search for their reports. |
| Precondition               | The Citizen must be logged in. The Notification System must be active. |
| Minimum guarantees         | The status of the notifications is not altered if reading them fails. |
| Success guarantees         | The list of notifications is displayed, and opened notifications are marked as "read". | 
| Trigger                    | The Citizen clicks on the notifications icon. |
| Main success scenario      | 1. The Citizen requests the list of notifications.<br>2. The system contacts the Notification External System `<<support>>`.<br>3. The external system returns the notification history for that user.<br>4. The system displays the list to the Citizen, highlighting unread ones.<br>5. The Citizen selects a notification.<br>6. The system marks the notification as read, communicating this back to the Notification System. |
| Extensions                 | - 2a. Notification System offline: The system displays a temporary service unavailability message. |

<br>

| Use Case                   | Send and receive messages |
|:---------------------------|:------------------------------------|
| ID                         | UC-06 |
| Scope                      | Participium App System |
| Level                      | User Goal/ Subfunction | 
| Intention in Context       | To manage direct text communication between a citizen and an operator regarding a specific report. |
| Primary actor              | Citizen (and consequently Operator) |
| Supporting actors          | Notification External System |
| Stakeholders' interests    | - Citizen / Operator: Need a channel to request clarifications or provide additional details. |
| Precondition               | The user must be authenticated. An open communication channel must exist. |
| Minimum guarantees         | Messages are not lost; in case of a sending failure, they remain as drafts or a clear error is shown. |
| Success guarantees         | The message is saved in the conversation history and the recipient is notified. | 
| Trigger                    | The user types text in the message area and presses "Send". |
| Main success scenario      | 1. The Citizen (or Operator) accesses the message area of a report.<br>2. They write the message content and click Send.<br>3. The system saves the message in the database, anchored to the report.<br>4. The system invokes the Notification External System `<<support>>` to alert the other party of the new message.<br>5. The system updates the on-screen chat showing the new message. |
| Extensions                 | - 4a. Notification failure: The message is saved and delivered within the system, but the user does not receive the push/email alert. The system logs the notification error. |

<br>

| Use Case                   | Review report |
|:---------------------------|:------------------------------------|
| ID                         | UC-07 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow an operator to analyze an incoming report to assess its validity, priority, and assignment. |
| Primary actor              | Operator |
| Supporting actors          | None |
| Stakeholders' interests    | - Operator: Wants to clearly understand the problem to decide on subsequent actions. |
| Precondition               | The Operator must have adequate privileges and be authenticated. There must be at least one report in the "New" status. |
| Minimum guarantees         | No modifications are made to the original data submitted by the citizen. |
| Success guarantees         | The Operator accesses all report information, including the private data of the reporter. | 
| Trigger                    | The Operator selects a report from the incoming work queue. |
| Main success scenario      | 1. The Operator opens the new reports queue.<br>2. They select a report.<br>3. The system loads and displays all details: text, media, location on the map, Citizen's data.<br>4. The Operator reads and analyzes the information to establish veracity and jurisdiction. |
| Extensions                 | - 3a. Media unreadable: The system displays a placeholder indicating that the attached photos/videos are corrupted or unavailable. |

<br>

| Use Case                   | Update report status |
|:---------------------------|:------------------------------------|
| ID                         | UC-08 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow an operator to modify the logical status of a report (e.g., Accepted, In Progress, Rejected, Resolved). |
| Primary actor              | Operator |
| Supporting actors          | None |
| Stakeholders' interests    | - Operator: Wants to keep track of the workflow.<br>- Citizen: Wants the visible progress to reflect reality. |
| Precondition               | The Operator must have analyzed the report (generally following UC-07). |
| Minimum guarantees         | If the update fails, the previous status is maintained. |
| Success guarantees         | The new status is saved in the database. The modification history is updated with the Operator's ID and a timestamp. | 
| Trigger                    | The Operator selects a new status from a dropdown menu within the report. |
| Main success scenario      | 1. The Operator, while viewing a report, decides to change its status.<br>2. They select the desired new status.<br>3. They add a mandatory/optional internal or public comment.<br>4. They confirm the operation.<br>5. The system updates the database and logs the audit trail of the action.<br>6. The system updates the interface confirming the modification. |
| Extensions                 | - 2a. Status transition not allowed: The system prevents the operator from skipping mandatory steps (e.g., jumping from "New" to "Closed" without passing through "Accepted") and displays an error. |

<br>

| Use Case                   | Manage system config |
|:---------------------------|:------------------------------------|
| ID                         | UC-09 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow administrators to modify basic platform parameters. |
| Primary actor              | Administrator |
| Supporting actors          | None |
| Stakeholders' interests    | - Administrator: Wants to adapt the system to new needs without having to alter the source code. |
| Precondition               | The user must be authenticated with the "Administrator" role. |
| Minimum guarantees         | Invalid modifications are not saved. The system keeps a backup of the previous configuration or allows a rollback. |
| Success guarantees         | The new configurations are applied to the system and become active immediately (or upon restart) for all users. | 
| Trigger                    | The Administrator accesses the control panel and selects "System Settings". |
| Main success scenario      | 1. The Administrator opens the configuration interface.<br>2. The system displays the various editable modules (e.g., category management).<br>3. The Administrator adds, removes, or modifies a parameter (e.g., creates a new "Public Parks" category).<br>4. The Administrator saves the changes.<br>5. The system validates the new parameters.<br>6. The system applies the configuration and shows a success message. |
| Extensions                 | - 5a. Configuration conflict: (e.g., deleting a category that already contains active reports). The system blocks the action and asks the Administrator to reassign the existing reports first. |

<br>

| Use Case                   | Download private stats |
|:---------------------------|:------------------------------------|
| ID                         | UC-10 |
| Scope                      | Participium App System |
| Level                      | User Goal | 
| Intention in Context       | To allow the administration to extract detailed reports for internal use, containing operator performance metrics and sensitive non-public data. |
| Primary actor              | Administrator |
| Supporting actors          | None |
| Stakeholders' interests    | - Administrator/Management: Needs precise data to evaluate staff and service efficiency. |
| Precondition               | The user must be authenticated with the "Administrator" role. |
| Minimum guarantees         | Access to this data is strictly logged for security and audit purposes. |
| Success guarantees         | The Administrator receives a file containing the requested sensitive data. | 
| Trigger                    | The Administrator clicks on "Export Internal Report". |
| Main success scenario      | 1. The Administrator accesses the advanced reporting area.<br>2. They set the search filters.<br>3. They request the generation of the report.<br>4. The system queries the database, accessing private tables as well.<br>5. The system compiles the file (e.g., an Excel spreadsheet).<br>6. The system initiates the download and logs the export action in the security logs. |
| Extensions                 | - 4a. Excessive data volume: If the query is too heavy, the system warns that the report will be generated in the background and emailed to the Administrator once ready. |


# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-XX | FR-XX  |
