# Task 4: System and Threat Model Linked to the Chosen Vulnerability

This Task 4 writeup is intentionally centered on the chosen Task 3 vulnerability:

- **Core vulnerability:** predictable session token generation with `java.util.Random` in `Login.generateSessionToken()`
- Evidence: [Login.java:183](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:183)

For marking, this is the strongest way to present Task 4 because the rubric wants the system model, assets, attacker, and capabilities explicitly linked to the chosen vulnerability.

## System Model

### Main components
- **`MainActivity`**
  - Registration screen
  - Collects username and password from the user
  - Writes credentials to `credentials.txt`
  - Evidence: [MainActivity.java:34](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:34), [MainActivity.java:59](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/MainActivity.java:59)

- **`Login`**
  - Reads credentials from `credentials.txt`
  - Verifies the username/password pair
  - Generates a session token after successful login
  - Stores the token in `SharedPreferences`
  - Evidence: [Login.java:77](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:77), [Login.java:174](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:174), [Login.java:183](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:183)

- **`Profile`**
  - Post-login screen
  - Clears the stored session token on logout
  - Evidence: [Profile.java:32](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Profile.java:32), [Profile.java:49](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Profile.java:49)

- **`credentials.txt`**
  - Local file in app-private storage
  - Stores registered usernames and passwords

- **`SharedPreferences`**
  - Stores the session token under `SessionPrefs`
  - Evidence: [Login.java:44](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:44), [Login.java:175](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:175)

### Important assets
- User credentials
- Session token
- Authentication state
- Contents of app-private storage

### Data flows
1. **Registration flow**
   - User enters username and password in `MainActivity`
   - App writes them into `credentials.txt`

2. **Login flow**
   - User enters credentials in `Login`
   - App reads `credentials.txt`
   - If a matching line is found, login succeeds
   - App generates a session token
   - App stores that token in `SharedPreferences`

3. **Session flow**
   - Successful login transitions the user to `Profile`
   - Logout clears the stored token from `SharedPreferences`

### Operational assumptions
- The app assumes the Android sandbox protects local storage from unauthorized access.
- The app assumes the contents of `credentials.txt` and `SharedPreferences` have not been tampered with.
- The app assumes the generated session token is unpredictable and cannot be guessed or reproduced.
- The app assumes that possession of a valid token corresponds to a legitimate authenticated session.

## Threat Model

### Primary attacker
- **External technical attacker**
  - Can decompile the APK and inspect the login/session logic
  - Can understand how the token is generated and stored

### Realistic supporting attacker environments
- **Rooted or emulated device attacker**
  - Can inspect app-private storage, memory, and logs
  - Can observe login timing and session state locally

- **Physical attacker with device access**
  - Can attempt local extraction of stored data if device protections are weak or bypassed

The strongest attacker model for this case is the **reverse engineer plus rooted-device observer**, because that directly matches the session-token weakness in the code.

### Attacker capabilities linked to the chosen vulnerability
- Reverse engineer the APK and inspect `generateSessionToken()`
- Learn the exact token format and alphabet
- Observe when login occurs
- Reproduce candidate outputs from the deterministic PRNG
- Read or capture stored session state in a compromised local environment
- Attempt replay or impersonation using predicted or stolen token values

### Attacker goals linked to the chosen vulnerability
- Predict or recover a valid session token
- Impersonate a legitimate logged-in user
- Bypass the intended protection of the authenticated session

## Why the Chosen Vulnerability Matters in This System

The system depends on the session token as the app's post-login authentication state. That token is generated in [Login.java:183](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:183) and stored in [Login.java:175](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java:175). Because the token is security-sensitive, it must be unpredictable. However, the implementation uses `java.util.Random`, which is deterministic and not suitable for session authentication.

That means the main trust assumption of the session design is false: the app behaves as if the token is hard to guess, but the code generates it with a weak PRNG. Once the attacker knows the algorithm and can narrow the generation context, the attack becomes a token prediction or token recovery problem rather than a true secret-guessing problem.

## Step-by-Step Attack Scenario

1. The attacker decompiles the APK and identifies `Login.generateSessionToken()`.
2. The attacker confirms that the token is 16 characters long and built from an alphanumeric alphabet using `Random.nextInt(62)`.
3. The attacker observes or estimates when the victim logged in.
4. In a rooted, emulated, or otherwise compromised local environment, the attacker collects timing, storage, or runtime clues about session creation.
5. The attacker generates candidate token outputs from the same deterministic PRNG behavior.
6. If the app trusts possession of that token as session state, the attacker can attempt session hijacking or impersonation.

## Short Task 4 Version for the Report

The app has three main components: `MainActivity`, `Login`, and `Profile`. Sensitive assets are the user's credentials and the session token, both of which are stored locally on the device. The key data flow is login: the app reads `credentials.txt`, authenticates the user, generates a session token in `Login.generateSessionToken()`, and stores that token in `SharedPreferences`.

The chosen attacker is a reverse engineer who can inspect the APK and, in a realistic stronger variant, run the app on a rooted or emulated device. This attacker can learn the exact token-generation algorithm, observe when logins occur, and inspect local session state. That directly links to the chosen vulnerability: the session token is generated with `java.util.Random`, which is deterministic and unsuitable for authentication. As a result, an attacker may predict or recover candidate session tokens and use them to impersonate a legitimate user session.

## Connection to the Other Task 3 Findings

These are not the center of Task 4, but the same model also supports them:

- **Plaintext credential storage**
  - The rooted-device attacker can inspect `credentials.txt` and recover usernames and passwords directly.

- **Account-collision registration flaw**
  - The attacker can abuse the registration flow in `MainActivity` because identities are stored as append-only text records rather than as unique user accounts.

For marking, keep those two as supporting findings and keep the session token weakness as the main Task 4 focus.
