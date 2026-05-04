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

    

### Edge Coverage

### Condition Coverage

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

