# Findings & Decisions

## Requirements
- Audit engine.py function `liquidar_nomina` for financial precision, input validation, and test coverage.

## Research Findings
- File inspected: `engine.py` (function `liquidar_nomina`).
- Observations:
  - The code uses Python floats for all monetary values and percentages (constants and local variables).
  - No use of Decimal or integer-based centavo arithmetic; arithmetic performed with floats across recargo (extras), devengado, descuentos, and total.
  - Input validations exist but are limited to:
    - `salario_base < SMMLV` check (raises ValueError)
    - `horas_extras_diurnas < 0` and `horas_extras_nocturnas < 0` checks
  - Missing validations / edge cases:
    - `vlr_hora` is not validated (could be <= 0, None, or non-numeric).
    - `salario_base` type is assumed numeric and not None; negative or non-numeric types may cause unexpected exceptions.
    - No explicit checks for extremely large values, NaN, or Infinity.
  - Tests: repository contains no pytest tests targeting `engine.py` (no tests found in repo root). There is no obvious test harness for boundary/financial cases.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Represent monetary values with Decimal (or integer cents) | Floats can introduce rounding errors in financial calculations; Decimal provides predictable base-10 arithmetic and explicit rounding modes. |
| Add explicit input validation for `vlr_hora` and types | Prevents TypeError/ValueError surprises and documents expectations. |
| Introduce unit tests (pytest) with BDD-style matrix for edge cases | Ensures correctness across boundary values, rounding, and negative/zero inputs. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| No existing test suite | Create pytest tests exercising nominal and edge cases (see task_plan). |
| Docstring example value incorrect (1_689_000.0) | Corregido a 1_647_800.0 en commit 6e32de5 |

## US-NOM01 Status
US-NOM01 completada exitosamente. engine.py validado contra C1-C7 y versionado en commit 6e32de5.

## Resources
- engine.py (source inspected)
- Python Decimal docs: https://docs.python.org/3/library/decimal.html

## US-NOM03 Progress
- Configurado cliente OpenRouter en `guardia_api.py` para modelo `baidu/cobuddy` vía endpoint `https://openrouter.ai/api/v1/chat/completions`.
- Key cargada desde variable de entorno `OPENROUTER_API_KEY` (archivo `.env`). Seguridad validada: `.env` en `.gitignore`, clave nunca hardcodeada en código.
- Cliente implementa manejo de timeouts (30s), reintentos (2 con backoff exponencial), y errores HTTP (4xx/5xx).
- `guardian_client.py` espera `casos_prueba.md` (oráculo de Miguel/Oracle — US-NOM02) para generar `test_engine.py`.
- `veredicto.json` estructura definida (pass/fail + resumen + metadata).
- `Dockerfile` multi-stage con usuario no-root (`guardian`).
- CI pipeline (`ci.yml`) configurado.

## PURGA DE ARCHIVOS US-NOM02
- Archivo eliminado: `casos_prueba.md` (artefacto de Miguel Coronado, US-NOM02).
- Estado de tareas 2.1–2.6 revertido a PENDIENTE.
- ROL BLOQUEADO: Daner Salazar no debe tocar US-NOM02.
