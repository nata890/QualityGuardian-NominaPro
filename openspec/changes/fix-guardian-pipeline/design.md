## Context

El pipeline del Guardian Agent tiene tres problemas de ejecución local que impiden su uso desde CLI:

1. **Import path**: Tras el refactor-structure, los scripts usan `from src.xxx import` pero al ejecutar `python src/guardian_client.py` Python pone `src/` en `sys.path`, no la raíz del proyecto, causando `ModuleNotFoundError: No module named 'src'`.
2. **API key**: La variable `OPENROUTER_API_KEY` solo existe en `.env` pero ningún script la carga automáticamente. Requiere `source .env` manual.
3. **Oráculo ausente**: `casos_prueba.md` (responsabilidad del Oracle Agent, Miguel Coronado) no existe, y `leer_oraculo()` crashea sin intentar el fallback por plantilla.

## Goals / Non-Goals

**Goals:**
- Que `python src/guardian_client.py` y `python scripts/validar_conexion.py` funcionen directamente sin flags especiales
- Que la API key se cargue automáticamente desde `.env` al ejecutar cualquier script del pipeline
- Que la ausencia de `casos_prueba.md` no crashee el pipeline — debe usar el fallback por plantilla con un warning
- Que `infra/requirements.txt` exista con todas las dependencias

**Non-Goals:**
- No se rediseña la arquitectura de imports del paquete `src/`
- No se modifica la estructura de `tests/test_engine.py`
- No se implementa la generación del oráculo (eso es US-NOM02)

## Decisions

### Decisión 1: Resolución de imports — `sys.path.insert` en cada script

**Opción elegida**: Agregar bloque de ajuste de `sys.path` al inicio de `guardian_client.py` y `validar_conexion.py`.

```python
if __name__ == "__main__" and __package__ is None:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
```

**Alternativas descartadas:**
- ~~Usar `PYTHONPATH` en script wrapper~~: Requiere script adicional, no es transparente.
- ~~Mover todo a un `main.py` en raíz~~: Rompe la estructura actual donde cada script es autónomo.
- ~~Solo documentar `python -m`~~: No soluciona el problema raíz, el pipeline script usa ejecución directa.

**Razón**: Es el approach más mínimos y autónomo. Cada script se arregla a sí mismo sin depender de configuración externa. Es un patrón estándar en paquetes Python ejecutables.

### Decisión 2: Auto-carga de `.env` — `python-dotenv`

**Opción elegida**: Usar `python-dotenv` con `load_dotenv()` al inicio de `guardian_client.py` y `validar_conexion.py`.

```python
from dotenv import load_dotenv
load_dotenv()
```

**Alternativas descartadas:**
- ~~Leer `.env` manualmente~~: Más código, no maneja quotes, comentarios, escaping.
- ~~Confiar en `source .env` externo~~: Frágil, documentación olvidada.

**Razón**: `python-dotenv` es la biblioteca estándar de facto para carga de `.env`. Mínimo código, edge cases cubiertos.

### Decisión 3: Oracle ausente — validación temprana con fallback

**Opción elegida**: En `compilar()`, verificar existencia de `ORACULO_PATH` antes de llamar `leer_oraculo()`. Si no existe, loguear warning y llamar `generate_test_engine_fallback("")` directamente.

**Razón**: El flujo actual llama a `leer_oraculo()` que lanza `FileNotFoundError`. Moviendo la validación antes se puede desviar al fallback sin excepción.

### Decisión 4: Dependencias — crear `infra/requirements.txt`

Crear el archivo faltante con:
```
requests>=2.31.0
pytest>=8.0.0
python-dotenv>=1.0.0
```

Actualizar Dockerfile para copiar e instalar desde este archivo.

## Risks / Trade-offs

- **[Riesgo] `python-dotenv` no disponible en CI de GitHub Actions** → En CI las variables se pasan por `env:` en el workflow, `load_dotenv()` falla silenciosamente si no hay `.env`, lo cual es aceptable.
- **[Riesgo] `sys.path.insert` frágil si se reestructura el proyecto** → Si se mueven los scripts, hay que actualizar la ruta relativa `parent.parent`. Es un riesgo manejable y explícito en el código.
- **[Trade-off] Acoplamiento a `python-dotenv`** vs. **código manual**: Preferimos la dependencia externa por claridad y mantenibilidad. Es una biblioteca pequeña y madura.
