## Why

El pipeline del Guardian Agent no se puede ejecutar desde línea de comandos por tres fallas encadenadas: (1) los imports relativos `from src.*` fallan al ejecutar los scripts directamente, (2) la API key de OpenCode Zen no se carga automáticamente desde `.env`, y (3) la ausencia del oráculo `casos_prueba.md` provoca un crash sin fallback. Esto bloquea la ejecución local del pipeline y la validación de conectividad con OpenCode Zen.

## What Changes

- **Fix import paths en `guardian_client.py` y `validar_conexion.py`**: Agregar lógica de `sys.path.insert` para que ambos scripts funcionen tanto con `python src/guardian_client.py` como con `python -m src.guardian_client`.
- **Auto-carga de `.env`**: Implementar carga de variable `OPENCODE_ZEN_API_KEY` desde archivo `.env` usando `python-dotenv` o lectura directa, para que no sea necesario `source .env` manualmente.
- **Manejo graceful de `casos_prueba.md` ausente**: Validar existencia del oráculo antes de leerlo y ejecutar fallback por plantilla si no existe, en lugar de lanzar `FileNotFoundError`.
- **Actualizar dependencias**: Agregar `python-dotenv` a `infra/requirements.txt` (crearlo si no existe).
- **Actualizar Dockerfile**: Agregar `python-dotenv` y ajustar CMD para funcionar con la nueva lógica de imports.

## Capabilities

### New Capabilities
- `import-path-fix`: Mecanismo de resolución de imports que permite ejecutar scripts del paquete `src/` directamente desde CLI sin depender de `python -m`.
- `env-auto-load`: Carga automática de variables de entorno desde `.env` al iniciar los scripts del pipeline.
- `oracle-fallback`: Manejo graceful del oráculo de pruebas ausente con fallback a generación por plantilla.

### Modified Capabilities
- (ninguna — los specs son nuevos)

## Impact

- **Archivos modificados**:
  - `src/guardian_client.py` — fix de import path + auto-carga .env + manejo oracle ausente
  - `scripts/validar_conexion.py` — fix de import path + auto-carga .env
  - `infra/Dockerfile` — agregar dotenv, ajustar CMD
  - `infra/requirements.txt` — **CREAR** con requests, pytest, python-dotenv
- **Dependencias nuevas**: `python-dotenv`
- **No breaking**: Los cambios son aditivos. No se modifican interfaces públicas ni rutas de archivos.
