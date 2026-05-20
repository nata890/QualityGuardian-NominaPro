## Why

El Sprint 1 del proyecto COIL UdeCaldas × UMB necesita un archivo `AGENTS.md` en la raíz del repositorio que defina el ecosistema de 5 agentes (Orchestrator, Lead Dev, Oracle, Guardian, DevOps) con roles, responsabilidades, System Prompts y Tool Access Policies. Sin este artefacto, el equipo carece de una arquitectura de agentes auditable que vincule cada artifact del pipeline (engine.py → casos_prueba.md → tests Docker → veredicto JSON) a los criterios de aceptación de las 3 HU del Sprint 1.

## What Changes

- Creación de `AGENTS.md` en la raíz del repositorio con los 5 perfiles de agente.
- Matriz de responsabilidades persona→agente→HU:
  - Natalia → Lead Dev Agent → US-NOM01 (engine.py, R1–R5)
  - Miguel → Oracle Agent → US-NOM02 (casos_prueba.md, 10+ escenarios Gherkin)
  - Daner → Guardian Agent + DevOps Agent → US-NOM03 (LangChain+Llama 3 8B, Docker, Pytest, CI/CD, veredicto JSON)
- Orchestrator Agent como capa de coordinación automatizada del pipeline.
- System Prompts base para cada perfil con límites explícitos.
- Tool Access Policies que definen qué puede leer/escribir cada agente.

## Capabilities

### New Capabilities
- `agents-ecosystem`: Arquitectura de 5 agentes con mapeo persona→agente, System Prompts, Tool Access Policies y protocolo de veredicto JSON para el Guardian Agent.

### Modified Capabilities
- (ninguna)

## Impact

- Crea `AGENTS.md` en la raíz del repositorio como artefacto de gobierno.
- No modifica código de `engine.py` ni archivos existentes.
- Roles inmutables: Natalia (Lead Dev), Miguel (Oracle), Daner (Guardian + DevOps).
