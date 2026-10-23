# Production Release

The current project is made for the assignment and local testing.

A production version would need more changes before it should be deployed.

## Password storage

The current users are seeded for testing.

A production system should store password hashes instead of test passwords.

Passwords should never be stored as plain text.

## Secret management

The JWT secret is currently provided through environment variables and Jenkins credentials.

In production, secrets should be stored in a dedicated secret management system and rotated when needed.

## HTTPS

The services currently communicate over local HTTP.

A production system should use HTTPS so tokens and data are protected while travelling between services.

## Database

Documents are currently stored in memory.

A production version should use a persistent database.

The database should also enforce access controls and use a restricted service account.

## Token handling

JWT tokens currently expire after one hour.

A production system should also consider:

- token revocation
- key rotation
- stronger session management
- logging of authentication failures

## Service access

The services currently run locally and can communicate directly.

In production, network rules should restrict which services can connect to each other.

Resource Service should only accept traffic from approved services or network locations.

## Error handling

The current system uses simple error responses.

A production system should have better error handling and should avoid exposing internal information.

## Logging and monitoring

Production services should have centralized logging and monitoring.

Security events such as failed logins, denied authorization requests and unusual activity should be recorded.

## Deployment

The Flask development server should not be used in production.

The services should run with a production application server and controlled configuration.

## CI/CD

The Jenkins pipeline should remain part of the release process.

A production release should only continue when:

- dependencies install correctly
- static analysis passes
- dependency analysis passes
- functional tests pass
- authorization tests pass