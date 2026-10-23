# Security Design

The project uses three secure design principles from the course:

- Least Privilege
- Complete Mediation
- Fail-Safe Defaults

## Least Privilege

### Design decision

Each service should only do the work it needs to do.

The Application API handles login and user requests.

The Resource Service owns the documents and decides if a user is allowed to access them.

The Processing Service only processes documents that it receives through an authorized request.

### Implementation

The Processing Service does not decide document ownership itself.

It forwards the same Authorization header to the Resource Service.

The Resource Service checks the JWT and document owner before returning the document.

This means the Processing Service cannot access a document just because it knows the document ID.

### Evidence

The export test shows that Omar can export his own document.

The authorization tests show that Omar cannot access Yamal's document.

Relevant tests:

`tests/test_authorization.py`

`tests/test_service_trust.py`

## Complete Mediation

### Design decision

Access to protected documents should be checked every time a document is requested.

A previous successful login should not automatically give access to every document.

### Implementation

The Resource Service checks the JWT for every protected document request.

It also checks that the user in the token matches the owner of the requested document.

Admin access also checks the role in the JWT before access is allowed.

### Evidence

The authorization tests check that Omar can access document 1 but gets HTTP 403 when trying to access Yamal's document 2.

The admin tests also check that a normal user gets HTTP 403 while the admin user is allowed.

Relevant test:

`tests/test_authorization.py`

## Fail-Safe Defaults

### Design decision

If the system cannot verify the user or permission, access should be denied.

Access should only be allowed after the required checks pass.

### Implementation

Protected routes return HTTP 401 if the Authorization header is missing or the token is invalid.

They return HTTP 403 if the user is authenticated but does not have permission for the requested action.

The Resource Service does not return a protected document until the JWT and ownership checks have passed.

### Evidence

The tests show that unauthorized document access is rejected.

The old internal route that trusted the X-User header was removed from the fixed version.

The test confirms that this route now returns HTTP 404.

Relevant tests:

`tests/test_authorization.py`

`tests/test_service_trust.py`