# QualityGuardian-NominaPro

Proyecto de IA Agéntica para la auditoría de un motor de cálculo de nómina colombiana. Colaboración COIL (Universidad de Caldas × Universidad Manuela Beltrán).

---

## Pipeline de Agentes

El proyecto implementa un pipeline secuencial de agentes de IA que auditan un motor de liquidación de nómina siguiendo reglas laborales colombianas:

```
Lead Dev (Natalia) ── engine.py ──→ Oracle (Miguel) ── casos_prueba.md ──→
    Guardian (Daner) ── test_engine.py ── Docker ──→ veredicto.json
        ↑ DevOps (Daner): Dockerfile + GitHub Actions CI
        ↑ Orchestrator (Miguel): coordina, revisa, consolida
```

### Flujo de datos

1. **Lead Dev Agent** implementa `liquidar_nomina()` en `src/engine.py` con las reglas R1–R5
2. **Oracle Agent** crea `casos_prueba.md` con escenarios Gherkin que cubren todas las reglas
3. **Guardian Agent** lee el oráculo, genera `test_engine.py` con Pytest, ejecuta dentro de Docker aislado y emite `veredicto.json`
4. **DevOps Agent** mantiene el Dockerfile multi-stage y la CI de GitHub Actions
5. **Orchestrator** coordina el pipeline y gestiona revisiones por la célula compañera

---

## Agentes y Responsabilidades

| Agente | Responsable | HU | Entregable |
|---|---|---|---|
| **Lead Dev** | Natalia Ceballos (UdeC) | US-NOM01 | `engine.py` con reglas R1–R5, tipado, docstring |
| **Oracle** | Miguel Coronado (UMB) | US-NOM02 | `casos_prueba.md` con ≥10 escenarios Gherkin |
| **Guardian** | Daner Salazar (UdeC) | US-NOM03 | `test_engine.py`, `veredicto.json`, LangChain + OpenRouter |
| **DevOps** | Daner Salazar (UdeC) | US-NOM03 | Dockerfile multi-stage, GitHub Actions CI |
| **Orchestrator** | Miguel Coronado (UMB) | Transversal | Coordinación, revisión célula compañera |

---

## Reglas de Negocio

| Regla | Descripción |
|---|---|
| **R1** | Recargo 25% sobre hora ordinaria para horas extras diurnas |
| **R2** | Recargo 75% sobre hora ordinaria para horas extras nocturnas |
| **R3** | Descuentos 4% salud + 4% pensión sobre total devengado |
| **R4** | Auxilio de transporte $162.000 si salario_base ≤ $2.600.000 |
| **R5** | Validaciones: salario < SMMLV → ValueError, horas negativas → ValueError, vlr_hora ≤ 0/NaN/Infinito → ValueError |

---

## Estructura del Proyecto

```
QualityGuardian-NominaPro/
├── AGENTS.md                  # Contrato de gobierno del repositorio
├── README.md                  # Este archivo
├── casos_prueba.md            # Oráculo de pruebas (Oracle Agent)
├── veredicto.json             # Veredicto del Guardian Agent
├── reporte_junit.xml          # Reporte JUnit de pytest
├── src/
│   ├── __init__.py
│   ├── engine.py              # Motor de cálculo de nómina (R1-R5)
│   ├── guardia_api.py         # Cliente OpenRouter con retry/backoff
│   └── guardian_client.py     # Orquestador: lee oráculo → genera tests → veredicto
├── tests/
│   └── test_engine.py         # Pruebas Pytest (generadas o manuales)
├── infra/
│   ├── Dockerfile             # Multi-stage, non-root, sin secrets
│   └── requirements.txt       # Dependencias Python
├── scripts/
│   ├── validar_conexion.py    # Verifica conectividad OpenRouter
│   ├── validar_pipeline.sh    # Script de validación local
│   └── copy_to_production.sh  # Mueve DRAFTs de .planning/ a producción
├── .planning/                 # DRAFTs antes de aprobación humana
│   └── fix-all-audit-issues/
│       ├── test_engine.py
│       ├── veredicto.json
│       └── reporte_junit.xml
├── artifacts/                 # Output crudo de la LLM para auditoría
├── .github/workflows/
│   └── ci.yml                 # CI: build Docker → run tests → upload artifacts
└── openspec/                  # Especificaciones OpenSpec
```

---

## Ejecución Local

### Prerrequisitos

- Python 3.11+
- Docker
- Variable de entorno `OPENROUTER_API_KEY` configurada

### 1. Instalar dependencias

```bash
pip install -r infra/requirements.txt
```

### 2. Configurar API Key

Crear archivo `.env` en la raíz del proyecto:

```
OPENROUTER_API_KEY=sk-or-v1-tu-clave-aqui
```

O exportar directamente:

```bash
export OPENROUTER_API_KEY="sk-or-v1-tu-clave-aqui"
```

### 3. Ejecutar el Guardian Agent (genera tests + veredicto)

```bash
python src/guardian_client.py
```

Esto:
1. Lee `casos_prueba.md`
2. Genera `test_engine.py` en `.planning/fix-all-audit-issues/`
3. Ejecuta los tests con pytest
4. Emite `veredicto.json` en `.planning/fix-all-audit-issues/`

### 4. Ejecutar tests directamente

```bash
python -m pytest tests/test_engine.py -v --tb=short --cov=src.engine
```

### 5. Ejecutar dentro de Docker

```bash
# Construir imagen
docker build -f infra/Dockerfile -t guardian .

# Ejecutar tests en contenedor aislado
docker run --name guardian-test --read-only --tmpfs /tmp \
  -e OPENROUTER_API_KEY \
  guardian \
  python -m pytest tests/test_engine.py -v --tb=short --junitxml=/tmp/reporte_junit.xml --cov=src.engine

# Extraer resultados
docker cp guardian-test:/tmp/reporte_junit.xml reporte_junit.xml
docker rm guardian-test
```

### 6. Mover DRAFTs a producción

Después de revisión humana:

```bash
bash scripts/copy_to_production.sh
```

---

## Workflow .planning/ (DRAFT → Producción)

Según las Tool Access Policies de AGENTS.md (sección 3):

1. Todo artifact generado por un agente se escribe primero en `.planning/<change-name>/` como **DRAFT**
2. El humano responsable revisa el DRAFT
3. Después de aprobación, se ejecuta `scripts/copy_to_production.sh` para copiar a los paths de producción
4. Los archivos en `.planning/` están versionados en git (NO están en `.gitignore`)

```
.planning/fix-all-audit-issues/
├── test_engine.py      ← DRAFT (revisar antes de copiar a tests/)
├── veredicto.json      ← DRAFT (revisar antes de copiar a raíz)
└── reporte_junit.xml   ← DRAFT (revisar antes de copiar a raíz)
```

---

## CI/CD (GitHub Actions)

El pipeline de CI se ejecuta en cada push a `main` o `develop`, y en pull requests a `main`:

1. **Checkout** del repositorio
2. **Build Docker** desde `infra/Dockerfile`
3. **Validar conectividad** OpenRouter (dentro del contenedor)
4. **Generar tests** con Guardian Agent (dentro del contenedor)
5. **Ejecutar tests** con `docker run --read-only` (aislamiento total)
6. **Extraer resultados** con `docker cp`
7. **Generar veredicto.json** desde JUnit XML con duraciones reales
8. **Upload artifacts**: `veredicto.json` y `reporte_junit.xml`

La API key se pasa como GitHub Secret (`OPENROUTER_API_KEY`) y se inyecta al contenedor con `-e`.

---

## Protocolo de Veredicto

El archivo `veredicto.json` sigue el schema definido en AGENTS.md sección 4:

```json
{
  "escenarios": [
    {
      "id": "test_R1_Nominal",
      "descripcion": "Test test_R1_Nominal",
      "resultado": "PASS",
      "duracion_ms": 3
    }
  ],
  "resumen": {
    "total": 15,
    "pasaron": 15,
    "fallaron": 0,
    "cobertura": "95.2%"
  },
  "metadata": {
    "modelo": "baidu/cobuddy:free",
    "timestamp": "2026-05-27T00:00:00Z",
    "oraculo": "casos_prueba.md",
    "duracion_total_ms": 45
  }
}
```

---

## Seguridad

- **OPENROUTER_API_KEY**: Nunca en texto plano en el repositorio. Se carga desde `.env` (local) o GitHub Secrets (CI).
- **Dockerfile**: No copia `.env` al contenedor. La API key se pasa en runtime con `docker run -e`.
- **Contenedor**: Se ejecuta como usuario non-root (`guardian`) con permisos de solo lectura (`chmod 550`).
- **.gitignore**: `.env` está excluido del version control.
