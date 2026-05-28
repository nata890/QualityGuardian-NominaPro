## ADDED Requirements

### Requirement: README.md SHALL document the full pipeline
The `README.md` SHALL describe the complete agent pipeline: Lead Dev → Oracle → Guardian → DevOps, including the role of each agent, the artifacts they produce, and the flow of data between them.

#### Scenario: Pipeline is documented
- **WHEN** reading README.md
- **THEN** all four agents (Lead Dev, Oracle, Guardian, DevOps) are described with their responsibilities

### Requirement: README.md SHALL include local execution instructions
The README SHALL provide step-by-step instructions for running the pipeline locally, including: installing dependencies, running the Guardian Agent, executing tests in Docker, and generating the verdict.

#### Scenario: Local execution steps are clear
- **WHEN** a new team member reads the README
- **THEN** they can run the full pipeline locally without asking questions

### Requirement: README.md SHALL document the .planning/ workflow
The README SHALL explain the DRAFT-to-production workflow via `.planning/` as defined in AGENTS.md Tool Access Policies.

#### Scenario: DRAFT workflow is explained
- **WHEN** reading the README
- **THEN** the process of writing to `.planning/` first and getting human approval is documented

### Requirement: README.md SHALL list project structure
The README SHALL include a tree view of the project directory structure with brief descriptions of each file and directory.

#### Scenario: Project structure is visible
- **WHEN** reading the README
- **THEN** a directory tree shows all key files and their purposes

### Requirement: README.md SHALL document environment setup
The README SHALL explain how to configure `OPENROUTER_API_KEY` via `.env` file and via GitHub Secrets for CI.

#### Scenario: API key setup is documented
- **WHEN** reading the README
- **THEN** instructions for both local (.env) and CI (GitHub Secrets) API key configuration are present
