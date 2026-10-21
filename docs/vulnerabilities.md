# Vulnerabilities

## CWE-20 - Improper Input Validation

The document create function accepts input without properly checking it.

For example, a document can be created with an empty title.

Test:

```json
{
  "title": "",
  "content": "test"
}

## CWE-862 - Missing Authorization

The `/all-documents` endpoint returns all documents without checking who is making the request.

No token or role check is required.

Test:

A GET request was sent to:

`/all-documents`

without an Authorization header.

Result:

The service returned both Omar's and Yamal's documents.

This means protected data can be accessed without an authorization check.