# Non-functional Requirements

The security requirements in the initial security plan are the non-functional requirements for the project.

They were defined before feature implementation in `docs/initial_security_plan.md`.

The main non-functional requirements are:

- Protected endpoints must require a valid JWT.
- Normal users must only access their own documents.
- Privileged functionality must require the admin role.
- Services must not trust unsigned user identity information from another service.
- User input must be validated before it is used.
- Exported files must remain inside the intended export directory.
- JWT tokens must have a limited validity period.
- Dependencies must be declared and installed through the project dependency files.
- Functional and security tests must pass before a release is accepted.
- Static analysis and dependency analysis must pass before a release is accepted.

These requirements are mainly security and build requirements rather than user-visible functionality.