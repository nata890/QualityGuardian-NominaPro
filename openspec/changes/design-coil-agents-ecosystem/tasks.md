## 1. US-NOM01: Implementar engine.py (Responsable: Natalia — Lead Dev)

- [x] 1.1 Natalia: Redactar engine.py con función liquidar_nomina tipada y docstring (US-NOM01 C1)
- [x] 1.2 Natalia: Implementar R1 — recargo 25% sobre hora ordinaria para extras diurnas (US-NOM01 C2)
- [x] 1.3 Natalia: Implementar R2 — recargo 75% sobre hora ordinaria para extras nocturnas (US-NOM01 C3)
- [x] 1.4 Natalia: Implementar R3 — descuentos 4% salud + 4% pensión sobre total devengado (US-NOM01 C4)
- [x] 1.5 Natalia: Implementar R4 — auxilio de transporte $162.000 si salario ≤ $2.600.000 (US-NOM01 C5)
- [x] 1.6 Natalia: Implementar R5 — validaciones con ValueError (salario < SMMLV, horas negativas) (US-NOM01 C6)
- [x] 1.7 Natalia: Verificar tipado consistente y legibilidad para LLM (US-NOM01 C7)
- [x] 1.8 Miguel (Orchestrator delegado): Coordinar revisión de engine.py por célula compañera
- [x] 1.9 Natalia: Aprobar y comitear engine.py

## 2. US-NOM02: Redactar oráculo de pruebas (Responsable: Miguel — Oracle)

- [ ] 2.1 Miguel: Crear casos_prueba.md con estructura Gherkin (Dado/Cuando/Entonces)
- [ ] 2.2 Miguel: Redactar escenarios nominales para cada regla R1–R5 (≥1 por regla)
- [ ] 2.3 Miguel: Redactar escenarios de caso límite (salario = SMMLV, tope auxilio, horas = 0, horas negativas, valores máximos)
- [ ] 2.4 Miguel: Verificar cobertura total ≥10 escenarios y formato legible por LLM
- [ ] 2.5 Miguel: Coordinar revisión de casos_prueba.md por célula compañera
- [ ] 2.6 Miguel: Aprobar y comitear casos_prueba.md

## 3. US-NOM03: Configurar Agente Guardian vía OpenRouter API (Responsable: Daner — Guardian + DevOps)

- [x] 3.1 Daner: Configurar variable de entorno `OPENROUTER_API_KEY` y cliente Python para peticiones a `https://openrouter.ai/api/v1/chat/completions` con modelo `baidu/cobuddy`. **No hardcodear la clave en el código.**
- [x] 3.2 Daner: Validar conectividad a OpenRouter API, latencia de inferencia y manejo de errores HTTP (timeouts, rate limits, 4xx/5xx)
- [x] 3.3 Daner: Implementar script LangChain que lea casos_prueba.md como contexto
- [x] 3.4 Daner: Implementar generación de test_engine.py con Pytest a partir del oráculo vía OpenRouter
- [x] 3.5 Daner: Verificar que cada escenario Gherkin se traduzca a una función test_* en Pytest
- [x] 3.6 Daner (DevOps): Crear Dockerfile multi-stage para ejecución aislada de pruebas (inyectar OPENROUTER_API_KEY como secret)
- [x] 3.7 Daner (DevOps): Configurar GitHub Actions CI que ejecute Guardian Agent en contenedor Docker en cada push a main (con OPENROUTER_API_KEY desde secrets)
- [x] 3.8 Daner: Implementar emisión de veredicto.json (pass/fail por escenario + cobertura + resumen)
- [x] 3.9 Daner: Verificar que el contenedor Docker no tenga acceso de escritura al host
- [x] 3.10 Daner (DevOps): Configurar artifacts de CI para almacenar veredicto.json y reporte de cobertura
- [x] 3.11 Daner: Validar pipeline completo — engine.py → oráculo → guardian → veredicto
- [x] 3.12 Daner: Aprobar pipeline y cerrar US-NOM03

## 4. Generar AGENTS.md en la raíz del repositorio

- [x] 4.1 Miguel (Orchestrator delegado): Redactar matriz de responsabilidades persona→agente→HU
- [x] 4.2 Miguel (Orchestrator delegado): Redactar System Prompt del Lead Dev Agent (Natalia, US-NOM01)
- [x] 4.3 Miguel (Orchestrator delegado): Redactar System Prompt del Oracle Agent (Miguel, US-NOM02)
- [x] 4.4 Miguel (Orchestrator delegado): Redactar System Prompt del Guardian Agent (Daner, US-NOM03)
- [x] 4.5 Miguel (Orchestrator delegado): Redactar System Prompt del DevOps Agent (Daner, US-NOM03)
- [x] 4.6 Miguel (Orchestrator delegado): Redactar System Prompt del Orchestrator Agent (Miguel, US-NOM03)
- [x] 4.7 Miguel (Orchestrator delegado): Incluir tabla de Tool Access Policies (lectura/escritura/prohibiciones por agente)
- [x] 4.8 Miguel (Orchestrator delegado): Incluir protocolo de veredicto JSON (schema y validación)
- [x] 4.9 Miguel (Orchestrator delegado): Guardar AGENTS.md en la raíz del repositorio

## 5. Validación y cierre

- [x] 5.1 Ejecutar `openspec validate design-coil-agents-ecosystem` y verificar que pasa
- [x] 5.2 Confirmar que los 5 perfiles de agente están definidos en AGENTS.md con sus System Prompts
- [x] 5.3 Confirmar que AGENTS.md está en la raíz del repositorio
- [x] 5.4 Entregar resumen al equipo con las asignaciones correctas: Natalia (Lead Dev), Miguel (Oracle), Daner (Guardian + DevOps)
- [x] 5.5 Marcar change design-coil-agents-ecosystem como apply-ready
