## ADDED Requirements

### Requirement: Standard directory structure
The repository SHALL organize its files into `src/`, `tests/`, `infra/`, and `scripts/` directories.

#### Scenario: src/ directory contains core modules
- **WHEN** inspecting the repository
- **THEN** `src/` contains `engine.py`, `guardia_api.py`, `guardian_client.py` and an `__init__.py`

#### Scenario: tests/ directory contains test files
- **WHEN** inspecting the repository
- **THEN** `tests/` contains `test_engine.py`

#### Scenario: infra/ directory contains infrastructure
- **WHEN** inspecting the repository
- **THEN** `infra/` contains `Dockerfile` and `requirements.txt`

#### Scenario: scripts/ directory contains utilities
- **WHEN** inspecting the repository
- **THEN** `scripts/` contains `validar_conexion.py` and `validar_pipeline.sh`

### Requirement: Imports updated after move
All Python imports SHALL be updated to reflect the new directory structure.

#### Scenario: guardian_client imports from src.guardia_api
- **WHEN** reading `src/guardian_client.py`
- **THEN** its import line reads `from src.guardia_api import inferir`

#### Scenario: test_engine imports from src.engine
- **WHEN** reading `tests/test_engine.py`
- **THEN** its import line reads `from src.engine import liquidar_nomina`

#### Scenario: validar_conexion imports from src.guardia_api
- **WHEN** reading `scripts/validar_conexion.py`
- **THEN** its import line reads `from src.guardia_api import ping`

### Requirement: CI/CD paths updated
The CI workflow and Dockerfile SHALL reference the new paths.

#### Scenario: CI workflow runs scripts from scripts/
- **WHEN** CI executes `validar_conexion.py` and `guardian_client.py`
- **THEN** the paths in `.github/workflows/ci.yml` point to `scripts/` and `src/` respectively

#### Scenario: Dockerfile COPY uses new paths
- **WHEN** building the Docker image
- **THEN** `infra/Dockerfile` COPYs from `src/`, `tests/`, and `scripts/` directories
