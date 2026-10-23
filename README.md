# Software Security Assignment 1

This project is a small document system made for the Software Security course.

The system has three separate services:

- Application API
- Resource Service
- Processing Service

The services communicate with HTTP.

## Main functionality

The system supports:

- Login with JWT
- Normal user and admin role
- Create documents
- View own documents
- Export own documents
- Admin access
- Authorization between the services

The export flow uses all three services.

Application API sends the request to Processing Service.

Processing Service sends the request to Resource Service.

Resource Service checks the JWT and document owner before returning the document.

## Users

The test users are:

- omar, role user
- yamal, role user
- admin, role admin

The passwords are not stored directly in the code.

They are loaded from environment variables.

## Requirements

Python 3 is required.

Install the Python packages with:

```powershell
python -m pip install -r requirements.txt
```

Install the helper package with:

```powershell
python -m pip install -e helper_package
```

## Environment variables

The following environment variables are required:

```powershell
$env:JWT_SECRET="your-secret"
$env:OMAR_PASSWORD="your-password"
$env:YAMAL_PASSWORD="your-password"
$env:ADMIN_PASSWORD="your-password"
```

The real values are not stored in the repository.

## Run the services

Open three terminals.

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

## Run tests

Run all tests with:

```powershell
python -m pytest tests -v
```

The tests cover:

- Document ownership
- Admin authorization
- Input validation
- Path traversal protection
- Trust between services
- Export flow

## Security checks

Bandit is used for static security analysis.

Run:

```powershell
bandit -r application_api resource_service processing_service
```

pip-audit is used for dependency analysis.

Run:

```powershell
pip-audit -r requirements.txt
```

## Jenkins

The project includes a Jenkins pipeline.

The pipeline does the following:

1. Creates a Python virtual environment
2. Installs dependencies
3. Installs the helper package
4. Runs Bandit
5. Runs pip-audit
6. Starts the three services
7. Runs pytest
8. Saves reports as Jenkins artifacts

The pipeline uses Jenkins credentials for the JWT secret and test passwords.

The Jenkinsfile is located in the root of the repository.

## Branches

The repository has these main branches:

- main
- vulnerable-version
- fixed-version

`vulnerable-version` contains the intentionally vulnerable version.

`fixed-version` contains the fixes and the final security tests.

## Vulnerabilities

The project includes these intentionally planted vulnerabilities:

- CWE-20 Improper Input Validation
- CWE-862 Missing Authorization
- CWE-22 Path Traversal
- Service trust vulnerability between components

More information is in:

```text
docs/vulnerabilities.md
```

The initial security plan is in:

```text
docs/initial_security_plan.md
```

## Helper package

The project includes a small installed helper package used when documents are exported.

It is located in:

```text
helper_package/
```

The package formats document data before it is returned as an export.