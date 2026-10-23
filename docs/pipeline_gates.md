# Pipeline Gates

A release is blocked if one of the following checks fails:

- Dependencies cannot be installed.
- Bandit reports a security issue.
- pip-audit finds a known vulnerable dependency.
- A functional or authorization test fails.

The Release gate stage is only reached if all previous stages pass.