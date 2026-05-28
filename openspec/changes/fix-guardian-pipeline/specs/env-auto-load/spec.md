## ADDED Requirements

### Requirement: Carga automática de OPENCODE_ZEN_API_KEY desde .env
Los scripts del pipeline DEBEN cargar la variable `OPENCODE_ZEN_API_KEY` desde el archivo `.env` en la raíz del proyecto si no está ya definida en el entorno.

#### Scenario: .env existe y contiene la key
- **WHEN** se ejecuta `guardian_client.py` o `validar_conexion.py`
- **AND** el archivo `.env` existe en la raíz con `OPENCODE_ZEN_API_KEY=sk-...`
- **THEN** la variable queda disponible en `os.environ`

#### Scenario: .env no existe
- **WHEN** se ejecuta cualquiera de los scripts
- **AND** el archivo `.env` no existe
- **THEN** el script no crashea, solo que `OPENCODE_ZEN_API_KEY` no estará definida

#### Scenario: OPENCODE_ZEN_API_KEY ya está en el entorno
- **WHEN** se ejecuta cualquiera de los scripts
- **AND** `OPENCODE_ZEN_API_KEY` ya está definida en el entorno
- **THEN** no se sobreescribe ni se modifica

### Requirement: Dependencia python-dotenv
El proyecto DEBE incluir `python-dotenv` como dependencia en `infra/requirements.txt`.

#### Scenario: requirements.txt contiene python-dotenv
- **WHEN** se inspecciona `infra/requirements.txt`
- **THEN** contiene `python-dotenv>=1.0.0`
