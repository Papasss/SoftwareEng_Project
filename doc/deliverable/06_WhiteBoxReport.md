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

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test

## 3 `NotificationService.notify_status_change`

### Control Flow Graph

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test


## 4 `NotificationService.count_unread_message_notifications_by_report`

### Control Flow Graph

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test


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
