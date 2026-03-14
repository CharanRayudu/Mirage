# Skill: File Upload Vulnerabilities

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- **NEVER** upload weaponized shells (e.g., functional PHP/JSP/ASP shells) that allow arbitrary command execution. Upload benign proofs-of-concept (e.g., returning `phpinfo()` or doing basic math like `echo 7*7;`) to demonstrate risk safely.
- Do not overwrite existing files, exceed storage quotas intentionally, or upload illegal/harmful content.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) detailing the upload request (multipart/form-data) and the server's response.
- Proof that the application parses or executes the uploaded file (e.g., successful rendering of an XSS payload in an SVG, or execution of a benign PHP scripts).
- Exact endpoint for the upload and the directory where the file is stored.

## Detection Heuristics
- Server accepts files with dangerous extensions (e.g., `.php`, `.jsp`, `.exe`, `.svg`, `.html`).
- Server relies purely on client-side MIME type or Extension validation rather than checking file contents.
- The uploaded file is accessible directly via a public URL and the server executes it instead of returning it as a static download or displaying it safely.

## Safe Test Procedure
1) Identify the file upload mechanism and the baseline behavior using valid inputs (e.g., uploading a benign `.jpg`).
2) Upload a benign payload file (e.g., an HTML file containing a simple JS alert `alert(1)`, or a PHP file with `echo 'SAFE_TEST';`).
3) Alter intermediate variables like the `Content-Type`, double extensions (e.g., `file.php.jpg`), or null byte injections (`file.php%00.jpg`) to bypass weak filters.
4) Attempt to navigate to the location of the uploaded file and verify if it is rendered or executed.
5) If suspicious, add a "Validator" task for safe confirmation.

## False-Positive Killers
- The server explicitly renames files to randomized non-executable extensions upon upload.
- The file is placed in an S3 bucket or isolated file store that does not parse server-side scripts.
- The server forces the `Content-Disposition: attachment` header, preventing inline script execution (XSS) in modern browsers.

## Remediation Guidance
- Ensure strict server-side validation checking the internal content/magic bytes instead of relying on the superficial extension or `Content-Type`.
- Enforce strict allowlists of permissible extensions (e.g., `.png`, `.jpg`).
- Strip EXIF data and re-encode images to neutralize embedded payloads.
- Store uploaded files outside the web root or on a dedicated remote file server (e.g., AWS S3).
- Implement restrictions preventing file execution in the upload directories.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Unrestricted File Upload on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <critical / high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
By uploading a malicious file, an attacker could potentially achieve Remote Code Execution (RCE) if the server processes the file, or Cross-Site Scripting (XSS) if the file is served inline to other users.

**Evidence:**
- <artifact path 1> — Shows the upload request bypassing restrictions by modifying the filename/content-type.
- <artifact path 2> — Shows the uploaded file being fetched and successfully interpreted or rendered by the server.

**Safe Reproduction Steps:**
1. Create a file named `payload.html` with basic HTML content.
2. Intercept the file upload request and change the `Content-Type` to `image/jpeg`.
3. Locate the file's final location (e.g., `/uploads/payload.html`).
4. Navigate to the uploaded file and observe that the file is interpreted as HTML.

**Suggested Fix:**
Only accept recognized file types using strict magic byte checks. Serve all uploaded content with a restrictive Content Security Policy (CSP), off the primary domain, and enforce the `Content-Disposition: attachment` header when files are fetched. Ensure the upload directory does not possess execution permissions.
```
