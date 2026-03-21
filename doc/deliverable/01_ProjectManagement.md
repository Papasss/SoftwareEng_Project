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
| ID    | Activity                              | Duration   | Dependencies   | Start           | End               | Critical | Milestone |
|:------|:--------------------------------------|:-----------|:---------------|:----------------|:------------------|:---------|:----------|
| WP1.1 | DEFINITION OF BUSINESS REQUIREMENTS   | 1 week     | No dependecies | Start of week 1 | End of week 1     | Yes      | Yes       |
| WP1.2 | DEFINITION OF TIME AND RESOURCE       | 1 week     | WP1.1          | Start of week 1 | End of week 1     | No       | No        |
| WP1.3 | PLANNING                              | 1 week     | WP1.2          | Start of week 1 | End of week 1     | No       | Yes       |
| WP2.1 | DEFINITION OF FUNCTIONAL REQUIREMENTS | 1 week     | WP1.1          | Start of week 2 | End of week 2     | Yes      | No        |
| WP2.2 | DEFINITION OF TECHNICAL REQUIREMENTS  | 1 week     | WP2.1          | Start of week 2 | End of week 2     | Yes      | Yes       |
| WP3.1 | DEFINITION OF ARCHITECTURE            | 3 weeks    | WP2.2          | Start of week 3 | End of week 5     | Yes      | No        |
| WP3.2 | DATABASE DESIGN                       | 3 weeks    | WP2.2          | Start of week 3 | End of week 5     | No       | No        | 
| WP3.3 | WEB AND MOBILE DESIGN                 | 3 weeks    | WP2.2          | Start of week 3 | End of week 5     | No       | Yes       |
| WP4.1 | IMPLEMENTATION OF BACK-END            | 20 weeks   | WP3.1, WP3.2   | Start of week 6 | End of week 25    | Yes      | No        |
| WP4.2 | IMPLEMENTATION OF FRONT-END           | 23 weeks   | WP3.3          | Start of week 6 | End of week 28    | Yes      | No        |
| WP4.3 | STATISTICS REPORTS                    | 21 weeks   | WP4.1, WP4.2   | Start of week 8 | End of week 28    | No       | Yes       |
| WP5.1 | UNIT TESTING                          | 2 weeks    | WP4.3          | Start of week 28 | End of week 29   | Yes      | No        |
| WP5.2 | INTEGRATION TESTING                   | 2 weeks    | WP5.1          | Start of week 30 | End of week 31   | Yes      | No        |
| WP5.3 | SYSTEM TESTING                        | 2 weeks    | WP5.2          | Start of week 32 | End of week 33   | Yes      | No        |
| WP5.4 | UAT                                   | 2 weeks    | WP5.3          | Start of week 34 | End of week 35   | Yes      | Yes       |
| WP6.1 | PLANNING SESSION WITH USER            | 1 week     | WP5.4          | Start of week 36 | End of week 36   | No       | No        |
| WP6.2 | TICKETING AND GO LIVE                 | 1 week     | WP5.4          | Start of week 37 | End of week 37   | Yes      | No        |
| WP6.3 | DEPLOY IN PROD ENVIRONMENT            | 1 week     | WP6.2          | Start of week 38 | End of week 38   | Yes      | Yes       |
| WP7.1 | ADJUSTMENTS OR BUG FIXES              | 2 weeks    | WP6.3          | Start of week 39 | End of week 40   | No       | No        | 

## Critical path
`WP1.1 → WP2.1 → WP2.2 → WP3.1 → WP4.1 → WP4.2 → WP5.1 → WP5.2 → WP5.3 → WP5.4 → WP6.2 → WP6.3`


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


