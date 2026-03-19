# Product Breakdown Structure (PBS)

| ID | Deliverable | Type  | Notes |
|:---|:------------|:--------------------------------------------------|:------|
| X# |             |                                                  |       |


---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID  | Work package | Traced PBS outputs (IDs) |
|:----|:-------------|:--------------------------|
| #.# |              |                           |


---

# Gantt, dependencies, and critical path

## Activity table
| ID  | Activity | Duration | Dependencies | Start | End | Critical | Milestone |
|:------|:---------|:---------|:-------------|:------|:----|:---------|:----------|
| WP1.1 | DEFINITION OF BUSINESS REQUIREMENTS         | 1 week         | No dependecies        | Start of week 1      | End of week 1    | Yes       | Yes       |
| WP1.2 | DEFINITION OF TIME AND RESOURCE         | 1 week         | WP1.1             | Start of week 1      | End of week 1    | No         | No          |
| WP1.3 | PLANNING         | 1 week         | WP1.2             | Start of week 1      | End of week 1    | No         | No          |
| WP2.1 | DEFINITION OF FUNCTIONAL REQUIREMENTS         | 1 week         | WP1.1             | Start of week 2      | End of week 2    | Yes         | Yes       |
| WP2.2 | DEFINITION OF TECHNICAL REQUIREMENTS        | 1 week         | WP2.1             | Start of week 2      | End of week 2    | Yes         | No          |
| WP3.1 | DEFINITION OF ARCHITECTURE        | 3 week         | WP2.2             | Start of week 3      | End of week 5    | Yes         | Yes         |
| WP3.2 | DATABASE DESIGN        | 3 week         | WP2.2, WP2.1              | Start of week 3      | End of week 5    | No         | No         |
| WP3.2 | WEB AND MOBILE DESIGN        | 3 week         | WP2.2, WP2.1              | Start of week 3      | End of week 5    | No         | No         |

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


