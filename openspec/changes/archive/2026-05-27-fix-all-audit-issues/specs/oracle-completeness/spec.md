## ADDED Requirements

### Requirement: Each oracle scenario SHALL include vlr_hora explicitly
Every test scenario in `casos_prueba.md` SHALL specify a `vlr_hora` value so that the Guardian Agent can generate tests with deterministic expected results. No scenario shall omit this parameter.

#### Scenario: CP-01 includes vlr_hora
- **WHEN** reading scenario CP-01 (recargo diurno)
- **THEN** `vlr_hora` is explicitly defined as a numeric value

#### Scenario: CP-10 includes vlr_hora
- **WHEN** reading scenario CP-10 (cálculo completo)
- **THEN** `vlr_hora` is explicitly defined as a numeric value

### Requirement: Oracle scenarios SHALL use strict Gherkin format
All scenarios in `casos_prueba.md` SHALL follow the Gherkin format with `Given`/`When`/`Then` keywords. The flat "Datos de entrada" / "Resultado esperado" format SHALL be removed or converted to Gherkin. Mixed formats are not allowed.

#### Scenario: All scenarios use Given/When/Then
- **WHEN** parsing `casos_prueba.md`
- **THEN** every scenario contains `Given`, `When`, and `Then` lines

#### Scenario: No flat format remains
- **WHEN** scanning `casos_prueba.md` for "Datos de entrada" sections
- **THEN** none are found outside of Gherkin-converted content

### Requirement: Oracle SHALL cover all business rules R1-R5
The oracle SHALL include at least one scenario per business rule (R1 through R5), plus at least two boundary cases (salario = SMMLV, tope exacto, horas = 0).

#### Scenario: R1 coverage
- **WHEN** counting scenarios for R1 (recargo diurno)
- **THEN** at least one scenario tests R1 with explicit vlr_hora

#### Scenario: R4 boundary coverage
- **WHEN** counting scenarios for R4 (auxilio de transporte)
- **THEN** at least three scenarios exist: applies, exact boundary, does not apply
