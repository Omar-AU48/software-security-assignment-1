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