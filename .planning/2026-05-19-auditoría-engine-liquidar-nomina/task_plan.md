# Task Plan: Auditoría - engine.liquidar_nomina

## Goal
Ensure `liquidar_nomina` is correct for financial use: numeric safety (no float-induced error), robust input validation, and full pytest coverage for edge cases.

## Current Phase
Phase 1

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
- [x] Identify constraints
- [x] Document in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [ ] Define approach for migration to Decimal (or integer cents)
- [ ] Create test matrix and pytest structure
- [ ] Define rounding policy (Decimal context or bankers/ROUND_HALF_UP)
- **Status:** in_progress

### Phase 3: Implementation
- [ ] Implement input validation for `vlr_hora`, `salario_base` types, and NaN/Infinity checks
- [ ] Replace float arithmetic with Decimal (or use integer-cents) within `liquidar_nomina` — spike first
- [ ] Add explicit unit conversion (pesos -> Decimal('0.01') or cents)
- [ ] Add pytest unit tests per test matrix
- **Status:** pending

### Phase 4: Testing & Verification
- [ ] Run pytest and confirm deterministic results across Python versions (3.11+)
- [ ] Add BDD-style test matrix to findings.md
- [ ] Verify edge cases: zero hours, large numbers, NaN/Infinity, minimal SMMLV boundary, transport aid threshold
- **Status:** pending

### Phase 5: Delivery
- [ ] Review outputs and present diffs (float vs Decimal) with sample cases
- [ ] Deliver testing artifacts and recommended migration patch
- **Status:** pending

## Tasks (Actionable)
1. Create pytest skeleton: tests/test_engine.py. (Owner: TBD, Est: 1h)
2. Write BDD test matrix in findings.md (see matrix section). (Owner: TBD, Est: 1h)
3. Spike: implement Decimal-based version in a non-committed file to compare outputs against current function for a variety of cases. (Owner: TBD, Est: 2h)
4. Implement input validations and type checks in `liquidar_nomina`. (Owner: TBD, Est: 1h)
5. Replace floats with Decimal in `engine.py` (small, local change) and run test suite. (Owner: TBD, Est: 2h)
6. Performance/sanity check: verify no unacceptable perf regressions for typical payroll batch sizes. (Owner: TBD, Est: 1h)

## Risks & Mitigations
- Risk: Changing numeric representation may alter output slightly due to rounding policy.
  - Mitigation: Define rounding policy in Phase 2 and run comparative matrix.
- Risk: Tests don't cover all real-world edge cases.
  - Mitigation: Add BDD matrix and a smoke test with representative payroll lines.


## Decisions Made
| Decision | Rationale |
|----------|-----------|

## Errors Encountered
| Error | Resolution |
|-------|------------|
