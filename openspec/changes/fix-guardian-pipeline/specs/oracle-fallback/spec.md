## ADDED Requirements

### Requirement: Manejo graceful de oráculo ausente
La función `compilar()` en `guardian_client.py` DEBE verificar la existencia de `casos_prueba.md` antes de intentar leerlo. Si no existe, DEBE usar el fallback por plantilla con un mensaje de advertencia.

#### Scenario: casos_prueba.md no existe
- **WHEN** se ejecuta `compilar()`
- **AND** `casos_prueba.md` no existe en la raíz del proyecto
- **THEN** se muestra un warning en consola
- **AND** se ejecuta `generate_test_engine_fallback()` sin lanzar excepción

#### Scenario: casos_prueba.md existe
- **WHEN** se ejecuta `compilar()`
- **AND** `casos_prueba.md` existe
- **THEN** se lee el oráculo normalmente
- **AND** se intenta generación vía LLM primero

### Requirement: Test_engine.py siempre se genera
El pipeline DEBE producir `test_engine.py` incluso si el oráculo no existe, usando el fallback por plantilla.

#### Scenario: Pipeline sin oráculo
- **WHEN** se ejecuta `ejecutar_y_veredicto()`
- **AND** no hay `casos_prueba.md`
- **THEN** se genera `test_engine.py` con las pruebas del fallback
- **AND** se ejecutan los tests
- **AND** se emite `veredicto.json`
