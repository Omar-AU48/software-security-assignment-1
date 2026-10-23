# Software Security Assignment 1

This project is a small document system made for the Software Security course.

The system has three separate services:

- Application API
- Resource Service
- Processing Service

The services communicate through HTTP.

## Main functionality

The system supports:

- Login with JWT
- Normal user and admin role
- Create documents
- View own documents
- Export own documents
- Admin-only access
- Authorization between services

The export flow uses all three services.

Application API sends the request to Processing Service.

Processing Service sends the request to Resource Service.

Resource Service checks the JWT and document owner before returning the document.

## Architecture

The three services have different responsibilities.

### Application API

Runs on port `5000`.

Responsibilities:

- Login
- Create JWT tokens
- Receive requests from users
- Check admin access
- Forward document requests
- Start the export flow

### Resource Service

Runs on port `5001`.

Responsibilities:

- Store documents
- Check JWT tokens
- Check document ownership
- Check admin authorization
- Create documents

### Processing Service

Runs on port `5002`.

Responsibilities:

- Request authorized documents from Resource Service
- Use the helper package
- Create document exports
- Save exports safely

## Users and roles

The system has two roles:

- `user`
- `admin`

The seeded users are:

- `omar` with role `user`
- `yamal` with role `user`
- `admin` with role `admin`

Omar and Yamal are used to test that one normal user cannot access another user's documents.

The passwords are loaded from environment variables and are not stored directly in the source code.

## Seed data

The project uses in-memory data, so no database setup is required.

The following documents are created automatically when Resource Service starts:

- Document 1 belongs to Omar
- Document 2 belongs to Yamal

The users are also loaded automatically when Application API starts.

Before starting the services, set the required environment variables in PowerShell:

```powershell
$env:JWT_SECRET="omarassignmentkey123456789012345"
$env:OMAR_PASSWORD="omar123"
$env:YAMAL_PASSWORD="yamal123"
$env:ADMIN_PASSWORD="admin123"
```

This is the seed setup used for local testing.

## Requirements

Python 3 is required.

The project has been tested with Python 3.14.

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

Install the helper package:

```powershell
python -m pip install -e helper_package
```

The project uses these pinned dependencies:

- Flask 3.1.3
- requests 2.34.2
- PyJWT 2.15.1
- pytest 9.1.1
- Bandit 1.9.4
- pip-audit 2.10.1

## Run the application

Set the environment variables first:

```powershell
$env:JWT_SECRET="omarassignmentkey123456789012345"
$env:OMAR_PASSWORD="omar123"
$env:YAMAL_PASSWORD="yamal123"
$env:ADMIN_PASSWORD="admin123"
```

Open three PowerShell terminals.

Start Resource Service:

```powershell
python resource_service/app.py
```

Start Processing Service:

```powershell
python processing_service/app.py
```

Start Application API:

```powershell
python application_api/app.py
```

The services run on:

```text
Application API: http://127.0.0.1:5000
Resource Service: http://127.0.0.1:5001
Processing Service: http://127.0.0.1:5002
```

## Test login

Example login request in PowerShell:

```powershell
$body = @{
    username = "omar"
    password = "omar123"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response
```

The response contains a JWT token.

## Run automated tests

Make sure all three services are running.

Run:

```powershell
python -m pytest tests -v
```

The automated tests cover:

- Omar can access his own document
- Omar cannot access Yamal's document
- Normal user cannot access admin functionality
- Admin can access admin functionality
- Empty document title is rejected
- Valid document can be created
- Path traversal is blocked
- Export flow works
- The old trusted internal user header route is removed

## Static security analysis

Bandit is used for static security analysis.

Run:

```powershell
python -m bandit -r application_api resource_service processing_service
```

The fixed version currently passes without Bandit findings.

## Dependency analysis

pip-audit is used to check the Python dependencies for known vulnerabilities.

Run:

```powershell
python -m pip_audit -r requirements.txt
```

The fixed version currently reports no known vulnerable dependencies.

## Helper package

The project includes an installable helper package:

```text
helper_package/
```

The package is called:

```text
export-helper
```

It is installed with:

```powershell
python -m pip install -e helper_package
```

Processing Service uses the package when creating document exports.

## Vulnerabilities

The project contains three intentionally planted vulnerabilities from the course catalog:

- CWE-20 Improper Input Validation
- CWE-862 Missing Authorization
- CWE-22 Path Traversal

It also contains one composition vulnerability involving trust between services.

The vulnerable behavior is documented in:

```text
docs/vulnerabilities.md
```

The vulnerable code is kept in the branch:

```text
vulnerable-version
```

The corrected implementation is kept in:

```text
fixed-version
```

## Security design

The project uses these three secure design principles:

- Least Privilege
- Complete Mediation
- Fail-Safe Defaults

The initial security and lifecycle plan is located in:

```text
docs/initial_security_plan.md
```

The pipeline gate rules are located in:

```text
docs/pipeline_gates.md
```

## Jenkins pipeline

The project includes a `Jenkinsfile`.

Jenkins creates a fresh Python virtual environment for every build.

The pipeline:

1. Deletes the old virtual environment
2. Creates a new virtual environment
3. Installs the pinned dependencies
4. Installs the helper package
5. Runs Bandit
6. Runs pip-audit
7. Starts the three services
8. Runs the automated tests
9. Runs the release gate
10. Saves reports and logs as Jenkins artifacts

The Jenkins credentials used by the pipeline are:

```text
jwt-secret
omar-password
yamal-password
admin-password
```

The secret values are stored in Jenkins and not in the repository.

## Pipeline gates

A release is blocked if:

- Dependencies cannot be installed
- Bandit reports a security issue
- pip-audit finds a known vulnerable dependency
- A functional or authorization test fails

The Release gate stage is only reached if all previous stages pass.

## Jenkins branches and pull requests

The repository is connected to a Jenkins Multibranch Pipeline.

Jenkins scans the repository automatically.

It detects:

- New commits on branches
- Pull requests

The `fixed-version` branch contains the Jenkinsfile and is automatically built when changes are detected.

Pull requests are also detected and tested automatically before they are merged.

## Jenkins artifacts

Jenkins saves the following build artifacts:

```text
application_api.log
bandit.txt
pip-audit.txt
processing_service.log
pytest.txt
pytest.xml
resource_service.log
```

These files provide evidence from the security checks, tests and running services.

## Repository branches

The main project branches are:

### main

Original development branch.

### vulnerable-version

Contains the intentionally planted vulnerabilities.

### fixed-version

Contains the fixed vulnerabilities, automated tests, security checks, Jenkins pipeline and final project documentation.

## Documentation

The main project documentation is located in:

```text
docs/
```

Files include:

```text
initial_security_plan.md
vulnerabilities.md
pipeline_gates.md
```

## Build commands

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Install helper package:

```powershell
python -m pip install -e helper_package
```

## Seed commands

Set the test user passwords and JWT secret:

```powershell
$env:JWT_SECRET="omarassignmentkey123456789012345"
$env:OMAR_PASSWORD="omar123"
$env:YAMAL_PASSWORD="yamal123"
$env:ADMIN_PASSWORD="admin123"
```

The users and initial documents are created automatically when the services start.

## Run commands

Resource Service:

```powershell
python resource_service/app.py
```

Processing Service:

```powershell
python processing_service/app.py
```

Application API:

```powershell
python application_api/app.py
```

## Test command

Run all automated tests:

```powershell
python -m pytest tests -v
```