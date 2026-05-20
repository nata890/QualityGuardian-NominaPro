## Context

Sprint 1 COIL UdeCaldas × UMB (Grupo 2, Caso Nómina Pro). 3 HU comprometidas:
- **US-NOM01** (3pt): Natalia implementa `liquidar_nomina` en `engine.py` — 7 CA
- **US-NOM02** (0pt): Miguel redacta `casos_prueba.md` con ≥10 escenarios — 6 CA
- **US-NOM03** (0pt): Daner configura Agente Guardian LangChain + OpenRouter API (modelo remoto `baidu/cobuddy`) + Docker + CI/CD — 7 CA

Se requiere un `AGENTS.md` en la raíz del repositorio que formalice el ecosistema de agentes con roles inmutables, System Prompts y Tool Access Policies.

## Goals / Non-Goals

**Goals:**
- Definir la estructura del archivo `AGENTS.md` que residirá en la raíz del repositorio.
- Establecer 5 perfiles de agente: Orchestrator (automatizado), Lead Dev (Natalia), Oracle (Miguel), Guardian (Daner), DevOps (Daner).
- Especificar System Prompts base, Tool Access Policies y protocolo de veredicto JSON.
- Vincular cada agente a sus HU y criterios de aceptación.

**Non-Goals:**
- No implementar el contenido de engine.py ni casos_prueba.md (son tareas del equipo).
- No configurar la integración con OpenRouter API ni Docker real (eso hará Daner siguiendo el diseño).
- No cubrir Sprints 2–6.

## Decisions

| Decisión | Elegida | Rationale |
|---|---|---|
| 5 agentes para 3 personas | Orchestrator automatizado, Natalia→Lead Dev, Miguel→Oracle, Daner→Guardian+DevOps | El pipeline tiene 4 etapas técnicas + 1 capa de coordinación. Daner tiene el perfil de AI Engineer para asumir Guardian y DevOps. |
| `AGENTS.md` en raíz del repo | Raíz del repositorio | Artefacto de gobierno del equipo. Debe ser visible para todos los miembros y la célula compañera. |
| Orchestrator sin dueño humano | Agente automatizado (sistema) | Coordina flujo, invoca agentes según estado de HU, no requiere intervención humana constante. |

## Architecture

```
 repositorio/
 ├── AGENTS.md              ← artefacto de gobierno (este diseño lo define)
 ├── engine.py              ← implementado por Lead Dev (Natalia)
 ├── casos_prueba.md        ← redactado por Oracle (Miguel)
 ├── test_engine.py         ← generado por Guardian (Daner) vía LangChain+OpenRouter
 ├── Dockerfile             ← creado por DevOps (Daner)
 ├── .github/workflows/ci.yml ← configurado por DevOps (Daner)
 └── veredicto.json         ← emitido por Guardian (Daner) tras ejecución Docker
```

### Pipeline de datos y agentes

```
┌──────────────┐     ┌──────────────┐     ┌───────────────────┐
│  LEAD DEV     │     │  ORACLE      │     │  GUARDIAN + DEVOPS │
│  (Natalia)    │────▶│  (Miguel)    │────▶│  (Daner)           │
│  engine.py    │     │ casos_prueba │     │  test_engine.py    │
│  R1-R5        │     │ .md (Gherkin)│     │  OpenRouter API    │
│  tipado+doc   │     │ 10+ casos    │     │  Docker runtime    │
└──────────────┘     └──────────────┘     │  CI/CD (GH Actions)│
                                           │  veredicto.json    │
                                           └───────────────────┘
                                                    ▲
                                           ┌────────┴────────┐
                                           │  ORCHESTRATOR    │
                                           │  (automatizado)  │
                                           │  coordina flujo  │
                                           │  valida pipeline │
                                           └─────────────────┘
```

## AGENTS.md Structure

El archivo `AGENTS.md` en la raíz del repositorio DEBE contener las siguientes secciones:

### 1. Matriz de responsabilidades (persona → agente → HU)

| Persona | Agente | HU | Entregable |
|---|---|---|---|
| Natalia Ceballos (UdeC) | Lead Dev Agent | US-NOM01 | engine.py con R1–R5 |
| Miguel Coronado (UMB) | Oracle Agent | US-NOM02 | casos_prueba.md (≥10 Gherkin) |
| Daner Salazar (UdeC) | Guardian Agent | US-NOM03 | LangChain + OpenRouter + Pytest + Veredicto |
| Daner Salazar (UdeC) | DevOps Agent | US-NOM03 | Dockerfile + GH Actions CI |
| Miguel Coronado (UMB) | Orchestrator Agent | Transversal | Coordinación del pipeline |

### 2. System Prompts base (por perfil)

Cada perfil DEBE incluir:
- **Rol**: nombre del agente y persona responsable.
- **Propósito**: una línea que describe su función en el pipeline.
- **Responsabilidades**: lista de acciones concretas que ejecuta.
- **Límites**: qué NO puede hacer (ej. no commitea código, no modifica artifacts de otro agente).
- **System Prompt**: texto completo del prompt que gobierna al agente.

### 3. Tool Access Policies

| Agente | Lectura | Escritura | Prohibido |
|---|---|---|---|
| Orchestrator | planning/, openspec/changes/ | task_plan.md, progress.md | Modificar código o specs |
| Lead Dev | engine.py, especificación R1–R5 | Propuestas (snippets) en .planning/ | Commit sin aprobación humana |
| Oracle | engine.py, R1–R5 | DRAFT casos_prueba.md en .planning/ | Modificar engine.py |
| Guardian | casos_prueba.md, engine.py (read-only) | test_engine.py, veredicto.json en .planning/ | Ejecutar fuera de contenedor Docker |
| DevOps | Dockerfiles, .github/workflows/ | Dockerfile, ci.yml propuestos | Despliegue a producción sin aprobación |

### 4. Protocolo de validación de veredicto JSON (Guardian Agent)

El Guardian Agent DEBE emitir un archivo `veredicto.json` con esta estructura:

```json
{
  "escenarios": [
    {
      "id": "R1-nominal",
      "descripcion": "Recargo diurno 25% sobre hora ordinaria",
      "resultado": "PASS",
      "duracion_ms": 12
    }
  ],
  "resumen": {
    "total": 10,
    "pasaron": 9,
    "fallaron": 1,
    "cobertura": "72.5%"
  },
  "metadata": {
    "modelo": "baidu/cobuddy",
    "timestamp": "2026-05-20T10:00:00Z",
    "oraculo": "casos_prueba.md"
  }
}
```

## Risks / Trade-offs

| Riesgo | Mitigación |
|---|---|
| [R1] `AGENTS.md` se desactualiza respecto a cambios reales | Incluir en tasks.md una tarea de revisión periódica del AGENTS.md contra el estado actual del pipeline. |
| [R2] Daner tiene carga alta (Guardian + DevOps) | Los agentes son asistentes, no reemplazos. Daner prioriza Guardian (core del pipeline); DevOps es configurable en 2–3 tareas. |
| [R3] Dependencia de conectividad a OpenRouter API (caídas, rate limits, latencia) | Tasks 3.1–3.2 incluyen manejo de errores HTTP, retry con backoff, timeouts y fallback a respuestas simuladas en CI offline. |
| [R4] Veredicto JSON puede no ser válido si cambia la estructura | El protocolo JSON está definido en AGENTS.md y debe validarse contra schema en CI. |
| [R5] Exposición de OPENROUTER_API_KEY en código o prompts | **Nunca incluir la API key en texto plano.** Debe cargarse exclusivamente desde variable de entorno `OPENROUTER_API_KEY`. El AGENTS.md y design.md lo documentan como requisito de seguridad. |

## Open Questions

- ¿OpenRouter API key se inyecta como secret de GitHub Actions o variable de entorno local? → **Ambas**: `OPENROUTER_API_KEY` como variable de entorno local para desarrollo, y como GitHub Secret para CI. Nunca hardcodeada.
- ¿La validación del veredicto JSON se hace con schema (JSON Schema, Zod) o validación manual? → Propuesta: JSON Schema en CI.
- ¿Timeout de API aceptable para inferencia? → Propuesta: 30s con 2 reintentos (backoff exponencial).
- Modelo utilizado: `baidu/cobuddy` vía endpoint `https://openrouter.ai/api/v1/chat/completions`.
