## 1. Crear estructura de directorios

- [x] 1.1 Crear directorios: `src/`, `tests/`, `infra/`, `scripts/`
- [x] 1.2 Crear `src/__init__.py` para habilitar imports como paquete

## 2. Actualizar imports en archivos destino

- [x] 2.1 Modificar `guardian_client.py`: `from guardia_api` → `from src.guardia_api`
- [x] 2.2 Modificar `test_engine.py`: `from engine` → `from src.engine`
- [x] 2.3 Modificar `validar_conexion.py`: `from guardia_api` → `from src.guardia_api`

## 3. Mover archivos con git mv (preserva historial)

- [x] 3.1 `git mv engine.py src/engine.py`
- [x] 3.2 `git mv guardia_api.py src/guardia_api.py`
- [x] 3.3 `git mv guardian_client.py src/guardian_client.py`
- [x] 3.4 `git mv test_engine.py tests/test_engine.py`
- [x] 3.5 `git mv validar_conexion.py scripts/validar_conexion.py`
- [x] 3.6 `git mv validar_pipeline.sh scripts/validar_pipeline.sh`
- [x] 3.7 `git mv requirements.txt infra/requirements.txt`
- [x] 3.8 `git mv Dockerfile infra/Dockerfile`

## 4. Actualizar rutas en CI y Docker

- [x] 4.1 Actualizar `.github/workflows/ci.yml`: cambiar paths de python/guardian_client/validar_conexion a scripts/ y src/
- [x] 4.2 Actualizar `infra/Dockerfile`: cambiar COPY paths a src/, tests/, scripts/

## 5. Validación post-movimiento

- [x] 5.1 Ejecutar `python -m pytest tests/test_engine.py -v` desde raíz y verificar 11/11 PASS
- [x] 5.2 Ejecutar `python -c "from src.engine import liquidar_nomina; print('import OK')"` desde raíz
- [x] 5.3 Ejecutar `python -c "from src.guardia_api import ping; print('import OK')"` desde raíz
- [x] 5.4 Validar sintaxis de `infra/Dockerfile` con `docker build` dry-run
- [x] 5.5 Ejecutar `openspec validate refactor-structure` y confirmar

## 6. Limpieza

- [x] 6.1 Verificar que no queden archivos `.py` originales en la raíz (excepto los de otros roles)
- [x] 6.2 Actualizar `AGENTS.md` si las rutas de Tool Access cambian
- [x] 6.3 Commit final con mensaje: `refactor: move source files to src/tests/infra/scripts`
