# Task 3 Focus: Vulnerability Discovery, Explanation, and Fixes

This file is the focused writeup for the vulnerability part of the assignment. It is aligned to:
- Task 3 in the spec
- The rubric categories `Vulnerability Discovery & Explanation` and `Fix / Mitigation`

## What Task 3 Actually Needs

For full marks, your section needs to do four things clearly:

1. Explain how the vulnerability was found.
2. Record every value in the APK that is treated like a random value, code, token, or similar.
3. Assess whether the generator/pattern is appropriate for the security role.
4. Pick one core security-relevant weak usage and explain risk, attack path, and fix.

Important: the assignment is explicitly biased toward randomness and token generation. That means your core vulnerability should be the weak session token generation, even if other flaws are also serious.

## Discovery Method

We used static analysis after decompiling the APK with JADX.

### Tooling
- `jadx` to decompile the APK into Java source and XML resources
- `rg` to search for keywords such as `Random`, `token`, `session`, `nextInt`, `password`

### High-value search patterns
- `Random`
- `sessionToken`
- `createSession`
- `nextInt`
- `credentials.txt`

### Relevant evidence files
- [AndroidManifest.xml](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/resources/AndroidManifest.xml)
- [Login.java](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java)
- [MainActivity.java](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java)
- [Profile.java](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Profile.java)

## Random / Token / Code Inventory

This is the exact inventory Task 3 asks for.

| Location | Class / Method | Generator / Helper | Security Role | Assessment |
|---|---|---|---|---|
| `MainActivity.randomNumberGenerator()` | `MainActivity` / `randomNumberGenerator()` | `new Random().nextInt(100)` | UI/demo-only random value | Not security-sensitive |
| `Login.generateSessionToken()` | `Login` / `generateSessionToken()` | `new Random()` with `nextInt(62)` over alphanumeric alphabet | Session token / authentication state | Security-sensitive and weak |
| `Login.createSession()` | `Login` / `createSession()` | Stores generated token into `SharedPreferences` | Session persistence | Inherits weakness from insecure token generator |

## Top 3 Critical Vulnerabilities

These are the three strongest findings overall. Only the first one is the best choice for the Task 3 core vulnerability.

### 1. Predictable session token generation with `java.util.Random` (Core Vulnerability)

#### Evidence
- Token generation: [Login.java:183](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:183)
- Token creation and storage: [Login.java:174](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:174)

#### Why it is vulnerable
The app generates a session token using `java.util.Random`, which is not a cryptographically secure random number generator. Session tokens must be unpredictable because they act as authentication state. If a token generator is predictable, an attacker can reduce the search space, reproduce candidate outputs, or replay observed tokens.

#### Security role
This value is not cosmetic or UI-only. It is the session token used after successful login, so it directly affects authentication and session integrity.

#### Concrete attack scenario
1. The attacker decompiles the APK and reads the token generation logic.
2. The attacker learns the token format: 16 alphanumeric characters chosen with `Random.nextInt(62)`.
3. The attacker observes a login event or captures one token in a realistic threat model such as a rooted device, hooking framework, or compromised local environment.
4. The attacker reproduces candidate outputs from the deterministic PRNG.
5. The attacker uses the predicted or recovered token to impersonate a session.

#### Fix
Replace `java.util.Random` with `java.security.SecureRandom` and generate at least 128 bits of entropy.

#### Example fix
```java
import java.security.SecureRandom;
import java.util.Base64;

private static final SecureRandom SECURE_RANDOM = new SecureRandom();

private String generateSessionToken() {
    byte[] bytes = new byte[16];
    SECURE_RANDOM.nextBytes(bytes);
    return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
}
```

#### Why the fix works
`SecureRandom` is designed for security-sensitive unpredictability. A 128-bit random token is infeasible to guess in practice, unlike outputs derived from a predictable general-purpose PRNG.

### 2. Plaintext credential storage in `credentials.txt`

#### Evidence
- Credentials written directly to file: [MainActivity.java:59](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:59)
- Format written: [MainActivity.java:60](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:60)
- Credentials read back during login: [Login.java:77](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:77)

#### Why it is vulnerable
Usernames and passwords are stored in cleartext format. If an attacker gains local file access through device compromise, backup artifacts, malware, or debugging access, the credentials are immediately exposed.

#### Concrete attack scenario
1. The attacker gains local app-data access on a compromised or rooted device.
2. The attacker reads `credentials.txt`.
3. The attacker extracts valid usernames and passwords directly.
4. The attacker logs into the app as the victim.

#### Fix
Do not store raw passwords. Store salted password hashes instead.

#### Example fix direction
- Generate a unique salt per account.
- Hash the password with a slow password hashing algorithm.
- On Android, use a strong KDF such as PBKDF2 and store only `salt + hash`.

#### Why the fix works
Hashing prevents recovery of the original password from storage. A unique salt also prevents identical passwords from producing identical stored values.

### 3. Account-collision flaw from append-based registration and any-match login

#### Evidence
- Registration appends another credential line instead of replacing or checking uniqueness: [MainActivity.java:59](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:59)
- Login accepts any stored line that matches username and password: [Login.java:85](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:85)

#### Why it is vulnerable
The app does not enforce unique usernames. If the same username is registered multiple times with different passwords, every matching pair remains valid. This breaks account integrity because one logical identity can have multiple accepted passwords.

#### Concrete attack scenario
1. A victim already registered the username `alice`.
2. An attacker re-registers `alice` with a different password.
3. The app appends the attacker-controlled entry to `credentials.txt`.
4. During login, the app scans the file and accepts any matching line.
5. Both the victim's and attacker's passwords now work for the same username.

#### Fix
- Enforce unique usernames at registration time.
- Store users in a structured format keyed by username.
- Reject duplicate usernames or explicitly implement account update flows with re-authentication.

#### Why the fix works
Unique identity enforcement ensures one username maps to exactly one account state and one credential verifier.

## What You Should Submit For Task 3

If you want this section to score well, structure it like this:

### Part A: Discovery method
State that you decompiled the APK with JADX and searched the source for random and session-related values.

### Part B: Inventory table
Include the random/token inventory table above.

### Part C: Core vulnerability
Make Vulnerability 1 the main one:
- where generated
- why `Random` is unsuitable
- what the token is used for
- concrete attack path
- exact fix and why it works

### Part D: Secondary findings
Briefly mention Vulnerabilities 2 and 3 as additional weaknesses found during static analysis. They strengthen your overall technical depth, but they should not replace the weak randomness issue as the center of Task 3.

## Best Marking Strategy

If the goal is to maximize marks against the rubric:
- Use `Predictable session token generation` as the main Task 3 vulnerability.
- Use the inventory table to show you checked all random-like values in the APK.
- Mention plaintext credential storage and account-collision logic as secondary findings.
- Keep the mitigation concrete, technical, and directly tied to the insecure randomness issue.
