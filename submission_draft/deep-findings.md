# Deep Vulnerability Findings (Extended Hunt)

This file captures additional issues found after an intensive static review of `a1_case1.apk`.

## F1 - Weak session token generation with `java.util.Random` (Primary)
- Severity: High
- Evidence:
  - [Login.java:183](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:183) to [Login.java:189](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:189)
- Why it matters:
  - `java.util.Random` is deterministic and not cryptographically secure for auth/session tokens.

## F2 - Plaintext credential storage in app file
- Severity: High (rooted/compromised-device threat model), Medium otherwise
- Evidence:
  - [MainActivity.java:59](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:59) to [MainActivity.java:60](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:60)
- Why it matters:
  - Username/password are written in clear format (`Username: ... Password: ...`) with no hashing/encryption.

## F3 - Account collision / parallel-password flaw (append + any-match)
- Severity: High
- Evidence:
  - Registration appends without uniqueness check: [MainActivity.java:59](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:59)
  - Login accepts any matching line: [Login.java:85](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:85) to [Login.java:104](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:104)
- Why it matters:
  - A second registration of the same username with a different password creates another valid credential entry.
  - This breaks account integrity and allows takeover-style behavior in shared data scenarios.

## F4 - Session token is generated but not enforced for authorization
- Severity: Medium
- Evidence:
  - Token generated/stored: [Login.java:174](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:174) to [Login.java:177](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:177)
  - Getter exists but no usage in app code: [Login.java:179](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:179)
  - Profile activity has no session validation logic before rendering: [Profile.java:22](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Profile.java:22) to [Profile.java:41](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Profile.java:41)
- Why it matters:
  - The token mechanism is effectively unused for access control, weakening the intended authentication boundary.

## F5 - Session token stored in plaintext `SharedPreferences`
- Severity: Medium (rooted/compromised-device model)
- Evidence:
  - [Login.java:175](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:175)
- Why it matters:
  - Session token confidentiality relies only on platform app sandbox; no encryption-at-rest is used.

## F6 - Authentication outcome logged to logcat
- Severity: Low
- Evidence:
  - [Login.java:53](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:53)
- Why it matters:
  - Login success/failure signals in logs can leak behavior to local observers in debugging/compromised contexts.

---

## Notes on confidence
- High confidence: F1, F2, F3 (directly observable and reproducible from code behavior).
- Medium confidence: F4, F5 (context-dependent exploitability, but valid security design weaknesses).
- Lower impact: F6 (informational leakage, not direct auth break).
