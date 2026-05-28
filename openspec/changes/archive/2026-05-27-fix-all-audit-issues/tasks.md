## 1. Engine Validations (R5 Extended)

- [x] 1.1 Add `import math` to `src/engine.py`
- [x] 1.2 Add validation for `vlr_hora <= 0` raising `ValueError` with descriptive message
- [x] 1.3 Add validation for `math.isnan(vlr_hora)` raising `ValueError`
- [x] 1.4 Add validation for `math.isinf(vlr_hora)` raising `ValueError`
- [x] 1.5 Update docstring in `liquidar_nomina` to document new exceptions
- [x] 1.6 Verify existing R1-R5 logic unchanged (manual review)

## 2. Oracle Completeness (casos_prueba.md)

- [x] 2.1 Add `vlr_hora` to each scenario CP-01 through CP-10 with explicit numeric values
- [x] 2.2 Convert all scenarios to strict Gherkin format (Given/When/Then), removing flat "Datos de entrada" sections
- [x] 2.3 Verify at least 10 scenarios cover all R1-R5 rules
- [x] 2.4 Verify boundary cases: salario = SMMLV, tope exacto, horas = 0

## 3. Test Corrections (test_engine.py)

- [x] 3.1 Fix `test_R4_No_Aplica`: change `salario_base=1_500_000` to `3_000_000` and assert `auxilio_transporte == 0.0`
- [x] 3.2 Update fallback in `guardian_client.py` line 222-224 to match corrected test (verify it already has correct values)
- [x] 3.3 Add `test_R5_VlrHora_Cero`: assert `ValueError` for `vlr_hora=0`
- [x] 3.4 Add `test_R5_VlrHora_Negativa`: assert `ValueError` for `vlr_hora=-5000`
- [x] 3.5 Add `test_R5_VlrHora_NaN`: assert `ValueError` for `vlr_hora=float('nan')`
- [x] 3.6 Add `test_R5_VlrHora_Infinito`: assert `ValueError` for `vlr_hora=float('inf')`
- [x] 3.7 Run `pytest tests/test_engine.py -v --tb=short` and verify all tests pass (expect 15+)

## 4. Docker Security

- [x] 4.1 Remove `COPY .env .env` from `infra/Dockerfile` line 25
- [x] 4.2 Change `chmod 770 /app` to `chmod 550 /app` (read-only, no write)
- [x] 4.3 Add `pytest-cov>=7.0.0` to `infra/requirements.txt`
- [x] 4.4 Verify Dockerfile builds successfully: `docker build -f infra/Dockerfile -t guardian .`
- [x] 4.5 Verify container runs with read-only: `docker run --read-only guardian python -c "print('ok')"`

## 5. CI/CD Docker Execution

- [x] 5.1 Rewrite `.github/workflows/ci.yml` to build Docker image instead of installing deps directly
- [x] 5.2 Replace `python -m pytest` step with `docker run --read-only guardian python -m pytest tests/test_engine.py`
- [x] 5.3 Add step to extract `veredicto.json` and `reporte_junit.xml` from container via `docker cp`
- [x] 5.4 Keep `OPENROUTER_API_KEY` passed via `docker run -e`
- [x] 5.5 Verify workflow YAML syntax is valid

## 6. Veredicto Schema Compliance

- [x] 6.1 Update `generar_veredicto()` in `guardian_client.py` to parse JUnit XML for real `duracion_ms` values
- [x] 6.2 Add coverage calculation: run pytest with `--cov=src.engine` and parse output for percentage
- [x] 6.3 Format `cobertura` as "XX.X%" string (never "N/A")
- [x] 6.4 Validate generated `veredicto.json` against AGENTS.md JSON Schema (manual check)

## 7. Planning Workflow

- [x] 7.1 Create `.planning/fix-all-audit-issues/` directory
- [x] 7.2 Update `guardian_client.py` OUTPUT_PATH to write to `.planning/fix-all-audit-issues/test_engine.py`
- [x] 7.3 Update `guardian_client.py` veredicto output to `.planning/fix-all-audit-issues/veredicto.json`
- [x] 7.4 Add copy-to-production step (manual or script) after human approval
- [x] 7.5 Verify `.planning/` is NOT in `.gitignore`

## 8. Documentation (README.md)

- [x] 8.1 Write pipeline overview section (Lead Dev → Oracle → Guardian → DevOps)
- [x] 8.2 Write agent roles and responsibilities section
- [x] 8.3 Write local execution instructions (install deps, run Guardian, Docker tests)
- [x] 8.4 Write .planning/ DRAFT workflow explanation
- [x] 8.5 Write project structure tree with file descriptions
- [x] 8.6 Write environment setup (.env for local, GitHub Secrets for CI)
- [x] 8.7 Review README for completeness and accuracy
