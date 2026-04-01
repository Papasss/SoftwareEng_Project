# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.

| Use Case                   | Profile registration and management |
|:---------------------------|:------------------------------------|
| ID                         | UC-01 |
| Scope                      | Participium System |
| Level                      | User Goal / Subfunction | 
| Intention in Context       | To allow an unregistered user to create an account to become a *Citizen*, or a registered user to modify their personal data. |
| Primary actor              | Visitor (and consequently Citizen, Operator, Administrator) |
| Supporting actors          | None |
| Stakeholders' interests    | - *Visitor/Citizen:* Wants to register or update their data quickly and securely.<br>- *Administration:* Wants accurate user data compliant with privacy regulations to track the validity of reports. |
| Precondition               | The system must be online. The user must have a valid email address. |
| Minimum guarantees         | Partially entered data is not saved if the procedure is interrupted. Existing data is not overwritten in the event of a system error. |
| Success guarantees         | A new profile is created in the database, or existing profile data is updated. | 
| Trigger                    | The user clicks on "Register" or "Manage Profile". |
| Main success scenario      | 1. The Visitor requests access to the registration/profile area.<br>2. The system displays the form with data fields (name, email, password, etc.).<br>3. The Visitor fills out or modifies the required fields.<br>4. The Visitor submits the form.<br>5. The system validates the entered data (e.g., email format, secure password).<br>6. The system saves the data in the database.<br>7. The system confirms the completion of the operation. |
| Extensions                 | - *5a. Invalid or missing data:* The system highlights the incorrect fields and asks the user to correct them.<br>- *5b. Email already registered (during registration):* The system warns that the account already exists and suggests password recovery. |

<br>

| Use Case                   | Submit report |
|:---------------------------|:------------------------------------|
| ID                         | UC-02 |
| Scope                      | Participium System |
| Level                      | User Goal | 
| Intention in Context       | To allow a citizen to create and submit a detailed report, including its geographic location. |
| Primary actor              | Citizen |
| Supporting actors          | Map System External System |
| Stakeholders' interests    | - *Citizen:* Wants to accurately report a problem.<br>- *Operator:* Needs accurate and geolocated data to intervene. |
| Precondition               | The Citizen must be authenticated (handled via the inclusion of UC-01). The Map System must be reachable. |
| Minimum guarantees         | The report is not saved in case of a network failure; the user is notified of the error. |
| Success guarantees         | The report is saved in the system with a "New" status, linked to the author and the geographic coordinates. | 
| Trigger                    | The Citizen selects the "Submit new report" option. |
| Main success scenario      | 1. The Citizen starts the new report procedure.<br>2. The system executes `<<include>>` UC-01 (Profile registration and management) to verify the user's identity or prompt authentication.<br>3. The system displays the report form.<br>4. The Citizen enters the details of the problem (text, photos).<br>5. The Citizen requests to set the location on the map.<br>6. The system queries the Map System External System `<<support>>` to display the map and obtain the coordinates.<br>7. The Map System returns the positional data.<br>8. The Citizen confirms the submission.<br>9. The system saves the report and provides a ticket number. |
| Extensions                 | - *2a. Authentication failed:* The process is aborted.<br>- *6a. Map System unavailable:* The system allows text-based manual entry of the address as an alternative.<br>- *9a. Contextual tracking:* The system proposes to execute `<<extend>>` UC-03 (Track and view report) to immediately view the status of the newly created report. |


# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-XX | FR-XX  |
