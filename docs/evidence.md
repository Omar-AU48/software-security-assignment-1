# Evidence

This file lists the main evidence used for the assignment and report.

All commit references below are taken from the project Git history.

## Initial security plan

Commit:

`d50919e` - first security plan

File:

`docs/initial_security_plan.md`

Evidence:

The initial security plan was committed before feature implementation.

It contains the planned requirements, assets, trust boundaries, access-control matrix, STRIDE analysis, security principles, tests and lifecycle activities.

## Three separate components

Commit:

`4c69575` - basic services running

Files:

- `application_api/app.py`
- `resource_service/app.py`
- `processing_service/app.py`

Evidence:

The project contains three separate Flask services running as separate processes.

The services communicate through HTTP.

## Communication between services

Commit:

`bcdaa96` - services can communicate

Evidence:

The services were connected through HTTP before the main functionality was implemented.

## Authentication

Commits:

- `11ee96f` - basic login working
- `8a49676` - jwt login working

File:

`application_api/app.py`

Evidence:

Users authenticate through Application API.

After successful authentication, Application API creates a signed JWT containing the user identity, role and expiration time.

## Admin authorization

Commit:

`d00ca00` - admin access working

Files:

- `application_api/app.py`
- `resource_service/app.py`

Test:

`tests/test_authorization.py`

Evidence:

The system distinguishes between the normal `user` role and the privileged `admin` role.

Normal users are denied access to admin-only functionality.

## Document access

Commit:

`4c119a5` - document access working

File:

`resource_service/app.py`

Test:

`tests/test_authorization.py`

Evidence:

Resource Service checks document ownership before returning a protected document.

Omar can access his own document and cannot access Yamal's document.

Screenshots:

- `S09_authorization_tests_pass.png`
- `S10_authorization_tests_4_pass.png`

## Document creation

Commits:

- `781afd4` - document create working
- `7f40c9f` - document create through api working

Files:

- `application_api/app.py`
- `resource_service/app.py`

Evidence:

Authenticated users can create documents through the Application API.

The owner is derived from the authenticated user rather than being trusted from arbitrary user input.

## Application API document flow

Commit:

`6dcbd8e` - documents through api working

Evidence:

Document requests can be sent through Application API to Resource Service.

## Three-component export functionality

Commit:

`cd4cbd9` - export flow working

Files:

- `application_api/app.py`
- `processing_service/app.py`
- `resource_service/app.py`

Evidence:

The export functionality involves all three application components.

The flow is:

User → Application API → Processing Service → Resource Service → Processing Service → Application API → User.

## Helper package

Commit:

`c873c1a` - helper package working

Files:

- `helper_package/pyproject.toml`
- `helper_package/export_helper/__init__.py`
- `helper_package/export_helper/formatter.py`

Evidence:

The project contains the installable `export-helper` package.

It is installed using:

`python -m pip install -e helper_package`

Processing Service uses the package when creating exports.

---

# Planted Vulnerabilities

## CWE-20 Improper Input Validation

Vulnerable commit:

`862917d` - first vulnerability documented

Fixed commit:

`c8c37f3` - input validation fixed

Relevant file:

`resource_service/app.py`

Test:

`tests/test_input_validation.py`

Evidence:

Invalid document input such as an empty title is rejected in the fixed version.

Screenshot:

`S11_input_validation_tests_pass.png`

## CWE-862 Missing Authorization

Vulnerable commit:

`676c03f` - missing authorization added

Fixed commit:

`cad0ac1` - authorization fixed

Relevant file:

`resource_service/app.py`

Test:

`tests/test_authorization.py`

Evidence:

The vulnerable version allowed access without the required authorization check.

The fixed version requires the appropriate authorization.

Screenshot:

`S10_authorization_tests_4_pass.png`

## CWE-22 Path Traversal

Vulnerable commit:

`15864d1` - path traversal added

Fixed commit:

`7d6f5db` - path traversal fixed

Relevant file:

`processing_service/app.py`

Test:

`tests/test_path_traversal.py`

Evidence:

The vulnerable implementation allowed an export filename to escape the intended export directory.

The fixed implementation prevents this behavior.

Screenshot:

`S12_path_traversal_test_pass.png`

## Composition Vulnerability

Vulnerable commit:

`6644dfe` - composition vulnerability added

Fixed commit:

`3d2e897` - service trust fixed

Relevant files:

- `processing_service/app.py`
- `resource_service/app.py`

Test:

`tests/test_service_trust.py`

Evidence:

The vulnerable design trusted an unsigned `X-User` identity passed between services.

The fixed design forwards the signed JWT instead.

Resource Service verifies the JWT and performs its own ownership check.

The old internal X-User route is removed.

Screenshot:

`S13_service_trust_tests_pass.png`

---

# Automated Tests

Commit:

`f05af48` - security tests added

Test files:

- `tests/test_authorization.py`
- `tests/test_input_validation.py`
- `tests/test_path_traversal.py`
- `tests/test_service_trust.py`

Evidence:

The test suite contains nine automated tests covering functional behavior and security guarantees.

Screenshots:

- `S14_all_tests_pass.png`
- `S19_all_tests_after_hardening.png`

---

# Security Hardening

Commit:

`c17ae98` - security hardening and checks

Evidence:

Security-sensitive configuration such as the JWT secret and test passwords was moved out of the source code and into environment variables or Jenkins credentials.

## Static analysis

Tool:

Bandit

Evidence:

Bandit identified issues during development.

After security hardening, the final Bandit scan completed without reported security issues.

Screenshots:

- `S15_bandit_before_fix.png`
- `S17_bandit_after_timeout_fix.png`
- `S18_bandit_clean.png`

## Dependency analysis

Tool:

pip-audit

Evidence:

The final dependency analysis reports no known vulnerabilities in the declared dependencies.

Screenshot:

`S16_pip_audit_clean.png`

---

# Jenkins CI/CD

## Initial Jenkins pipeline

Commit:

`945fea3` - jenkins pipeline added

File:

`Jenkinsfile`

Evidence:

The pipeline validates the project, runs static analysis, runs dependency analysis, starts the services and runs automated tests.

The Jenkins setup was corrected during development with:

- `157c96b` - fix jenkins python setup
- `3954656` - fix jenkins service wait
- `a804e98` - save pip audit result

Development evidence:

- `S20_jenkins_python_not_found.png`
- `S21_jenkins_build_failed.png`
- `S22_jenkins_timeout_failure.png`

Successful pipeline evidence:

- `S23_jenkins_pipeline_success.png`
- `S24_jenkins_test_results.png`
- `S25_jenkins_artifacts.png`
- `S26_jenkins_final_artifacts.png`

## Fresh test environment

Commit:

`cbe3f52` - use fresh test environment

File:

`Jenkinsfile`

Evidence:

The pipeline removes the previous virtual environment and creates a fresh `.venv` before installing the project dependencies.

Screenshot:

`S27_jenkins_fresh_environment.png`

## Automatic push builds

Commit used to trigger evidence:

`85adbb2` - update readme ci

Evidence:

The Jenkins Multibranch Pipeline automatically detected the change to `fixed-version` and started a new build.

Screenshots:

- `S28_multibranch_scan_success.png`
- `S29_jenkins_automatic_push_build.png`

## Pull request builds

Commit:

`224d25a` - test pull request

Branch:

`pr-test`

Evidence:

Jenkins detected the pull request and automatically ran the pipeline for it.

Screenshots:

- `S30_jenkins_pull_request_detected.png`
- `S31_jenkins_pull_request_success.png`

## Release gate

Commit:

`a4913c7` - define pipeline gates

Files:

- `Jenkinsfile`
- `docs/pipeline_gates.md`

Evidence:

The pipeline only reaches the Release gate after the build setup, Bandit analysis, dependency analysis and automated tests have completed successfully.

The pipeline is configured so that failure in a required earlier stage prevents the release gate from being reached.

Screenshot:

`S32_jenkins_release_gate_pass.png`

## Reproducible dependencies

Commit:

`76a5eaa` - pin dependencies

File:

`requirements.txt`

Evidence:

The direct Python dependencies used by the project are pinned to specific versions.

A Jenkins build completed successfully after the dependencies were pinned.

---

# Required Documentation

## README

Commit:

`e76c4b0` - complete readme

File:

`README.md`

Evidence:

The README contains the project purpose and instructions to build, seed, run and test the application.

## Secure design principles

Commit:

`b8df75c` - document security design

File:

`docs/security_design.md`

Evidence:

The document describes:

- Least Privilege
- Complete Mediation
- Fail-Safe Defaults

For each principle it describes the design decision, implementation and evidence.

## Authority

Commit:

`4cbbeb6` - document authority flow

File:

`docs/authority.md`

Evidence:

The document explains how JWT authority is bound to:

- service
- resource
- action
- validity period

## Production release

Commit:

`d1c78b2` - document production release

File:

`docs/production_release.md`

Evidence:

The document describes what would need to change before the system should be used in production.

## Architecture and non-functional requirements

Commit:

`7f5a128` - complete architecture requirements

Files:

- `docs/architecture.md`
- `docs/non_functional_requirements.md`

Evidence:

The repository contains an explicit architecture description, data flows, component responsibilities, trust boundaries and non-functional security requirements.

The original requirements and threat model remain documented in:

`docs/initial_security_plan.md`

---

# Branches and Git History

The repository keeps the full development history.

Important branches are:

## main

Contains the project state before the intentional vulnerability work.

## vulnerable-version

Contains the intentionally planted vulnerabilities.

Current vulnerable branch commit:

`6644dfe` - composition vulnerability added

## fixed-version

Contains the corrected implementation, automated tests, security checks, Jenkins pipeline and final project documentation.

This is the current final development branch.

## pr-test

Temporary branch used to demonstrate automatic Jenkins pull request execution.

Commit:

`224d25a` - test pull request

---

# Screenshot Evidence

The verified screenshot evidence currently consists of:

- `S09_authorization_tests_pass.png`
- `S10_authorization_tests_4_pass.png`
- `S11_input_validation_tests_pass.png`
- `S12_path_traversal_test_pass.png`
- `S13_service_trust_tests_pass.png`
- `S14_all_tests_pass.png`
- `S15_bandit_before_fix.png`
- `S16_pip_audit_clean.png`
- `S17_bandit_after_timeout_fix.png`
- `S18_bandit_clean.png`
- `S19_all_tests_after_hardening.png`
- `S20_jenkins_python_not_found.png`
- `S21_jenkins_build_failed.png`
- `S22_jenkins_timeout_failure.png`
- `S23_jenkins_pipeline_success.png`
- `S24_jenkins_test_results.png`
- `S25_jenkins_artifacts.png`
- `S26_jenkins_final_artifacts.png`
- `S27_jenkins_fresh_environment.png`
- `S28_multibranch_scan_success.png`
- `S29_jenkins_automatic_push_build.png`
- `S30_jenkins_pull_request_detected.png`
- `S31_jenkins_pull_request_success.png`
- `S32_jenkins_release_gate_pass.png`

The screenshots are kept separately from the repository and can be used as figures or appendix evidence in the final report.