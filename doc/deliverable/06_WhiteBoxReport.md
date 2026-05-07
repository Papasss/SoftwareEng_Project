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

  $V(G) = \pi + 1$ = 11 + 1 = 12  

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

### Path Coverage

### Minimal Suite Test

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

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test

