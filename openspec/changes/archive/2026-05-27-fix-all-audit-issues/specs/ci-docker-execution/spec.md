## ADDED Requirements

### Requirement: CI SHALL build and run tests inside Docker container
The GitHub Actions workflow (`.github/workflows/ci.yml`) SHALL build the Docker image from `infra/Dockerfile` and execute all tests inside the container using `docker run`. Direct installation of Python dependencies on the runner SHALL NOT be used for test execution.

#### Scenario: CI builds Docker image
- **WHEN** the CI workflow runs on a push to main
- **THEN** the Docker image is built from `infra/Dockerfile`

#### Scenario: CI runs tests in container
- **WHEN** the CI workflow reaches the test execution step
- **THEN** tests are executed via `docker run` with the built image, not via `python -m pytest` directly on the runner

### Requirement: CI SHALL extract veredicto.json from container
After test execution, the CI SHALL extract `veredicto.json` and `reporte_junit.xml` from the container using `docker cp` and upload them as GitHub Actions artifacts.

#### Scenario: veredicto.json is extracted
- **WHEN** tests complete inside the container
- **THEN** `veredicto.json` is copied out and uploaded as an artifact

### Requirement: CI SHALL run container in read-only mode
The `docker run` command SHALL use `--read-only` flag to prevent the container from writing to the host filesystem, ensuring test isolation as required by AGENTS.md.

#### Scenario: Container runs read-only
- **WHEN** the CI executes tests
- **THEN** the `docker run` command includes `--read-only` flag
