## ADDED Requirements

### Requirement: AGENTS.md exists at repository root
The repository SHALL contain an `AGENTS.md` file at its root that defines the 5-agent ecosystem (Orchestrator, Lead Dev, Oracle, Guardian, DevOps) with responsibilities, System Prompts, and Tool Access Policies.

#### Scenario: AGENTS.md is present at root
- **WHEN** inspecting the repository root
- **THEN** the file AGENTS.md exists

#### Scenario: AGENTS.md contains matrix of responsibilities
- **WHEN** reading AGENTS.md
- **THEN** it includes a table mapping each agent to a human responsible person and a HU identifier (US-NOM01, US-NOM02, US-NOM03)

### Requirement: Roles are immutable in AGENTS.md
The AGENTS.md SHALL assign each agent to exactly one person with no ambiguity:
- Lead Dev Agent → Natalia Ceballos (UdeC) → US-NOM01
- Oracle Agent → Miguel Coronado (UMB) → US-NOM02
- Guardian Agent → Daner Alejandro Salazar Colorado (UdeC) → US-NOM03
- DevOps Agent → Daner Alejandro Salazar Colorado (UdeC) → US-NOM03

#### Scenario: Lead Dev Agent assigned to Natalia
- **WHEN** reading Lead Dev Agent section
- **THEN** the responsible person is Natalia Ceballos (UdeC)

#### Scenario: Oracle Agent assigned to Miguel
- **WHEN** reading Oracle Agent section
- **THEN** the responsible person is Miguel Coronado (UMB)

#### Scenario: Guardian Agent assigned to Daner
- **WHEN** reading Guardian Agent section
- **THEN** the responsible person is Daner Alejandro Salazar Colorado (UdeC)

#### Scenario: DevOps Agent assigned to Daner
- **WHEN** reading DevOps Agent section
- **THEN** the responsible person is Daner Alejandro Salazar Colorado (UdeC)

### Requirement: Each agent has a System Prompt
Every agent profile in AGENTS.md SHALL include a System Prompt with: role, purpose, responsibilities, and limits.

#### Scenario: Lead Dev Agent prompt includes R1-R5
- **WHEN** reading Lead Dev Agent System Prompt
- **THEN** it mentions engine.py implementation, R1 (25% diurnal), R2 (75% nocturnal), R3 (4%+4% deductions), R4 ($162K transport aid), R5 (validated exceptions)

#### Scenario: Oracle Agent prompt includes Gherkin format
- **WHEN** reading Oracle Agent System Prompt
- **THEN** it mentions casos_prueba.md with 10+ Gherkin scenarios (Dado/Cuando/Entonces)

#### Scenario: Guardian Agent prompt includes LangChain and Llama 3
- **WHEN** reading Guardian Agent System Prompt
- **THEN** it mentions LangChain framework, Llama 3 8B via Ollama, and Docker execution

#### Scenario: DevOps Agent prompt includes CI/CD pipeline
- **WHEN** reading DevOps Agent System Prompt
- **THEN** it mentions Dockerfile multi-stage and GitHub Actions CI

### Requirement: Guardian Agent emits veredicto.json with protocol
The AGENTS.md SHALL define the verification protocol for the Guardian Agent's JSON verdict output.

#### Scenario: Veredicto JSON schema is defined
- **WHEN** reading Guardian Agent section
- **THEN** it includes the JSON schema for veredicto.json with escenarios array, resumen object, and metadata object

#### Scenario: Veredicto includes pass/fail per scenario
- **WHEN** inspecting a veredicto.json file
- **THEN** each escenario entry has resultado field set to "PASS" or "FAIL"
