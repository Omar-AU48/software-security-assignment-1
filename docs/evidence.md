# Evidence

This file collects the main evidence used for the assignment report.

## Initial security plan

Commit:

`d50919e` - first security plan

File:

`docs/initial_security_plan.md`

Evidence:

The plan was committed before the feature implementation and contains the requirements, assets, trust boundaries, access-control matrix, STRIDE analysis and security principles.

## Three services

Commit:

`4c69575` - basic services running

Files:

- `application_api/app.py`
- `resource_service/app.py`
- `processing_service/app.py`

Evidence:

The three Flask services run as separate processes and communicate through HTTP.

## Document authorization

Commit:

`4c119a5` - document access working

File:

`resource_service/app.py`

Test:

`tests/test_authorization.py`

Evidence:

The Resource Service checks the JWT and document owner before returning a document.

Omar can access his own document but cannot access Yamal's document.

## Document creation

Commit:

`781afd4` - document create working

Files:

- `application_api/app.py`
- `resource_service/app.py`

Evidence:

Authenticated users can create documents and the owner is taken from the JWT.

## CWE-20 fix

Commit:

`c8c37f3` - input validation fixed

File:

`resource_service/app.py`

Test:

`tests/test_input_validation.py`

Evidence:

Empty titles and invalid document input are rejected.

Screenshot:

`S11_input_validation_tests_pass.png`

## CWE-862 fix

Commit:

`cad0ac1` - authorization fixed

File:

`resource_service/app.py`

Test:

`tests/test_authorization.py`

Evidence:

Normal users cannot access admin-only functionality.

Screenshot:

`S10_authorization_tests_4_pass.png`

## CWE-22 fix

Commit:

`7d6f5db` - path traversal fixed

File:

`processing_service/app.py`

Test:

`tests/test_path_traversal.py`

Evidence:

The supplied filename cannot escape the exports directory.

Screenshot:

`S12_path_traversal_test_pass.png`

## Service trust fix

Commit:

`3d2e897` - service trust fixed

Files:

- `processing_service/app.py`
- `resource_service/app.py`

Test:

`tests/test_service_trust.py`

Evidence:

Processing Service forwards the signed JWT instead of sending an unsigned X-User identity.

The old internal X-User route is removed.

Screenshot:

`S13_service_trust_tests_pass.png`

## Automated security tests

Commit:

`f05af48` - security tests added

Tests:

- `tests/test_authorization.py`
- `tests/test_input_validation.py`
- `tests/test_path_traversal.py`
- `tests/test_service_trust.py`

Evidence:

All 9 tests pass.

Screenshots:

- `S14_all_tests_pass.png`
- `S19_all_tests_after_hardening.png`

## Static analysis

Commit:

`c17ae98` - security hardening and checks

Tool:

Bandit

Evidence:

Initial result:

- 5 Low
- 7 Medium
- 0 High

Final result:

- 0 Low
- 0 Medium
- 0 High

Screenshots:

- `S15_bandit_before_fix.png`
- `S17_bandit_after_timeout_fix.png`
- `S18_bandit_clean.png`

## Dependency analysis

Tool:

pip-audit

Evidence:

No known vulnerabilities were found in the project dependencies.

Screenshot:

`S16_pip_audit_clean.png`

## Jenkins pipeline

Commit:

`945fea3` - jenkins pipeline added

File:

`Jenkinsfile`

Evidence:

The pipeline performs setup, static analysis, dependency analysis, starts the services and runs automated tests.

Screenshots:

- `S23_jenkins_pipeline_success.png`
- `S24_jenkins_test_results.png`
- `S26_jenkins_final_artifacts.png`

## Fresh test environment

Commit:

`cbe3f52` - use fresh test environment

File:

`Jenkinsfile`

Evidence:

Jenkins deletes the previous `.venv` and creates a new virtual environment for the build.

Screenshot:

`S27_jenkins_fresh_environment.png`

## Automatic builds

Evidence:

The Jenkins Multibranch Pipeline detects changes to the fixed-version branch and pull requests.

Screenshots:

- `S28_multibranch_scan_success.png`
- `S29_jenkins_automatic_push_build.png`
- `S30_jenkins_pull_request_detected.png`
- `S31_jenkins_pull_request_success.png`

## Release gate

Commit:

`a4913c7` - define pipeline gates

Files:

- `Jenkinsfile`
- `docs/pipeline_gates.md`

Evidence:

The release gate is only reached after dependency installation, Bandit, pip-audit and automated tests pass.

Screenshot:

`S32_jenkins_release_gate_pass.png`

## Jenkins artifacts

The pipeline stores:

- `application_api.log`
- `resource_service.log`
- `processing_service.log`
- `bandit.txt`
- `pip-audit.txt`
- `pytest.txt`
- `pytest.xml`

Evidence:

`S26_jenkins_final_artifacts.png`