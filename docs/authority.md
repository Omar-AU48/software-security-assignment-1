# Authority

The system uses JWT tokens to carry user identity and role between the services.

## Service

Application API creates the JWT after a successful login.

The token is then sent with requests to the other services in the Authorization header.

Resource Service does not trust the Processing Service to tell it who the user is.

Instead, Resource Service verifies the JWT itself before returning protected data.

## Resource

Each document has an owner.

The Resource Service compares the username from the JWT with the owner of the requested document.

A normal user can only access documents where the owner matches the user in the token.

For example:

- Omar can access document 1
- Omar cannot access document 2 because it belongs to Yamal

## Action

Different actions require different permissions.

Normal users can:

- create documents
- view their own documents
- export their own documents

Admin-only actions check that the JWT contains the admin role.

The `/admin` and `/all-documents` routes deny normal users with HTTP 403.

## Validity period

JWT tokens have an expiration time.

The Application API creates tokens with a validity period of one hour.

The token contains the `exp` field.

Services reject expired tokens and return HTTP 401.

This means a token cannot be used forever.

## Authority through the export flow

The export flow uses all three services.

1. The user sends a JWT to Application API.
2. Application API forwards the same Authorization header to Processing Service.
3. Processing Service forwards the same Authorization header to Resource Service.
4. Resource Service verifies the JWT.
5. Resource Service checks document ownership.
6. Only an authorized document is returned to Processing Service.
7. Processing Service creates the export.

The user identity is therefore not replaced by an unsigned internal header.

The same signed token is used across the workflow.

## Evidence

Relevant implementation:

- `application_api/app.py`
- `resource_service/app.py`
- `processing_service/app.py`

Relevant tests:

- `tests/test_authorization.py`
- `tests/test_service_trust.py`

The tests show that document ownership and role checks are enforced and that the old internal X-User trust route is no longer available.