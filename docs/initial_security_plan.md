# Initial Security Plan

## 1. Purpose

The system is a small document workspace where users can create, view and export their own private documents.

The system is split into three separate parts:

1. Application API
2. Resource Service
3. Processing Service

The goal is to make the application work and then test how security can fail between the different parts of the system.

## 2. Functional Requirements

FR1: A user can log in to the system.

FR2: A normal user can create a document.

FR3: A normal user can view their own documents.

FR4: A user can request an export of their own documents.

FR5: An admin user can perform a restricted admin action.

FR6: The export function must use all three services.

## 3. Security Requirements

SR1: A user must not be able to view another user's documents.

SR2: Only the admin user can use the restricted admin function.

SR3: Each service must check the permissions that are relevant to the resources it handles.

SR4: If a user's identity or permission cannot be verified, access must be denied.

SR5: The processing service must only access the data needed for the requested export.

SR6: User input must be checked before it is used in security-sensitive operations.

## 4. Users and Roles

The system has two roles:

### Normal User
A normal user can:
- Log in
- Create documents
- View their own documents
- Request an export of their own documents

### Admin
An admin can:
- Log in
- View their own documents
- Use the restricted admin function

Seeded users:

- omar - normal user
- yamal - normal user
- admin - admin user

## 5. Access Control Matrix

| Action | Normal User | Admin |
|---|---|---|
| Log in | Yes | Yes |
| Create own document | Yes | Yes |
| View own document | Yes | Yes |
| View another user's document | No | No |
| Request export of own documents | Yes | Yes |
| Use restricted admin function | No | Yes |

## 6. Assets

The main assets in the system are:

- User accounts
- User documents
- Exported documents
- User identity and role information
- Authentication information

## 7. Components and Responsibilities

### Application API

The Application API is the entry point for the user.

Its main responsibilities are:

- Handle login
- Identify the current user
- Receive requests from the user
- Send requests to the other services
- Check whether the user is allowed to perform the requested action

### Resource Service

The Resource Service owns the users' documents and exported results.

Its main responsibilities are:

- Store documents
- Return documents
- Store export results
- Check whether the requester is allowed to access a specific resource

### Processing Service

The Processing Service handles export jobs.

Its main responsibilities are:

- Receive export requests
- Ask the Resource Service for the required documents
- Use the helper package to create the export
- Send the result back to the Resource Service

## 8. Data Flow

### Create and view document

1. The user sends a request to the Application API.
2. The Application API identifies the user and sends the request to the Resource Service.
3. The Resource Service checks if the user is allowed to access the document.
4. The Resource Service creates or returns the document.
5. The result is returned to the user through the Application API.

### Export document

1. The user requests an export through the Application API.
2. The Application API identifies the user and sends the export request to the Processing Service.
3. The Processing Service asks the Resource Service for the documents needed for the export.
4. The Resource Service checks whether the user is allowed to access the requested documents.
5. The Processing Service uses the helper package to create the export.
6. The export is saved through the Resource Service.
7. The result is returned to the user through the Application API.

## 9. Trust Boundaries

The system has several trust boundaries where data or authority moves between different parts of the system.

### User to Application API

The Application API must not trust input from the user automatically.

It must check:
- Who the user is
- Whether the request is valid
- Whether the user is allowed to perform the requested action

### Application API to Resource Service

The Resource Service must not assume that every request from the Application API is automatically allowed.

It must still check whether the user is allowed to access the requested resource.

### Application API to Processing Service

The Processing Service should only receive the information needed for the requested job.

It should not get more access than necessary.

### Processing Service to Resource Service

The Resource Service must check which user's data the Processing Service is requesting.

The Processing Service must not be able to access documents belonging to another user without permission.

## 10. STRIDE Analysis

### Spoofing

A user could try to pretend to be another user.

Control:
The Application API must authenticate the user before access is given.

### Tampering

A user could try to change a document or request that they are not allowed to change.

Control:
The Resource Service must check ownership and permissions before changing protected resources.

### Repudiation

A user could deny that they performed an important action.

Control:
Important actions should be logged with the user identity and action performed.

### Information Disclosure

A user could try to read another user's private documents.

Control:
The Resource Service must check authorization before returning documents.

### Denial of Service

A user could send many requests and make the services unavailable.

Control:
The system should reject invalid requests and avoid unnecessary processing.

### Elevation of Privilege

A normal user could try to use an admin function.

Control:
The system must check the user's role before allowing restricted admin actions.

## 11. Security Design Principles

The system will use the following security design principles:

### Least Privilege

Each service should only have the permissions needed for its own job.

For example, the Processing Service should only access the documents needed for the requested export.

### Fail Safe

If the system cannot verify a user's identity or permission, access must be denied.

### Complete Mediation

Access to protected resources must be checked every time they are requested.

The system must not assume that a request is allowed just because it came from another internal service.

## 12. Planned Tests and Evidence

The following tests will be used as evidence during development:

- Test that a normal user can log in.
- Test that a user can create and view their own document.
- Test that Omar cannot access Yamal's document.
- Test that a normal user cannot use the admin function.
- Test that an export only includes documents the user is allowed to access.
- Test that invalid or missing authorization is denied.
- Test that security fixes prevent the planted vulnerabilities.

Test results, logs and pipeline results will be saved as evidence.