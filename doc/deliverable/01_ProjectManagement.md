# Product Breakdown Structure (PBS)

| ID | Deliverable | Type  | Notes |
|:---|:------------|:--------------------------------------------------|:------|
| X# |             |                                                  |       |


---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID    | Work package               | Traced PBS outputs (IDs) |
|:------|:---------------------------|:-------------------------|
| WP 1  | PROJECT MANAGEMENT         | D8                       |
| WP 2  | REQUIREMENTS               | D1, D3                   |
| WP 3  | DESIGN AND ARCHITECTURES   | D2, I1, I6, I7           |
| WP 4  | IMPLEMENTATION             | S1-S21, A1-A7, T1-T4     |
| WP 5  | TESTING                    | D4, D5                   |
| WP 6  | DEPLOYMENT                 | D6, D7                   |
| WP 7  | MAINTENANCE                | ...                      |


---

# Gantt, dependencies, and critical path

## Activity table
| ID | Activity | Duration | Dependencies | Start | End | Critical | Milestone |
|:---|:---------|:---------|:-------------|:------|:----|:------|:---------|
| R# |          |          |              |       |     |       |          |


## Critical path
`X → X → X → ...`



---

# Risk Management

**Scales and thresholds**
- **Probability (P)**: 1 (rare) … 5 (almost certain)
- **Impact (I)**: 1 (minor) … 5 (critical)
- **Exposure**: `P × I` (range 1–25)

Risk level thresholds (by exposure):
- **Low**: 1–5
- **Medium**: 6–10
- **High**: 11–16
- **Very High**: >16



## Risks table
| ID | Risk | Category | P | I | P×I | Level | Mitigation / Response strategy |
|:---|:-----|:---------|--:|--:|----:|:------|:-------------------------------|
|  |      |          |   |   |     |       |                                |


