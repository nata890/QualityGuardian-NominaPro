## ADDED Requirements

### Requirement: Scripts ejecutables directamente desde CLI
Los scripts `src/guardian_client.py` y `scripts/validar_conexion.py` DEBEN poder ejecutarse con `python <ruta>` sin errores de import.

#### Scenario: guardian_client.py se ejecuta directamente
- **WHEN** se invoca `python src/guardian_client.py` desde la raíz del proyecto
- **THEN** el script se ejecuta sin lanzar `ModuleNotFoundError`

#### Scenario: validar_conexion.py se ejecuta directamente
- **WHEN** se invoca `python scripts/validar_conexion.py` desde la raíz del proyecto
- **THEN** el script se ejecuta sin lanzar `ModuleNotFoundError`

#### Scenario: python -m también funciona
- **WHEN** se invoca `python -m src.guardian_client`
- **THEN** el script funciona correctamente (regresión: no romper el modo módulo)

### Requirement: Mecanismo portátil de resolución de imports
El mecanismo de ajuste de `sys.path` DEBE usar rutas relativas al archivo, no absolutas ni asumir un directorio de trabajo específico.

#### Scenario: Ruta calculada desde __file__
- **WHEN** el script calcula la raíz del proyecto
- **THEN** usa `Path(__file__).resolve().parent.parent` para scripts en `src/` y `Path(__file__).resolve().parent` para scripts en raíz
