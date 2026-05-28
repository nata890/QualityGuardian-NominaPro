## ADDED Requirements

### Requirement: Dockerfile SHALL NOT copy .env into the image
The `infra/Dockerfile` SHALL NOT contain any `COPY .env` or equivalent instruction. Secrets (OPENROUTER_API_KEY) SHALL be passed at runtime via `docker run -e`.

#### Scenario: No .env in Dockerfile
- **WHEN** scanning `infra/Dockerfile` for `COPY` instructions
- **THEN** no line matches `COPY .env` or `COPY *.env`

#### Scenario: API key passed at runtime
- **WHEN** running the container with `docker run -e OPENROUTER_API_KEY=xxx`
- **THEN** the application can access the key via `os.getenv("OPENROUTER_API_KEY")`

### Requirement: Dockerfile SHALL set read-only permissions for application files
The Dockerfile SHALL set file permissions to read-only (550 or more restrictive) for the `/app` directory. The non-root user SHALL NOT have write access to application code.

#### Scenario: Files are read-only
- **WHEN** the container runs as the `guardian` user
- **THEN** the user cannot modify files in `/app`

### Requirement: Dockerfile SHALL maintain multi-stage build
The Dockerfile SHALL continue to use multi-stage build (builder + runtime stages) to minimize image size and avoid including build tools in the final image.

#### Scenario: Final image has no build tools
- **WHEN** inspecting the runtime stage
- **THEN** pip and build dependencies from the builder stage are not present as executables
