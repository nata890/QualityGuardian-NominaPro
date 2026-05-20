## Context

Actualmente 11 archivos en la raíz del repositorio sin estructura de directorios, mezclando código fuente, tests, configuraciones y scripts. La refactorización debe preservar todas las relaciones de importación y rutas de CI/CD.

### Mapa de dependencias actual

```
engine.py ── importado por ──→ test_engine.py
guardia_api.py ── importado por ──→ guardian_client.py, validar_conexion.py
Dockerfile ── COPY de ──→ engine.py, guardia_api.py, guardian_client.py, test_engine.py, validar_conexion.py, casos_prueba.md
.github/workflows/ci.yml ── ejecuta ──→ validar_conexion.py, guardian_client.py, test_engine.py
```

### Archivos por responsable

| Responsable | Archivos | Acción |
|---|---|---|
| US-NOM03 (Daner) | engine.py, guardia_api.py, guardian_client.py, test_engine.py, validar_conexion.py, validar_pipeline.sh, Dockerfile, requirements.txt | Mover |
| Compartido/Raíz | AGENTS.md, README.md, .env, .gitignore | No mover |
| Infraestructura | .github/workflows/ci.yml | Actualizar paths |

## Goals / Non-Goals

**Goals:**
- Separar el código fuente en `src/`, tests en `tests/`, infraestructura en `infra/` y scripts en `scripts/`.
- Actualizar todos los imports y referencias de ruta para que el pipeline funcione después del movimiento.
- Preservar el historial de git (`git mv` para mantener trazabilidad).

**Non-Goals:**
- No mover archivos de US-NOM02 (Miguel). Si `casos_prueba.md` existe, permanece en raíz.
- No cambiar la lógica interna de ningún archivo, solo sus rutas.
- No refactorizar el contenido de AGENTS.md.

## Architecture objetivo

```
repositorio/
├── AGENTS.md
├── README.md
├── .env
├── .gitignore
├── src/
│   ├── engine.py             ← lógica R1-R5
│   ├── guardia_api.py        ← cliente OpenRouter
│   └── guardian_client.py    ← orquestador
├── tests/
│   └── test_engine.py        ← 11 tests Pytest
├── infra/
│   ├── Dockerfile            ← multi-stage
│   └── requirements.txt      ← dependencias
├── scripts/
│   ├── validar_conexion.py   ← diagnóstico
│   └── validar_pipeline.sh   ← orquestación CI local
├── .github/
│   └── workflows/
│       └── ci.yml            ← CI/CD (paths actualizados)
└── openspec/
    └── changes/
        ├── design-coil-agents-ecosystem/
        └── refactor-structure/   ← este cambio
```

## Decisions

| Decisión | Elegida | Rationale |
|---|---|---|
| `git mv` vs copiar+borrar | `git mv` | Preserva historial y blame. |
| `src/` vs `app/` | `src/` | Convención estándar Python para proyectos con tests y scripts separados. |
| `infra/` vs `docker/` | `infra/` | Más genérico para incluir CI y configuraciones. |
| Imports: `from src.engine` vs sys.path | `from src.engine` | Explícito y sin efectos secundarios. Requiere que `src/` sea un paquete (con `__init__.py`). |

## Risks / Trade-offs

| Riesgo | Mitigación |
|---|---|
| Imports rotos tras mover archivos | Actualizar TODOS los imports antes de mover: `from engine` → `from src.engine`. Se aplica en un solo commit atómico. |
| CI/CD falla por paths desactualizados | Actualizar `ci.yml` y `Dockerfile` en el mismo commit que los movimientos. |
| Scripts externos referencian paths absolutos | Documentar el cambio. Es breaking change menor (sprint 1, aún sin consumidores externos). |
| `guardian_client.py` espera `casos_prueba.md` en raíz | `guardian_client.py` ya tiene manejo de FileNotFoundError. La ruta del oráculo se actualiza a `../casos_prueba.md` desde `src/` si existe. |

## Imports a modificar

| Archivo | Import actual | Import nuevo |
|---|---|---|
| `src/guardian_client.py` | `from guardia_api import inferir` | `from src.guardia_api import inferir` |
| `tests/test_engine.py` | `from engine import liquidar_nomina` | `from src.engine import liquidar_nomina` |
| `scripts/validar_conexion.py` | `from guardia_api import ping` | `from src.guardia_api import ping` |
