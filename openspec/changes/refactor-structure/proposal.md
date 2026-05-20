## Why

La raíz del repositorio contiene 11 archivos de código, configuración y scripts mezclados sin estructura de directorios. Esto dificulta la navegación, el mantenimiento y la comprensión del rol de cada componente. Se propone una estructura estándar con carpetas `src/`, `tests/`, `infra/` y `scripts/` que aisle responsabilidades y prepare el repo para escalar a Sprints 2–6.

## What Changes

- Creación de carpetas: `src/`, `tests/`, `infra/`, `scripts/`.
- Movimiento de archivos US-NOM03 (Daner) a sus nuevas ubicaciones.
- Actualización de imports relativos en los archivos Python movidos.
- Actualización de rutas en `Dockerfile` (COPY) y `.github/workflows/ci.yml`.
- **BREAKING**: Los paths de los archivos cambian. Cualquier script o configuración externa que referencie paths absolutos dejará de funcionar.

## Capabilities

### New Capabilities
- `project-structure`: Organización estándar con `src/`, `tests/`, `infra/`, `scripts/` que aísla responsabilidades y clarifica la propiedad de cada módulo.

### Modified Capabilities
- (ninguna — primer cambio estructural)

## Impact

- **Archivos movidos** (US-NOM03):
  - `engine.py` → `src/engine.py`
  - `guardia_api.py` → `src/guardia_api.py`
  - `guardian_client.py` → `src/guardian_client.py`
  - `test_engine.py` → `tests/test_engine.py`
  - `validar_conexion.py` → `scripts/validar_conexion.py`
  - `validar_pipeline.sh` → `scripts/validar_pipeline.sh`
  - `requirements.txt` → `infra/requirements.txt`
  - `Dockerfile` → `infra/Dockerfile`
- **Archivos NO movidos** (US-NOM02, compartidos o raíz):
  - `AGENTS.md` — permanece en raíz (gobierno del repo)
  - `README.md` — permanece en raíz
  - `.env` — permanece en raíz
  - `.gitignore` — permanece en raíz
  - `.github/workflows/ci.yml` — se actualizan paths internos
- **Imports a actualizar**:
  - `guardian_client.py`: `from guardia_api` → `from src.guardia_api`
  - `validar_conexion.py`: `from guardia_api import` → `from src.guardia_api import`
  - `test_engine.py`: `from engine import` → `from src.engine import`
