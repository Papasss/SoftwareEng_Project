## 1 `participium.services.auth_service.AuthService.authenticate`

Suggested test file: `test_authenticate.py`

Prototype: `authenticate(identifier: str, password: str) -> User`

| TC-ID | identifier | password | Expected | Fixture |
| :---- | :--------- | :------- | :------- | :------ |
|  |  |  |  |  |

## 2 `participium.core.utils.parse_date`

Suggested test file: `test_parse_date.py`

Prototype: `parse_date(value: str | None) -> datetime | None`


| TC-ID | value | Expected | Fixture |
|:------|:------|:----------|:---------|
| DATE-01 | `"2025-05-01"` | Datetime object returned | None |
| DATE-02 | `None` | None returned | None |
| DATE-03 | `"invalid-date"` | Invalid date format error | None |
| DATE-04 | `""` | Empty date value error | None |
| DATE-05 | `"2025/05/01"` | Unsupported date format error | None |

## 3 `participium.core.status_flow.ensure_transition_allowed`

Suggested test file: `test_status_flow.py`

Prototype: `ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus) -> bool`

Allowed transitions:
`Pending Approval -> Pending Approval | Assigned | Rejected`;
`Assigned -> Assigned | In Progress | Suspended | Resolved`;
`In Progress -> In Progress | Suspended | Resolved`;
`Suspended -> Suspended | In Progress | Resolved`;
`Rejected -> Rejected`;
`Resolved -> Resolved`.

| TC-ID  | current_status   | next_status       | Expected        | Fixture |
| :----  | :-------------   | :----------       | :-------------- | :------ |
|  3.1.1 | PENDING_APPROVAL | PENDING_APPROVAL  | True            | None    |
|  3.1.2 | PENDING_APPROVAL | ASSIGNED          | True            | None    |
|  3.1.3 | PENDING_APPROVAL | REJECTED          | True            | None    |
|  3.1.4 | PENDING_APPROVAL | RESOLVED          | ValidationError | None    |
|  3.1.5 | PENDING_APPROVAL | IN_PROGRESS       | ValidationError | None    |
|  3.1.6 | PENDING_APPROVAL | SUSPENDED         | ValidationError | None    |
|  3.2.1 | ASSIGNED         | ASSIGNED          | True            | None    |
|  3.2.2 | ASSIGNED         | IN_PROGRESS       | True            | None    |
|  3.2.3 | ASSIGNED         | SUSPENDED         | True            | None    |
|  3.2.4 | ASSIGNED         | RESOLVED          | True            | None    |
|  3.2.5 | ASSIGNED         | PENDING_APPROVAL  | ValidationError | None    |
|  3.2.6 | ASSIGNED         | REJECTED          | ValidationError | None    |
|  3.3.1 | IN_PROGRESS      | IN_PROGRESS       | True            | None    |
|  3.3.2 | IN_PROGRESS      | SUSPENDED         | True            | None    |
|  3.3.3 | IN_PROGRESS      | RESOLVED          | True            | None    |
|  3.3.4 | IN_PROGRESS      | ASSIGNED          | ValidationError | None    |
|  3.3.5 | IN_PROGRESS      | PENDING_APPROVAL  | ValidationError | None    |
|  3.3.6 | IN_PROGRESS      | REJECTED          | ValidationError | None    |
|  3.4.1 | SUSPENDED        | IN_PROGRESS       | True            | None    |
|  3.4.2 | SUSPENDED        | SUSPENDED         | True            | None    |
|  3.4.3 | SUSPENDED        | RESOLVED          | True            | None    |
|  3.4.4 | SUSPENDED        | ASSIGNED          | ValidationError | None    |
|  3.4.5 | SUSPENDED        | PENDING_APPROVAL  | ValidationError | None    |
|  3.4.6 | SUSPENDED        | REJECTED          | ValidationError | None    |
|  3.5.1 | REJECTED         | REJECTED          | True            | None    |
|  3.5.2 | REJECTED         | SUSPENDED         | ValidationError | None    |
|  3.5.3 | REJECTED         | RESOLVED          | ValidationError | None    |
|  3.5.4 | REJECTED         | ASSIGNED          | ValidationError | None    |
|  3.5.5 | REJECTED         | PENDING_APPROVAL  | ValidationError | None    |
|  3.5.6 | REJECTED         | IN_PROGRESS       | ValidationError | None    |
|  3.6.1 | RESOLVED         | RESOLVED          | True            | None    |
|  3.6.2 | RESOLVED         | SUSPENDED         | ValidationError | None    |
|  3.6.3 | RESOLVED         | REJECTED          | ValidationError | None    |
|  3.6.4 | RESOLVED         | ASSIGNED          | ValidationError | None    |
|  3.6.5 | RESOLVED         | PENDING_APPROVAL  | ValidationError | None    |
|  3.6.6 | RESOLVED         | IN_PROGRESS       | ValidationError | None    |
|  3.7.1 | PENDING_APPROVAL | NEW_STATUS        | ValidationError | None    |

## 4 participium.services.report_service.ReportService.create_report

Suggested test file: test_create_report.py

Prototype: create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report

| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | Expected | Fixture |
|:------|:----------|:-------------|:------|:-------------|:----------|:-----------|:--------|:---------------|:----------|:---------|
| REPORT-01 | Valid user | Valid category | "Broken streetlight" | "Light not working" | 45.0703 | 7.6869 | Valid image list | False | Report created successfully | Existing user and category |
| REPORT-02 | Valid user | Valid category | "Road damage" | "Large pothole" | 45.0703 | 7.6869 | [] | False | Report created without photos | Existing user and category |
| REPORT-03 | Valid user | Invalid category | "Garbage issue" | "Overflowing bins" | 45.0703 | 7.6869 | [] | False | Invalid category ID | Existing user |
| REPORT-04 | Valid user | Valid category | "" | "Description" | 45.0703 | 7.6869 | [] | False | Empty title error | Existing user and category |
| REPORT-05 | Valid user | Valid category | "Water leakage" | "" | 45.0703 | 7.6869 | [] | False | Empty description error | Existing user and category |
| REPORT-06 | Valid user | Valid category | "Traffic issue" | "Heavy blockage" | 999 | 7.6869 | [] | False | Invalid latitude value | Existing user and category |
| REPORT-07 | None | Valid category | "Street issue" | "Street blocked" | 45.0703 | 7.6869 | [] | False | User authentication required | Existing category |
| REPORT-08 | Valid user | Valid category | "Illegal dumping" | "Waste near road" | 45.0703 | 7.6869 | Invalid file type | False | Unsupported file format | Existing user and category |
| REPORT-09 | Valid user | Valid category | "Noise complaint" | "Construction noise" | 45.0703 | 7.6869 | Valid image list | True | Anonymous report created successfully | Existing user and category |
## 5 `participium.services.report_service.ReportService.update_status`

Suggested test file: `test_update_status.py`

Prototype: `update_status(report_id: int, operator: User, next_status_value: str, note: str | None = None) -> Report`

| TC-ID | report_id | operator  | next_status_value | note | Expected              | Fixture      |
| :---- | :-------- | :-------- | :---------------- | :--- | :-------------------- | :------------|
| 5.1   |  201      |  Citizen  |  Assigned         | None | AuthorizationError    | User, Report |
| 5.2   |  201      |  Admin    |  Assigned         | None | AuthorizationError    | User, Report |
| 5.3   |  201      |  Operator |  Assigned         | None | NotFoundError         | User, Report |
| 5.4   |  201      |  Operator |  Invalid Status   | None | ValidationError       | User, Report |
| 5.5   |  201      |  Operator |  Rejected         | None | ValidationError       | User, Report |
| 5.6   |  201      |  Operator |  Resolved         | None | ValidationError       | User, Report |
| 5.7   |  201      |  Operator |  Rejected         | The problem no longer exists. | ReportStatus.REJECTED | User, Report |

## 6 `participium.services.report_service.ReportService.list_public_reports`

Suggested test file: `test_public_reports.py`

Prototype: `list_public_reports(category_id: int | None = None, status: ReportStatus | None = None, date_from: datetime | None = None, date_to: datetime | None = None, sort: str = "desc") -> list[Report]`

| TC-ID | category_id | status | date_from | date_to | sort | Expected | Fixture |
|:------|:-------------|:--------|:------------|:----------|:------|:----------|:---------|
| LIST-01 | `None` | `None` | `None` | `None` | `"desc"` | All public reports | Existing public reports |
| LIST-02 | Valid category | `None` | `None` | `None` | `"desc"` | Filtered reports | Existing category and reports |
| LIST-03 | `None` | `Resolved` | `None` | `None` | `"desc"` | Resolved reports only | Existing resolved reports |
| LIST-04 | `None` | `None` | Valid start date | Valid end date | `"desc"` | Reports in date range | Existing dated reports |
| LIST-05 | `None` | `None` | `None` | `None` | `"asc"` | Ascending sorted reports | Existing public reports |
| LIST-06 | Invalid category | `None` | `None` | `None` | `"desc"` | Empty result or error | None |
| LIST-07 | `None` | Invalid status | `None` | `None` | `"desc"` | Validation error | None |
| LIST-08 | `None` | `None` | Future date | Past date | `"desc"` | Invalid date range | None |
| LIST-09 | `None` | `None` | `None` | `None` | Invalid sort value | Validation error | Existing public reports |


## 7 participium.services.messaging_service.MessagingService.send_message

Suggested test file: test_send_message.py

Prototype: send_message(report: Report, sender: User, body: str) -> Message

| TC-ID | report | sender | body | Expected | Fixture |
|:------|:--------|:--------|:------|:----------|:---------|
| MSG-01 | Valid report | Valid user | "Issue still unresolved" | Message created | Existing report and authorized user |
| MSG-02 | Valid report | Valid user | "" | Validation error | Existing report and authorized user |
| MSG-03 | Closed report | Valid user | "Need update" | Operation not allowed | Existing closed report |
| MSG-04 | Invalid report | Valid user | "Any update?" | Report not found | Existing user |
| MSG-05 | Valid report | Unauthorized user | "Checking status" | Authorization error | Existing report and unauthorized user |
| MSG-06 | Valid report | Valid user | Very long message | Message created | Existing report and authorized user |
| MSG-07 | Valid report | None | "Test message" | Authentication error | Existing report |

## 8 `participium.core.security.verify_password`

Suggested test file: `test_verify_password.py`

Prototype: `verify_password(password: str, password_hash: str) -> bool`

| TC-ID | password | password_hash | Expected | Fixture |
| :---- | :------- | :------------ | :------- | :------ |
|  |  |  |  |  |



## 9 `participium.services.notification_service.NotificationService.create_notification`

Suggested test file: `test_create_notification.py`

Prototype: `create_notification(user: User | None, notification_type: str, title: str, body: str, report: Report | None = None) -> Notification`

| TC-ID | user | notification_type | title | body | report | Expected | Fixture |
|:------|:------|:------------------|:------|:------|:--------|:----------|:---------|
| NOTIF-01 | Valid user | Valid type | `"Report updated"` | `"Your report status changed"` | Valid report | Notification created | Existing user and report |
| NOTIF-02 | `None` | System type | `"Maintenance notice"` | `"System update tonight"` | `None` | System notification created | None |
| NOTIF-03 | Valid user | Invalid type | `"Alert"` | `"Test notification"` | `None` | Notification type error | Existing user |
| NOTIF-04 | Valid user | Valid type | `""` | `"Notification body"` | `None` | Title validation error | Existing user |
| NOTIF-05 | Valid user | Valid type | `"Reminder"` | `""` | `None` | Body validation error | Existing user |
| NOTIF-06 | Valid user | Valid type | `"Status update"` | Very long message | Valid report | Notification created | Existing user and report |
| NOTIF-07 | Invalid user | Valid type | `"Warning"` | `"Unauthorized access"` | `None` | User validation error | None |

## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected | Fixture |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- | :------- | :------ |
|  |  |  |  |  |  |  |  |  |
