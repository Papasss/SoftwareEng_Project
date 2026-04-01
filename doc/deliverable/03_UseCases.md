# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.
  
| Use Case                | Profile registration and management   | Submit Report                         |
|:------------------------|:--------------------------------------|:--------------------------------------|
| ID                      | UC 01                                 | UC 02
| Scope                   | Login Component                       | App system                            |
| Level                   | Subfunction                           | User goal                             |
| Intention in Context    | It allows to user to create an account in order to use all apps functionalities | It allows a citizen to create and submit a detailed report, including its geographic location | 
| Primary actor           | Citizen                               | Citizen                               |
| Supporting actors       | Authentication system                 | Map System External System            |
| Stakeholders' interests | Visitor/Citizen: Wants to register or update their data quickly and securely 
                            Administration: Wants accurate user data compliant with privacy regulations to track the validity of reports                   | Citizen: Wants to accurately report a problem
                                                                    Operator: Needs accurate and geolocated data to intervene                             |     
| Precondition            | The system must be online. The user must have a valid email address             | The Citizen must be authenticated (handled via the inclusion of UC-01). The Map System must be reachable | 
| Minimum guarantees      | Partially entered data is not saved if the procedure is interrupted. 
                            Existing data is not overwritten in the event of a system error.                |  The report is not saved in case of a network failure; the user is notified of the error. | 
| Success guarantees      | A new profile is created in the database, or existing profile data is updated   |  The report is saved in the system with a "New" status | 
| Trigger                 | The user clicks on "Register" or "Manage Profile"                               |  The Citizen selects the "Submit new report" option | 
| Main success scenario   | 1 The Citizen requests access to the registration/profile area.
                            2 The system displays the form with data fields (name, email, password, etc.).
                            3 The Citizen fills out or modifies the required fields.
                            4 The Citizen submits the form.
                            5 The system validates the entered data (e.g., email format, secure password).
                            6 The system saves the data in the database.
                            7 The system confirms the completion of the operation.                          |  
                             
                            1 The Citizen starts the new report procedure.
                            2 The system executes <<include>> UC-01 (Profile registration and management) to verify the
                              user's identity or prompt authentication.
                            3 The system displays the report form.
                            4 The Citizen enters the details of the problem (text, photos).
                            5 The Citizen requests to set the location on the map.
                            6 The system queries the Map System External System <<support>> to display the map and
                              obtain the coordinates.
                            7 The Map System returns the positional data.
                            8 The Citizen confirms the submission.
                            9 The system saves and public the report.                                       |

| Extensions              | 5a. Invalid or missing data: The system highlights the incorrect fields 
                               and asks the user to correct them.
                            5b. Email already registered (during registration): The system warns that the 
                               account already exists and suggests password recovery.                       |

                            2a. Authentication failed: The process is aborted.
                            6a. Map System unavailable: The system allows text-based manual entry of the address as an
                                alternative.
                            9a. Contextual tracking: The system proposes to execute <<extend>> UC-03 (Track and view
                                report) to immediately view the status of the newly created report.         |


# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-XX | FR-XX  |
