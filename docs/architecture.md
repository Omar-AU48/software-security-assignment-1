# Architecture

The application uses a multi-tier architecture with three separate Python Flask services.

Each component runs as its own process and communicates through HTTP.

## Application API

Port: `5000`

Responsibilities:

- authenticate users
- create JWT tokens
- receive user requests
- enforce admin access for API-level privileged actions
- forward document requests to Resource Service
- start the export workflow through Processing Service

The Application API establishes the initial user identity after login.

## Resource Service

Port: `5001`

Responsibilities:

- own the protected document data
- verify JWT tokens
- enforce document ownership
- enforce admin authorization
- create documents

Resource Service is the final authority for document access.

A request is not accepted only because it came from another internal service.

## Processing Service

Port: `5002`

Responsibilities:

- receive export requests
- forward the user's Authorization header to Resource Service
- receive an authorized document
- use the external helper package
- create and save exports

Processing Service does not decide document ownership.

## External helper package

The project contains the installable package:

`helper_package/export_helper`

It is installed using:

`python -m pip install -e helper_package`

Processing Service uses it to format document exports.

## Main data flows

### Login

1. User sends username and password to Application API.
2. Application API verifies the credentials.
3. Application API returns a signed JWT containing the user identity, role and expiration time.

### Read document

1. User sends a JWT and document ID to Application API.
2. Application API forwards the request and Authorization header to Resource Service.
3. Resource Service verifies the JWT.
4. Resource Service compares the JWT subject with the document owner.
5. The document is returned only if the authorization check passes.

### Export document

This functionality involves all three application components.

1. User sends an export request and JWT to Application API.
2. Application API forwards the request to Processing Service.
3. Processing Service forwards the same Authorization header to Resource Service.
4. Resource Service verifies the token and document ownership.
5. Resource Service returns the authorized document.
6. Processing Service uses `export-helper` to format the document.
7. The result is returned through Application API to the user.

## Trust boundaries

The main trust boundaries are:

- User to Application API
- Application API to Resource Service
- Application API to Processing Service
- Processing Service to Resource Service
- Processing Service to the helper package

A service-to-service request is not automatically trusted.

Authorization is based on the signed JWT and the checks performed by the service that owns the protected resource.

## Protected resources

The main protected resources are:

- user identity
- user role
- JWT tokens
- documents
- document ownership
- exported files

## Access control

Normal users can:

- log in
- access their own profile
- create documents
- read their own documents
- export their own documents

Normal users cannot:

- read another user's documents
- perform admin-only operations

Admin users can perform the privileged admin operations defined by the application.

The complete access-control matrix and STRIDE threat model are documented in:

`docs/initial_security_plan.md`