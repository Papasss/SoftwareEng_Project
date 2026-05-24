## 1 `ReportService.create_report`

### Control Flow Graph

 - `![](../data/img/report_service_control_flow.png)`

### Atomic Conditions

  1) Parsing category_id to int
  2) Checking category exists
  3) Checking category is active
  4) Checking title is not None
  5) Checking description is not None
  6) Checking latitude is not None
  7) Checking longitude is not None
  8) Parsing latitude to float
  9) Parsing longitude to float
  10) Checking photo is valid
  11) Counting number of photos: max 3
  12) Create report object
  13) Add report to repository
  14) Flush session
  15) Add photo to report
  16) Add Report to ReportStatusHistory
  17) Commit changes

### Structural Lower Bound

  The formula involves adding +1 to the decisional nodes
  $V(G) = \pi + 1$ = 8 + 1 = 9  

### Node Coverage

 - reachable coverage: 100%
 - minimum number of test case: 8
 - test cases: 
      - TC1(category_id: "7"; "A valid active category is required.")
      - TC2(category_id: 999; "A valid active category is required.")    
      - TC3(title: None; "Title and description are required.")
      - TC4(latitude: None; "Latitude and longitude are required.")
      - TC5(resolved_longitude: "sette"; "Latitude and longitude must be valid numbers.")
      - TC6(valid_photos: []; "At least one photo is required.")
      - TC7(valid_photos: [FileStorage(filename="photo1.jpg"), FileStorage(filename="photo2.jpg"), FileStorage(filename="photo3.jpg"), FileStorage(filename="photo4.jpg")]; "A report can contain at most 3 photos.")
      - TC8(user2, 2, "proper_title", "proper_desc", 15.0, 22.0, [FileStorage(filename="photo1.jpg")], True)

### Edge Coverage

 - reachable coverage: 100%
 - minimum number of test case: 8
 - test cases: 
      - TC1(category_id: "7"; "A valid active category is required.")
      - TC2(category_id: None; "A valid active category is required.")    
      - TC3(title: None; "Title and description are required.")
      - TC4(latitude: None; "Latitude and longitude are required.")
      - TC5(resolved_longitude: "sette"; "Latitude and longitude must be valid numbers.")
      - TC6(valid_photos: []; "At least one photo is required.")
      - TC7(valid_photos: [FileStorage(filename="photo1.jpg"), FileStorage(filename="photo2.jpg"), FileStorage(filename="photo3.jpg"), FileStorage(filename="photo4.jpg")]; "A report can contain at most 3 photos.")
      - TC8(user2, 2, "proper_title", "proper_desc", 15.0, 22.0, [FileStorage(filename="photo1.jpg"), FileStorage(filename="")], True)

### Condition Coverage

 - reachable coverage: 100%
 - minimum number of test case: 13
 - test cases: 
      - TC1(category_id: "7"; "A valid active category is required.")
      - TC2(category_id: [1, 2]; "A valid active category is required.")
      - TC3(category_id: 2 --> is_active = False; "A valid active category is required.")
      - TC4(category_id: 999; "A valid active category is required.") 
      - TC5(title: None; "Title and description are required.")
      - TC6(description: None; "Title and description are required.")
      - TC7(latitude: None; "Latitude and longitude are required.")
      - TC8(longitude: None; "Latitude and longitude are required.")
      - TC9(resolved_longitude: "sette"; "Latitude and longitude must be valid numbers.")
      - TC10(resolved_latitude: [14.0]; "Latitude and longitude must be valid numbers.")
      - TC11(valid_photos: []; "At least one photo is required.")
      - TC12(valid_photos: [FileStorage(filename="photo1.jpg"), FileStorage(filename="photo2.jpg"), FileStorage(filename="photo3.jpg"), FileStorage(filename="photo4.jpg")]; "A report can contain at most 3 photos.")
      - TC13(user2, 2, "proper_title", "proper_desc", 15.0, 22.0, [FileStorage(filename="photo1.jpg"), FileStorage(filename=""), None], True)

### Loop Coverage

 - reachable coverage: 100%
 - minimum number of test case: 4
 - test cases: 
      - TC1(valid_photos: []; "At least one photo is required.")
      - TC2(valid_photos: [FileStorage(filename="photo1.jpg")]; Success)
      - TC3(valid_photos: [FileStorage(filename="photo1.jpg"), FileStorage(filename="photo2.jpg"), FileStorage(filename="photo3.jpg")]; Success)   --> limit case
      - TC4(valid_photos: [FileStorage(filename="photo1.jpg"), FileStorage(filename="photo2.jpg"), FileStorage(filename="photo3.jpg"), FileStorage(filename="photo4.jpg")]; "A report can contain at most 3 photos.")

### Path Coverage

 - reachable coverage: unfeasible
 - minimum number of test case: 5 + 3$^n$
 - test cases: The loop condition for the possible photos occurs before the condition “if len(valid_photos) > 3”, resulting in potentially infinite paths 

### Minimal Suite Test

 - `test_create_report_raises_when_category_id_is_malformed`
 - `test_create_report_raises_when_category_is_inactive`
 - `test_create_report_raises_when_title_or_description_is_missing`
 - `test_create_report_raises_when_coordinates_are_missing`
 - `test_create_report_raises_when_coordinates_are_not_numeric`
 - `test_create_report_raises_when_more_than_three_photos_are_provided`
 - `test_create_report_persists_report_photo_and_status_history`

## 2 `MessagingService._resolve_recipient`

### Control Flow Graph

 - `![](../data/img/resolve_recipient_control_flow.png)`

### Atomic Conditions

1) Checking sender role is ADMIN or OPERATOR
2) Checking message.sender exists
3) Checking message.sender role is ADMIN or OPERATOR
4) Checking status_event.changed_by exists
5) Checking status_event.changed_by role is ADMIN or OPERATOR


### Structural Lower Bound

The formula involves adding +1 to the decisional nodes.
V(G) = π + 1 = 5 + 1 = 6

### Node Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(sender role ADMIN, returns report.reporter)
    - TC2(message sender role OPERATOR found in previous messages, returns message.sender)
    - TC3(status_event.changed_by role ADMIN/OPERATOR found in status history, returns status_event.changed_by)
    - TC4(no valid recipient found, returns None)

### Edge Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(sender role ADMIN, TRUE branch → returns report.reporter)
    - TC2(sender role not ADMIN/OPERATOR, previous message sender role OPERATOR found → returns message.sender)
    - TC3(no valid message sender found, status_event.changed_by role ADMIN/OPERATOR found → returns status_event.changed_by)
    - TC4(no valid message sender and no valid status history recipient found → returns None)

### Condition Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(sender role ADMIN → condition TRUE, returns report.reporter)
    - TC2(sender role not ADMIN/OPERATOR, message.sender exists and role is OPERATOR → conditions TRUE, returns message.sender)
    - TC3(message.sender not found, status_event.changed_by exists and role is ADMIN/OPERATOR → conditions TRUE, returns status_event.changed_by)
    - TC4(message.sender does not exist and status_event.changed_by does not exist → conditions FALSE, returns None)

### Loop Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(messages = [], status_history = [] → loops execute 0 iterations)
    - TC2(messages contains one valid OPERATOR sender → loop executes 1 iteration and returns message.sender)
    - TC3(messages empty, status_history contains one valid ADMIN/OPERATOR → status_history loop executes 1 iteration and returns status_event.changed_by)
    - TC4(messages and status_history contain no valid ADMIN/OPERATOR → loops execute completely and return None)

### Path Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(sender role ADMIN/OPERATOR → return report.reporter)
    - TC2(valid ADMIN/OPERATOR sender found in messages → return message.sender)
    - TC3(valid ADMIN/OPERATOR found in status_history → return status_event.changed_by)
    - TC4(no valid recipient found → return None)

All independent execution paths of the function are covered.

### Minimal Suite Test

- test_admin_sender_returns_reporter
- test_previous_operator_message_used
- test_status_history_operator_used
- test_no_recipient_returns_none

## 3 `NotificationService.notify_status_change`

### Control Flow Graph

- '![](../data/img/notify_status_change_control_flow.png)'

### Atomic Conditions

1) Checking if the report exists
2) Checking if the user to notify exists
3) Checking if the report status has actually changed
4) Checking if a notification for this change already exists
5) Checking if sending the notification succeeds

### Structural Lower Bound

The formula involves adding +1 to the decisional nodes:
V(G) = π + 1 = 5 + 1 = 6

### Node Coverage

- reachable coverage: 100%
- minimum number of test case: 5
- test cases:
    - TC1(report does not exist → raises ValueError)
    - TC2(user to notify does not exist → returns without notification)
    - TC3(report status has not changed → returns without notification)
    - TC4(notification already exists for this change → skips sending)
    - TC5(valid report, status changed, notification does not exist → notification sent successfully)

### Edge Coverage

- reachable coverage: 100%
- minimum number of test case: 5
- test cases:
    - TC1(report does not exist → raise exception)
    - TC2(user to notify does not exist → branch returns early)
    - TC3(status unchanged → branch returns early)
    - TC4(notification already exists → skip sending branch)
    - TC5(notification created and sent → normal execution path)

### Condition Coverage

- reachable coverage: 100%
- minimum number of test case: 5
- test cases:
    - TC1(report exists → FALSE, raises exception)
    - TC2(user exists → FALSE, return early)
    - TC3(status changed → FALSE, return early)
    - TC4(notification exists → TRUE, skip sending)
    - TC5(all TRUE conditions → notification sent successfully)

### Loop Coverage

- reachable coverage: 100%
- minimum number of test case: 3
- test cases:
    - TC1(empty list of users to notify → loop executes 0 iterations)
    - TC2(list of users to notify contains one valid user → loop executes 1 iteration)
    - TC3(list of users to notify contains multiple users → loop executes multiple iterations, notifications sent to each)

### Path Coverage

- reachable coverage: 100%
- minimum number of test case: 5
- test cases:
    - TC1(report does not exist → raise ValueError)
    - TC2(user does not exist → return early)
    - TC3(status unchanged → return early)
    - TC4(notification already exists → skip sending)
    - TC5(normal execution → notification sent)
- All independent execution paths of the function are covered.

### Minimal Suite Test

- test_notify_status_change_raises_when_report_does_not_exist
- test_notify_status_change_skips_when_user_does_not_exist
- test_notify_status_change_skips_when_status_unchanged
- test_notify_status_change_skips_when_notification_already_exists
- test_notify_status_change_sends_notification_successfully


## 4 `NotificationService.count_unread_message_notifications_by_report`

### Control Flow Graph

- `![](../data/img/count_unread_message_notifications_by_report_control_flow.png)`

### Atomic Conditions

1) Checking notification.report_id is None
2) Checking report_id already exists in counts dictionary

### Structural Lower Bound

The formula involves adding +1 to the decisional nodes.
V(G) = π + 1 = 2 + 1 = 3

### Node Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(empty notifications list → returns empty dictionary)
    - TC2(notification.report_id is None → continue branch executed)
    - TC3(valid report_id first occurrence → count initialized)
    - TC4(duplicate report_id found → count incremented)

### Edge Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(loop not entered → returns empty dictionary)
    - TC2(notification.report_id is None → TRUE branch executed)
    - TC3(notification.report_id valid → FALSE branch executed and count initialized)
    - TC4(existing report_id encountered again → count increment branch executed)

### Condition Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(notification.report_id is None → TRUE condition)
    - TC2(notification.report_id is not None → FALSE condition)
    - TC3(report_id not already in counts dictionary → initializes count)
    - TC4(report_id already exists in counts dictionary → increments existing count)

### Loop Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(notifications = [] → loop executes 0 iterations)
    - TC2(notifications contains one item with report_id = None → loop executes 1 iteration)
    - TC3(notifications contains one valid report_id → loop executes 1 iteration and initializes count)
    - TC4(notifications contains repeated report_id values → loop executes multiple iterations and increments count)

### Path Coverage

- reachable coverage: 100%
- minimum number of test case: 4
- test cases:
    - TC1(empty notifications list → return empty dictionary)
    - TC2(notification.report_id is None → continue loop)
    - TC3(valid report_id first occurrence → initialize count)
    - TC4(repeated report_id → increment count)
All independent execution paths of the function are covered.

### Minimal Suite Test

- test_returns_empty_dictionary_when_notifications_list_is_empty
- test_skips_notifications_with_none_report_id
- test_initializes_count_for_first_report_occurrence
- test_increments_count_for_duplicate_report_id

## 5 `UserService.update_user`

### Control Flow Graph

 - `![](../data/img/update_user_control_flow.png)`

### Atomic Conditions

  1) Checking username is not None
  2) Checkin username is equal to the one gets by his id
  3) Checking username is not None gets from the user repository
  4) Checking email is not None
  5) Checking email is equal to the one gets by his id
  6) Checking email is not None gets from the user repository
  7) Checking fields are not None
  8) Checking value is a String type
  9) Checking category_id is in payload
  10) Checking role is not None
  11) Checking category_id is not None
  12) Checking is_active is not None
  13) Checkin email_notifications_enabled is not None
  14) Commit changes

### Structural Lower Bound

  The formula involves adding +1 to the decisional nodes
  $V(G) = \pi + 1$ = 11 + 1 = 12  

### Node Coverage

 - reachable coverage: 100%
 - minimum number of test case: 3
 - test cases: 
      - TC1({username: "username_already_used"}; "Username already in use.")
      - TC2({email: "email_already_used@gmail.com"}; "Email already in use.")    
      - TC3({first_name: "Gianluca"}; return User)

### Edge Coverage

 - reachable coverage: 100%
 - minimum number of test case: 5
 - test cases: 
      - TC1({username: "username_already_used"}; "Username already in use.")
      - TC2({email: "email_already_used@gmail.com"}; "Email already in use.")    
      - TC3({}; return User)
      - TC4({"username": "new_user", "first_name": "  Mario  ", "role": "ADMIN", "category_id": 5, "is_active": True, "email_notifications_enabled": True}; return User)
      - TC5({"last_name": 12345, "category_id": 999}; return User)

### Condition Coverage

 - reachable coverage: 100%
 - minimum number of test case: 5
 - test cases: 
      - TC1({username: "username_already_used"}; "Username already in use.")    --> Precondition('get_by_username' return an User) 
      - TC2({email: "email_already_used@gmail.com"}; "Email already in use.")    --> Precondition('get_by_email' return an User) 
      - TC3({username: "old_user", email: "old_user@gmail.com", category_id: 5}; return User)
      - TC4({username: "new_user", email: "new_user@gmail.com"}; return User)    --> Precondition('get_by_email' and 'get_by_username' return None)    
      - TC5({username: "", email: "", "role": "admin"}; return User)

### Loop Coverage

 - reachable coverage: 100%
 - minimum number of test case: 4
 - test cases: 
      - TC1({role: "admin"}; return User) 
      - TC2({first_name: "Giuseppe"}; return User)
      - TC3({first_name: "Giuseppe", last_name: "Delli"}; return User)
      - TC4({first_name: "Giuseppe", last_name: "Delli", username: "gdl7", email: "giuseppe.delli@hotmail.com"}; return User)

### Path Coverage

 - reachable coverage: unfeasible
 - minimum number of test case: 2 + (3$^4$ * 2 * 3 * 2 * 2) = 1946
 - test cases: The loop condition for each field is limited at max 4 different fields, so the explosion of necessary path is limited at least 1946. The first 2 paths added represent the ValidationError paths.

### Minimal Suite Test

 - `test_update_user_raises_validation_error_when_username_already_in_use`
 - `test_update_user_raises_validation_error_when_email_already_in_use`
 - `test_update_user_converts_boolean_fields_to_bool`
 - `test_update_user_resolves_category_when_category_id_in_payload`
 - `test_update_user_complete_update_all_fields`
