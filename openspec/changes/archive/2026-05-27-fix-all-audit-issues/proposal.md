## Why

El proyecto QualityGuardian-NominaPro tiene una auditoría de cumplimiento contra AGENTS.md que revela 8 hallazgos (3 críticos, 5 medios) que impiden alcanzar el 10/10 en todas las dimensiones. Los bugs actuales causan falsos positivos en pruebas, fuga potencial de secrets en Docker, y un veredicto JSON que no cumple su propio schema. Sin corregirlos, el pipeline no es auditable ni reproducible — el objetivo central del proyecto COIL UdeCaldas × UMB.

## What Changes

- **Corregir bug en test_R4_No_Aplica**: El test usa `salario_base=1_500_000` pero su nombre dice "Salario sobre el tope". Se corrige a `salario_base=3_000_000` con `auxilio_transporte == 0.0`.
- **Agregar validaciones de entrada en engine.py**: Validar `vlr_hora <= 0`, `NaN`, `Infinity` con `ValueError` descriptivo.
- **Completar oráculo con `vlr_hora` explícito**: Cada escenario CP-01 a CP-10 incluye `vlr_hora` para eliminar valores arbitrarios en tests generados.
- **Estandarizar formato Gherkin en casos_prueba.md**: Unificar a formato Gherkin estricto (Given/When/Then) sin mezcla de formatos planos.
- **Eliminar fuga de secrets en Dockerfile**: Quitar `COPY .env .env`, usar variables de entorno en runtime, permisos de solo lectura.
- **Refactorizar CI/CD para ejecutar tests dentro de Docker**: La CI debe buildear la imagen y correr `docker run` en lugar de instalar dependencias directo en el runner.
- **Corregir veredicto.json para cumplir schema**: `cobertura` en formato "XX.X%", `duracion_ms` con valores reales medidos.
- **Establecer workflow .planning/ para DRAFTs**: Todos los artifacts generados por agentes pasan primero por `.planning/` antes de producción.
- **Documentar pipeline completo en README.md**: Roles, agentes, cómo ejecutar local, cómo se genera el veredicto.

## Capabilities

### New Capabilities
- `engine-validation`: Validaciones completas de entrada en engine.py (vlr_hora, NaN, Infinity)
- `oracle-completeness`: Oráculo con vlr_hora explícito y formato Gherkin estricto
- `docker-security`: Dockerfile seguro sin secrets embebidos, permisos de solo lectura
- `ci-docker-execution`: CI/CD que ejecuta tests dentro de contenedor Docker aislado
- `veredicto-schema-compliance`: Veredicto JSON que cumple el schema de AGENTS.md (cobertura, duración)
- `planning-workflow`: Workflow de DRAFTs en .planning/ antes de producción
- `project-documentation`: README.md con documentación completa del pipeline

### Modified Capabilities
- `agents-ecosystem`: Modificar requisito de Tool Access Policies para exigir paso por .planning/ (ya definido en AGENTS.md pero no implementado)

## Impact

**Archivos afectados:**
- `src/engine.py` — nuevas validaciones R5 extendidas
- `tests/test_engine.py` — corrección de test_R4_No_Aplica, nuevos tests para vlr_hora
- `casos_prueba.md` — reescritura con vlr_hora y Gherkin estricto
- `infra/Dockerfile` — eliminar COPY .env, ajustar permisos
- `.github/workflows/ci.yml` — refactor completo para usar Docker
- `src/guardian_client.py` — medir duración real, calcular cobertura
- `README.md` — documentación completa
- `src/__init__.py` — posiblemente necesario para imports

**Dependencias:** Sin nuevas dependencias externas. Se usa `pytest-cov` si se instala en requirements.txt para cobertura real.

**Riesgos:** El cambio al CI puede requerir ajustes en el Dockerfile para que los tests se ejecuten correctamente en el entorno de GitHub Actions.
