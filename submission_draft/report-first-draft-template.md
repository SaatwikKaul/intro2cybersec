# INFO5995 Assignment 1 First Draft Template

This is a report-shaped first draft for the final 2-page USENIX submission. It is intentionally centered on the one confirmed randomness-related vulnerability, because that is what the specification and rubric reward.

## Title
**Predictable Session Token Generation in an Android Authentication APK**

## Short Introduction
An APK, or Android Package Kit, is the file format used to distribute and install Android applications. Because an APK contains compiled bytecode rather than human-readable source, security auditing requires decompilation to recover the application logic, resources, and manifest. In this case study, we reverse engineered the provided APK to understand its authentication design and evaluate whether any security-sensitive values that appear random are generated safely. Our goal was to identify a validated randomness or cryptographic misuse issue that could affect session security.

`[TODO: add one sentence summarising AI assistance and point to the separate AI log]`

## App Overview
The application is a simple local authentication app. A user can register with a username and password, then log in using those stored credentials. On successful login, the app generates a session token and stores it locally before opening the profile screen. From static analysis, the app appears to rely entirely on local storage rather than a visible backend service.

## System and Threat Model
The system has three main code components: `MainActivity`, which handles registration; `Login`, which checks credentials and creates the session token; and `Profile`, which represents the post-login screen. Sensitive assets are the username and password stored in `credentials.txt`, and the session token stored in `SharedPreferences`. The key data flow is: registration writes credentials to local storage, login reads those credentials, a successful login generates a session token, and that token is then stored as the app's authentication state.

Our threat model focuses on an attacker who can reverse engineer the APK and inspect the client-side logic. A realistic stronger version of this attacker can also run the app on a rooted or emulated device and inspect local storage, memory, and logs. The attacker’s primary goal is to obtain, predict, replay, or forge a valid session token in order to impersonate a legitimate user session. This model directly matches the chosen vulnerability because the session token is generated on the client and trusted as authentication state.

`[TODO: optionally insert the system model figure here if space allows]`

## How the Vulnerability Was Found
We used static analysis after decompiling the APK with `jadx`. The manifest and app classes were inspected to identify the authentication flow, and targeted source searches were performed for terms such as `Random`, `sessionToken`, `createSession`, and `nextInt`. This process identified two random-like values in the app: a non-security demo value in `MainActivity.randomNumberGenerator()`, and a security-sensitive session token generated in `Login.generateSessionToken()`. Only the second one is relevant to authentication and therefore to assignment marking.

### Random-like value inventory

| Location | Generator / Helper | Security role | Assessment |
|---|---|---|---|
| `MainActivity.randomNumberGenerator()` | `new Random().nextInt(100)` | UI/demo-only value | Not security-sensitive |
| `Login.generateSessionToken()` | `new Random()` with `nextInt(62)` over an alphanumeric alphabet | Session token | Security-sensitive and weak |

## Vulnerability Details
The core vulnerability is in `Login.generateSessionToken()`, where the app generates its session token using `java.util.Random` at [Login.java:183](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:183). The generated token is then stored in `SharedPreferences` during session creation at [Login.java:174](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:174). This is weak because `java.util.Random` is a general-purpose deterministic PRNG rather than a cryptographically secure source of randomness. Session tokens must be unpredictable, since they are used as proof of authenticated state. If the generator is predictable, the attacker can reduce the difficulty of recovering valid session values.

In this system, the weakness matters because the session token is a protected asset and a core part of the login flow. The app assumes that the generated token is unique and hard to guess, but that trust assumption is false if the token comes from a predictable PRNG. The result is a direct link between the system model and the vulnerability: a weak randomness source undermines the integrity of the app’s authentication state.

## Exploitation Path
The attacker first decompiles the APK and locates `generateSessionToken()`. From the code, they learn that the token is 16 characters long and composed from an alphanumeric alphabet using `Random.nextInt(62)`. In a realistic stronger environment, such as a rooted or emulated device, the attacker can observe login timing and collect local clues about session creation. Because the generator is deterministic, the attacker can reproduce candidate outputs around the observed generation context. If the app accepts possession of the predicted token as valid session state, the attacker can attempt session hijacking or impersonation.

## Concrete Fix / Mitigation
The direct fix is to replace `java.util.Random` with `java.security.SecureRandom` and generate at least 128 bits of entropy for the session token. For example, the app can generate 16 random bytes with `SecureRandom` and encode them using URL-safe Base64. This works because `SecureRandom` is designed for security-sensitive unpredictability, unlike `java.util.Random`, which is deterministic and unsuitable for authentication tokens.

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

To reduce exposure further, the vulnerable version should no longer be distributed, and users should be pushed to an updated version containing the patched token generator. As a development-time control, static analysis tools and secure code review should flag the use of non-cryptographic randomness for session, token, or key material before release.

## Closing Sentence
In summary, APK analysis was necessary to recover the authentication logic and reveal that the app generates security-sensitive session tokens with `java.util.Random`. Because the session token is central to the app’s authentication state, replacing that generator with `SecureRandom` is the key mitigation needed to restore the intended security property.

## Notes for Final Editing
- Remove this section before submission.
- Keep the final report within 2 pages in the USENIX template.
- Put the AI interaction details in the separate `ai-log/` folder, not in the main report body.
- If space is tight, compress the random-value inventory table into one sentence.
- Do not include unrelated bugs such as duplicate registration or plaintext credential storage as main findings in the report body, because the current spec only marks randomness/cryptography issues.
