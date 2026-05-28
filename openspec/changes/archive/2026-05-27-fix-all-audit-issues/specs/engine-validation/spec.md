## ADDED Requirements

### Requirement: engine.py SHALL validate vlr_hora is positive
The `liquidar_nomina` function SHALL reject `vlr_hora` values that are less than or equal to zero, raising a `ValueError` with a descriptive message indicating the invalid value.

#### Scenario: vlr_hora is zero
- **WHEN** `liquidar_nomina` is called with `vlr_hora=0`
- **THEN** a `ValueError` is raised with a message indicating that the hour value must be positive

#### Scenario: vlr_hora is negative
- **WHEN** `liquidar_nomina` is called with `vlr_hora=-5000`
- **THEN** a `ValueError` is raised with a message indicating that the hour value must be positive

### Requirement: engine.py SHALL reject NaN and Infinity for vlr_hora
The `liquidar_nomina` function SHALL detect `NaN` and `Infinity` values for `vlr_hora` using `math.isnan()` and `math.isinf()`, raising a `ValueError` with a descriptive message.

#### Scenario: vlr_hora is NaN
- **WHEN** `liquidar_nomina` is called with `vlr_hora=float('nan')`
- **THEN** a `ValueError` is raised with a message indicating that the hour value cannot be NaN

#### Scenario: vlr_hora is positive infinity
- **WHEN** `liquidar_nomina` is called with `vlr_hora=float('inf')`
- **THEN** a `ValueError` is raised with a message indicating that the hour value cannot be infinite

#### Scenario: vlr_hora is negative infinity
- **WHEN** `liquidar_nomina` is called with `vlr_hora=float('-inf')`
- **THEN** a `ValueError` is raised with a message indicating that the hour value cannot be infinite

### Requirement: engine.py SHALL preserve all existing R1-R5 validations
All existing validations (salario_base < SMMLV, horas_extras_diurnas < 0, horas_extras_nocturnas < 0) SHALL remain unchanged and functional.

#### Scenario: existing validations still work
- **WHEN** `liquidar_nomina` is called with `salario_base=500000` (below SMMLV)
- **THEN** a `ValueError` is raised with the existing SMMLV message
