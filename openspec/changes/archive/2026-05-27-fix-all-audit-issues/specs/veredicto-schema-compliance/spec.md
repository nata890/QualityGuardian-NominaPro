## ADDED Requirements

### Requirement: veredicto.json cobertura SHALL match schema format
The `resumen.cobertura` field in `veredicto.json` SHALL be a string matching the pattern `^\d{2}\.\d%$` (e.g., "75.0%", "0.0%", "100.0%"). The value "N/A" SHALL NOT be used.

#### Scenario: Coverage is formatted correctly
- **WHEN** veredicto.json is generated after test execution
- **THEN** `resumen.cobertura` matches the regex `^\d{2}\.\d%$`

#### Scenario: Coverage is calculated from pytest-cov
- **WHEN** pytest runs with `--cov=src.engine`
- **THEN** the coverage percentage is extracted and formatted as "XX.X%"

### Requirement: veredicto.json duracion_ms SHALL reflect actual test duration
Each scenario's `duracion_ms` field SHALL contain the actual execution time in milliseconds, parsed from the JUnit XML `time` attribute. The value SHALL NOT be hardcoded to 0.

#### Scenario: Duration is measured from JUnit
- **WHEN** veredicto.json is generated
- **THEN** each `escenarios[i].duracion_ms` equals `junit_time * 1000` rounded to integer

#### Scenario: Duration is positive for non-trivial tests
- **WHEN** a test takes measurable time (>0.001s)
- **THEN** `duracion_ms` is > 0

### Requirement: veredicto.json SHALL pass JSON Schema validation
The complete `veredicto.json` SHALL validate against the JSON Schema defined in AGENTS.md section 4, including all required fields, types, and format constraints.

#### Scenario: Full schema validation passes
- **WHEN** veredicto.json is validated against the AGENTS.md schema
- **THEN** all fields pass type checks, enum constraints, and pattern matches
