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
| DATE-01 | `"2025-05-01"` | Valid datetime | None |
| DATE-02 | `None` | None returned | None |
| DATE-03 | `"invalid-date"` | ValueError | None |
| DATE-04 | `""` | ValueError | None |
| DATE-05 | `"2025/05/01"` | Invalid format error | None |

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

| TC-ID | current_status | next_status | Expected | Fixture |
| :---- | :------------- | :---------- | :------- | :------ |
|  |  |  |  |  |

## 4 participium.services.report_service.ReportService.create_report

Suggested test file: test_create_report.py

Prototype: create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report

| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | Expected | Fixture |
|:------|:----------|:-------------|:------|:-------------|:----------|:-----------|:--------|:---------------|:----------|:---------|
| REPORT-01 | Valid user | Valid category | "Broken streetlight" | "Light not working" | 45.0703 | 7.6869 | Valid image list | False | Report created | Existing user and category |
| REPORT-02 | Valid user | Valid category | "Road damage" | "Large pothole" | 45.0703 | 7.6869 | [] | False | Report created | Existing user and category |
| REPORT-03 | Valid user | Invalid category | "Garbage issue" | "Overflowing bins" | 45.0703 | 7.6869 | [] | False | Category error | Existing user |
| REPORT-04 | Valid user | Valid category | "" | "Description" | 45.0703 | 7.6869 | [] | False | Validation error | Existing user and category |
| REPORT-05 | Valid user | Valid category | "Water leakage" | "" | 45.0703 | 7.6869 | [] | False | Validation error | Existing user and category |
| REPORT-06 | Valid user | Valid category | "Traffic issue" | "Heavy blockage" | 999 | 7.6869 | [] | False | Invalid coordinates | Existing user and category |
| REPORT-07 | None | Valid category | "Street issue" | "Street blocked" | 45.0703 | 7.6869 | [] | False | Authentication error | Existing category |
| REPORT-08 | Valid user | Valid category | "Illegal dumping" | "Waste near road" | 45.0703 | 7.6869 | Invalid file type | False | File validation error | Existing user and category |
| REPORT-09 | Valid user | Valid category | "Noise complaint" | "Construction noise" | 45.0703 | 7.6869 | Valid image list | True | Anonymous report created | Existing user and category |
| REPORT-10 | Valid user | Valid category | Very long title | "Description" | 45.0703 | 7.6869 | [] | False | Validation error | Existing user and category |

## 5 `participium.services.report_service.ReportService.update_status`

Suggested test file: `test_update_status.py`

Prototype: `update_status(report_id: int, operator: User, next_status_value: str, note: str | None = None) -> Report`

| TC-ID | report_id | operator | next_status_value | note | Expected | Fixture |
| :---- | :-------- | :------- | :---------------- | :--- | :------- | :------ |
|  |  |  |  |  |  |  |

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

Prototype: `create_notification(user: User | None, notification_type: NotificationType, title: str, body: str, report: Report | None = None) -> Notification | None`

| TC-ID | user | notification_type | title | body | report | Expected | Fixture |
| :---- | :--- | :---------------- | :---- | :--- | :----- | :------- | :------ |
|  |  |  |  |  |  |  |  |

## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected | Fixture |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- | :------- | :------ |
|  |  |  |  |  |  |  |  |  |
