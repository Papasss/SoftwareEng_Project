# Product Breakdown Structure (PBS)

| ID | Deliverable | Type  | Notes |
|:---|:------------|:--------------------------------------------------|:------|
| X# |             |                                                  |       |


---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID   | Work package               | Traced PBS outputs (IDs)                    |
|:-----|:---------------------------|:--------------------------------------------|
| WP1  | PROJECT MANAGEMENT         | D1                                          |
| WP2  | REQUIREMENTS               | D1                                          |
| WP3  | DESIGN AND ARCHITECTURES   | S5, S8, S10, S13, S15, I1, I2, D2           |
| WP4  | IMPLEMENTATION             | S1-20, I3-6                                 |
| WP5  | TESTING                    | D4                                          |
| WP6  | DEPLOYMENT                 | D3, D5                                      |
| WP7  | MAINTENANCE                | S1-20, I5                                   |


**Description** <br>
The division into project phases followed the iterative software development model, which places great emphasis on avoiding a monolithic, one-way process. For this reason, it was decided to include the ‘Maintenance’ phase as a fundamental element for the future of the project. Furthermore, importance was attached to the project’s design phases, understood as business decisions, by initially including the ‘Project Management’ phase, which is useful as the client is no longer merely a client but is involved in the process steps, engaging in constant dialogue with the project manager.

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


