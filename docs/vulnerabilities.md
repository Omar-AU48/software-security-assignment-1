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
```

Result:

The document was created successfully even though the title was empty.

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

## CWE-22 - Path Traversal

The export function lets the user choose the filename without checking the path.

A normal filename such as `omar.txt` is saved inside the exports folder.

Test:

```json
{
  "filename": "../outside.txt"
}
```

Result:

The service accepted the filename and returned:

`exports\../outside.txt`

The `..` can move the file outside the intended exports folder.