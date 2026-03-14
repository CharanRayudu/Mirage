# Skill: Business Logic Vulnerabilities

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- **NEVER** manipulate financial balances on real-world accounts or production systems. Always use sandboxed environments (e.g., Stripe Test Mode) or explicitly authorized test financial profiles. Do not interact with actual payment gateways.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showcasing the unexpected sequential interaction or boundary manipulation.
- Output illustrating the broken state (e.g., an order generated with negative value, a multi-step wizard bypassed, conflicting object state).
- The exact API parameters, steps taken, and accounts utilized.

## Detection Heuristics
- An input field intended for positive integers (e.g., `quantity=1`) accepts a negative number (e.g., `quantity=-1`), causing the backend to deduct funds natively or create an underflow logic state.
- Force Browsing: Directly requesting 'Step 3' (e.g., `/checkout/confirm`) of a multi-step user interaction flow bypasses required prerequisites ('Step 2: `/checkout/payment`).
- The system checks business restrictions sequentially across separate endpoints, resulting in Race Conditions (e.g., applying a one-time-use coupon code concurrently).

## Safe Test Procedure
1) Establish a baseline interaction analyzing business workflow parameters (e.g., buying 1 item for $10).
2) To test Boundary manipulation: Inject negative values, massive numbers (Integer Overflow), decimals, or zero into quantity/transaction fields.
3) To test Workflow Bypasses: Initiate a transactional workflow, capture the HTTP requests for each step, and manually replay the concluding "success" step out-of-order.
4) To test Race Conditions (if authorized): Utilize `ffuf` or `Turbo Intruder` (or basic thread pools) to concurrently send 5-10 requests modifying the same state object.
5) If suspicious, add a "Validator" task for safe confirmation without breaking data models.

## False-Positive Killers
- The application evaluates negative integers contextually but rigorously applies type-casting or mathematical bounds-checking on the backend logic sink.
- The API explicitly enforces atomic transactional integrity preventing Time-Of-Check-To-Time-Of-Use (TOCTTOU) Race Conditions.
- Forced browsing redirects the user gracefully back to 'Step 1' because session flags indicate prerequisites were skipped.

## Remediation Guidance
- Enforce strict server-side state-machine validations across all multi-stage transactions. Do not rely entirely on the client or URL steps.
- Apply rigorous Type and Value boundary validations natively before processing mathematically sensitive inputs (e.g., currency, timestamps, quantities).
- Implement database atomicity, robust locking schemas, and dedicated transactional boundaries to eliminate Race Conditions.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Flawed Business Logic on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
Because of an intricate failure in the application's native business rules, an attacker can manipulate operational states (e.g., purchasing items with negative currencies or bypassing required checkout validations). This leads directly to substantial financial or operational loss.

**Evidence:**
- <artifact path 1> — Demonstrates the HTTP Request forcefully skipping preceding workflow steps or injecting unexpected business boundaries (e.g., `quantity=-5`).
- <artifact path 2> — Showcases the vulnerable backend response approving the transaction or permanently altering the application state improperly.

**Safe Reproduction Steps:**
1. Intercept an HTTP request to the `<endpoint>` responsible for concluding the transactional state.
2. Manipulate the mathematical constraints or submit the request prematurely out of standard sequential order.
3. Observe that the server's backend logic accepts the operation, generating an illogical and unauthorized state modification.

**Suggested Fix:**
Refactor the application code to explicitly validate contextual workflow prerequisites natively on the application server. Adopt robust server-side enforcement of basic data invariants, specifically ensuring quantities cannot be instantiated negatively, and transactions remain strictly atomic.
```
