# Skill: Prototype Pollution (JavaScript/Node.js)

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- **DANGER:** Prototype pollution on a backend Node.js server can globally degrade state, causing denial of service or RCE across all user sessions. Use extreme caution and only test non-destructive, isolated properties like `{"__proto__":{"x_testProperty":"test"}}`. Do NOT overwrite core object methods like `toString` or application-critical configuration keys.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showing the JSON or URL-encoded payload modifying `__proto__`, `constructor`, or `prototype`.
- Proof of pollution: a subsequent request (or the current one) that reflects or reacts to the newly injected property across isolated scopes.
- Specific sink/source mechanism identified (e.g., `merge()`, `clone()`, JSON parsing API).

## Detection Heuristics
- Injecting `{"__proto__": {"polluted": true}}` into a JSON body causes a completely unrelated endpoint or another user's session to reflect the `polluted` property.
- Passing `?__proto__[test_key]=test_value` in URL parameters results in global modification of Object attributes.
- Fuzzed properties unexpectedly alter the application's control flow, bypass authentication logic, or break JSON responses system-wide.

## Safe Test Procedure
1) Establish a baseline for a JSON endpoint or URL parameter mechanism expected to merge or deep-clone data (e.g., config updates, generic POST endpoints).
2) Inject a harmless distinct property: `{"__proto__": {"mirage_test_prop": 1}}` or `?constructor[prototype][mirage_test_prop]=1`.
3) Check if `mirage_test_prop` is accessible globally or reflected in subsequent unrelated requests.
4) If suspected on the client-side (DOM), check if `Object.prototype.mirage_test_prop` evaluates to `1` in the browser console.
5) If suspicious, add a "Validator" task for safe confirmation. **Shut down further fuzzing to prevent DoS.**

## False-Positive Killers
- The application strips `__proto__` entirely from JSON parsing.
- The runtime uses `Object.create(null)` for Dictionaries, structurally defusing prototype chain pollution.
- The pollution is strictly local to the instantiated object, and `Object.prototype` remains untouched globally.

## Remediation Guidance
- Utilize `Object.create(null)` instead of `{}` when creating dictionaries or objects meant to store arbitrary user input.
- Securely implement object assignment. Do not recursively merge keys named `__proto__`, `constructor`, or `prototype`.
- Freeze the prototype via `Object.freeze(Object.prototype)` early in the Node.js bootstrap process.
- Map user input explicitly using validation schemas (like Zod, Joi) to discard unauthorized nested object maps.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Prototype Pollution on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
An attacker can manipulate JavaScript's global `Object.prototype`, which injects properties into all objects across the application. Relying on affected properties downstream can lead to critical authorization bypasses, Cross-Site Scripting (XSS), or severe Remote Code Execution (RCE) on Node.js backends.

**Evidence:**
- <artifact path 1> — Demonstrates the HTTP Request passing the nested JSON payload `{"__proto__": {"mirage_safetest": "1"}}`.
- <artifact path 2> — Showcases a secondary, unrelated HTTP response reflecting the `mirage_safetest` value as if it was a native object attribute, confirming global pollution.

**Safe Reproduction Steps:**
1. Send an HTTP POST request to `<endpoint>` injecting `{"__proto__": {"mirage_safetest": "1"}}` into the payload.
2. Send a regular, unrelated HTTP GET request to another application endpoint.
3. Observe that the property `mirage_safetest` is unexpectedly serialized and returned in the second response, demonstrating a compromised object prototype inheritance chain.

**Suggested Fix:**
Filter and discard object keys matching `__proto__`, `constructor`, and `prototype` in all recursive merge, clone, or assignment functions. Instantiating data maps with `Object.create(null)` serves as a strong defense against prototype manipulation.
```
