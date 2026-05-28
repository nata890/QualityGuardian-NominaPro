## Context

El proyecto QualityGuardian-NominaPro implementa un pipeline de auditoría de nómina colombiana basado en agentes de IA (Lead Dev → Oracle → Guardian → DevOps). El pipeline funciona parcialmente pero tiene 8 hallazgos de auditoría que impiden el cumplimiento total del contrato definido en AGENTS.md.

Estado actual:
- `engine.py` implementa R1-R5 correctamente pero sin validaciones de `vlr_hora`
- `casos_prueba.md` tiene 10 escenarios pero sin `vlr_hora` explícito y con formato Gherkin inconsistente
- `test_engine.py` tiene un bug crítico en `test_R4_No_Aplica`
- `Dockerfile` copia `.env` al contenedor (fuga de secrets)
- `ci.yml` ejecuta tests fuera de Docker
- `veredicto.json` no cumple su propio schema (cobertura="N/A", duracion_ms=0)
- No existe flujo de `.planning/` para DRAFTs
- `README.md` tiene 2 líneas

## Goals / Non-Goals

**Goals:**
- Corregir todos los hallazgos de auditoría (críticos y medios)
- Alcanzar 10/10 en cada dimensión del checklist de AGENTS.md
- Mantener compatibilidad con el pipeline existente (no romper lo que funciona)
- Hacer el pipeline reproducible y auditable

**Non-Goals:**
- No se rediseña la arquitectura de agentes
- No se cambia el modelo LLM (baidu/cobuddy:free)
- No se modifica la lógica de negocio R1-R5 existente (solo se agregan validaciones)
- No se implementan nuevas reglas de negocio

## Decisions

### Decisión 1: Validaciones de vlr_hora en engine.py — ValueError descriptivo

**Opción elegida**: Agregar validaciones R5 extendidas para `vlr_hora <= 0`, `math.isnan()`, `math.isinf()`. Cada una lanza `ValueError` con mensaje descriptivo.

**Alternativas descartadas:**
- ~~Silenciar valores inválidos~~: Rompe la auditabilidad.
- ~~Usar assert en vez de ValueError~~: Los asserts se desactivan con `-O`.
- ~~Validar tipos (isinstance)~~: El tipado de Python ya lo cubre; agregarlo sería redundante y no es exigido por AGENTS.md.

### Decisión 2: Corrección de test_R4_No_Aplica — fallback como fuente de verdad

**Opción elegida**: Corregir directamente `test_engine.py` y también el fallback en `guardian_client.py:222-224` (que ya tiene la lógica correcta). El fallback será la fuente de verdad para asegurar consistencia si se regeneran los tests.

### Decisión 3: vlr_hora en oráculo — valor fijo por escenario

**Opción elegida**: Agregar `vlr_hora` explícito a cada escenario CP-01 a CP-10 con valores razonables (10_000–15_000). Esto elimina la ambigüedad y permite verificación numérica exacta.

### Decisión 4: Dockerfile seguro — eliminar COPY .env, usar runtime env

**Opción elegida**: Eliminar `COPY .env .env`. La API key se pasa en runtime con `docker run -e OPENROUTER_API_KEY`. Los permisos se ajustan a `chmod 550` (lectura+ejecución, sin escritura).

**Alternativas descartadas:**
- ~~BuildKit secrets~~: Overkill para este proyecto académico.
- ~~Multi-stage con secret mount~~: Complejidad innecesaria.

### Decisión 5: CI con Docker — build + run en GitHub Actions

**Opción elegida**: El CI buildea la imagen Docker y ejecuta los tests con `docker run --read-only`. El veredicto.json se extrae del contenedor con `docker cp`.

**Alternativas descartadas:**
- ~~Seguir ejecutando fuera de Docker~~: Viola AGENTS.md.
- ~~Usar Docker Compose~~: Overkill para un solo contenedor.

### Decisión 6: Cobertura real — pytest-cov

**Opción elegida**: Agregar `pytest-cov` a `requirements.txt` y ejecutar con `--cov=src.engine`. El resultado se parsea para generar `cobertura: "XX.X%"` en el veredicto.

### Decisión 7: Duración real — capturar tiempo de pytest

**Opción elegida**: Parsear el campo `time` del JUnit XML (ya disponible en `reporte_junit.xml`) para llenar `duracion_ms` con valores reales. El CI ya lo hace correctamente; el script local (`guardian_client.py`) debe actualizarse para hacer lo mismo.

### Decisión 8: Workflow .planning/ — DRAFTs antes de producción

**Opción elegida**: Los artifacts generados por el Guardian Agent (test_engine.py, veredicto.json) se escriben primero en `.planning/fix-all-audit-issues/`. Después de aprobación humana, se copian a sus paths de producción. Esto se documenta en README.md.

## Risks / Trade-offs

- **[Riesgo] CI con Docker puede ser más lento** → El build de la imagen agrega ~30s al CI. Mitigación: caché de capas con `actions/cache` o `docker/build-push-action`.
- **[Riesgo] pytest-cov no disponible en imagen Docker** → Se agrega a `requirements.txt` y se instala en el stage builder.
- **[Trade-off] vlr_hora fijo vs. calculado** → Fijar vlr_hora en el oráculo reduce flexibilidad pero elimina ambigüedad. Preferimos determinismo.
- **[Riesgo] El modelo free de OpenRouter puede fallar** → El fallback por plantilla ya existe y es robusto. Este cambio lo mejora, no lo reemplaza.
