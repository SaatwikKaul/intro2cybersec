# PoC Notes (Case 1 APK)

## Objective
Demonstrate, with executable evidence, that the app uses weak randomness for a security-sensitive session token and that the resulting authentication state is stored locally after login.

## Final deliverables
- `poc_01_app_register_login_profile.mp4`
  - Final app-execution PoC
  - Shows the original APK running unmodified
  - Flow shown: register `alice` / `pass123`, transition to the login screen, log in, and reach the protected `Profile` activity
- `poc_02_terminal_storage_and_code.mp4`
  - Final terminal/storage/code PoC
  - Shows plaintext `credentials.txt`
  - Shows `shared_prefs/SessionPrefs.xml` containing the generated session token
  - Shows the vulnerable `Login.generateSessionToken()` implementation using `new Random()`
  - Shows the included Java `Random` compatibility demo script
- `token_generator_demo.py`
  - Demonstrates deterministic token generation from a Java `Random`-compatible PRNG
- `terminal_poc_demo.sh`
  - Replays the terminal evidence sequence used in the terminal PoC video

## Important scope note
- The APK itself was not modified.
- The UI, strings, and app behavior shown in the videos come from the original provided APK: `Assignment1/a1_case1.apk`.
- Only the emulator environment, automation inputs, PoC scripts, and report materials were created locally.

## Vulnerable code reference
- File: `Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java`
- Token creation: lines 174-177
- Token retrieval: lines 179-181
- Weak token generator: lines 183-189

## Environment used
- Host OS: macOS
- Android SDK command-line tools
- Android Emulator
- `adb`
- `ffmpeg`
- Rooted Android emulator session for reading private app storage under `/data/data/com.example.mastg_test0016`

## Static analysis reproduction
1. Decompile the APK with JADX:
   - `JAVA_OPTS='-Duser.home=/tmp/jadxhome' HOME=/tmp/jadxhome Assignment1/tools/jadx/bin/jadx -d Assignment1/decompiled Assignment1/a1_case1.apk`
2. Confirm the package and activities from the manifest:
   - `sed -n '1,120p' Assignment1/decompiled/resources/AndroidManifest.xml`
3. Locate randomness- and token-related logic:
   - `rg -n "generateSessionToken|sessionToken|new Random|nextInt" Assignment1/decompiled/sources/com/example/mastg_test0016`
4. Inspect the vulnerable method directly:
   - `sed -n '174,190p' Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java`

## Reproducing the app behavior
1. Start an Android emulator.
2. Install the APK:
   - `adb install -r Assignment1/a1_case1.apk`
3. Launch the app:
   - `adb shell am start -n com.example.mastg_test0016/.MainActivity`
4. Register a test account in the app:
   - username: `alice`
   - password: `pass123`
5. Log in with the same credentials.
6. Confirm that the app reaches the protected `Profile` activity.

## Reproducing the stored-data evidence
This requires a rooted emulator or another environment where app-private storage is accessible.

1. Restart `adbd` as root:
   - `adb root`
2. Read the plaintext credential file:
   - `adb shell cat /data/data/com.example.mastg_test0016/files/credentials.txt`
3. Read the stored session preferences:
   - `adb shell cat /data/data/com.example.mastg_test0016/shared_prefs/SessionPrefs.xml`

Expected result:
- `credentials.txt` contains a line in the format `Username: <user> Password: <pass>`
- `SessionPrefs.xml` contains a `sessionToken` string generated at login

## Reproducing the deterministic PRNG demo
1. Run the included demo:
   - `python3 Assignment1/submission_draft/pocs/token_generator_demo.py --seed 12345 --count 3`
2. Observe that the output is deterministic for the same seed.
3. Optional bounded-search demonstration:
   - `python3 Assignment1/submission_draft/pocs/token_generator_demo.py --target <TOKEN> --start-seed <N> --end-seed <M>`

## Reproducing the videos
### Video 1: app execution
1. Clear prior app state:
   - `adb shell pm clear com.example.mastg_test0016`
2. Launch the app:
   - `adb shell am start -n com.example.mastg_test0016/.MainActivity`
3. Record the emulator screen:
   - `adb shell screenrecord --time-limit 28 /sdcard/poc_app_registration_login_v2.mp4`
4. While recording, perform:
   - registration with `alice` / `pass123`
   - login with `alice` / `pass123`
   - wait until the `Profile` screen is visible
5. Pull the result:
   - `adb pull /sdcard/poc_app_registration_login_v2.mp4`

### Video 2: terminal evidence
1. Ensure the emulator is running and the app has already been registered/logged in.
2. Run the provided terminal script:
   - `zsh Assignment1/submission_draft/pocs/terminal_poc_demo.sh`
3. Record the desktop while the script runs.
4. The script prints:
   - plaintext stored credentials
   - stored session token XML
   - vulnerable code snippet from `Login.java`
   - deterministic Java `Random` demo output

## What each PoC proves
- `poc_01_app_register_login_profile.mp4`
  - Proves the APK implements the local registration and session flow described in the report.
- `poc_02_terminal_storage_and_code.mp4`
  - Proves that credentials are stored in plaintext.
  - Proves that a session token is stored in app preferences after login.
  - Proves that the token-generation code uses `java.util.Random`.
- `token_generator_demo.py`
  - Proves the relevant PRNG family is deterministic and therefore unsuitable for security-sensitive token generation.

## Attack narrative linkage
1. Reverse engineer the APK and locate `generateSessionToken()`.
2. Confirm that the session token is security-relevant because it is created at login and stored for later session use.
3. In a rooted/emulated attacker environment, inspect the stored token and related app state.
4. Use knowledge of the token-generation algorithm to explain why the implementation is weak and why a secure generator such as `SecureRandom` is required.

## Working artifacts
These files are retained as intermediate artifacts from the recording process:
- `poc_app_registration_login.mp4`
- `poc_app_registration_login_v2.mp4`
- `poc_terminal_storage_and_code.mp4`
- `poc_terminal_storage_and_code_trimmed.mp4`
- `test-display-recording.mp4`
- `frames/`

The final submission-facing video files are:
- `poc_01_app_register_login_profile.mp4`
- `poc_02_terminal_storage_and_code.mp4`

## Notes
- This APK appears to be a local training sample rather than a production client/server app.
- The storage-inspection PoC relies on a rooted emulator; that maps directly to the threat model's rooted-device attacker capability.
- The report's primary marked vulnerability remains the weak use of `java.util.Random` for session-token generation.
