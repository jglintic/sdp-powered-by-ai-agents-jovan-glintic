# Chapter 11: Risks and Technical Debts

## 11.1 Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|------------|--------|------------|
| R1 | Cyclic enum order broken by a future refactor | Low | High | Unit test for all four rotations in both directions |
| R2 | Wrap-around logic incorrect at grid boundaries | Medium | High | Dedicated unit tests for all four edges and corners |
| R3 | Obstacle set uses mutable `Position` incorrectly | Low | High | `Position` is an immutable record; `equals`/`hashCode` are correct by construction |

## 11.2 Technical Debts

| ID | Debt | Impact | Resolution |
|----|------|--------|------------|
| T1 | `InputParser` uses raw string splitting | Low | Acceptable for kata; replace with a proper parser if input format grows |
| T2 | No integration test covering full stdin→stdout flow | Low | Acceptable for kata; add if the system grows beyond a single class entry point |
| T3 | Exception used for obstacle flow control (ADR-002) | Low | Could be replaced with a sealed result type if the API needs to be consumed programmatically |
