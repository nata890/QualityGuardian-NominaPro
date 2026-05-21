## 1. Dependencias

- [x] 1.1 Crear `infra/requirements.txt` con `requests`, `pytest`, `python-dotenv`

## 2. Import path fix

- [x] 2.1 Agregar bloque `sys.path.insert` en `src/guardian_client.py` (antes de `from src.guardia_api import`)
- [x] 2.2 Agregar bloque `sys.path.insert` en `scripts/validar_conexion.py` (antes de `from src.guardia_api import`)

## 3. Auto-carga de .env

- [x] 3.1 Agregar `from dotenv import load_dotenv; load_dotenv()` al inicio de `src/guardian_client.py`
- [x] 3.2 Agregar `from dotenv import load_dotenv; load_dotenv()` al inicio de `scripts/validar_conexion.py`

## 4. Oracle fallback

- [x] 4.1 Modificar `compilar()` en `guardian_client.py` para verificar existencia de `casos_prueba.md` antes de leerlo
- [x] 4.2 Si no existe, llamar `generate_test_engine_fallback("")` con warning en consola

## 5. Dockerfile

- [x] 5.1 Actualizar `infra/Dockerfile` para copiar `infra/requirements.txt` e instalar dependencias
- [x] 5.2 Verificar que el CMD funcione con la nueva lógica de imports (ajustar ruta de ejecución si es necesario)

## 6. Verificación

- [x] 6.1 Ejecutar `python src/guardian_client.py` y confirmar que no da `ModuleNotFoundError`
- [x] 6.2 Ejecutar `python scripts/validar_conexion.py` y confirmar que carga la key desde `.env`
- [x] 6.3 Ejecutar `python -m pytest tests/test_engine.py -v --tb=short` y confirmar 11/11 PASS
- [x] 6.4 Ejecutar `pip install -r infra/requirements.txt` y confirmar instalación limpia
