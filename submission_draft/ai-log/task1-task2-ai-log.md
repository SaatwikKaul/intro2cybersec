# AI Log for Task 1 and Task 2

## Task 1: Tool selection and decompilation setup

### Goal
Find a workable APK decompilation workflow and extract readable source and resources.

### Steps performed
1. Checked the local environment for APK analysis tools such as `jadx`, `apktool`, `aapt`, and Android SDK tools.
2. Confirmed those tools were not already installed.
3. Selected `jadx` as the main decompiler because it is well-suited to Java-level inspection of APKs.
4. Downloaded a portable `jadx` release into the assignment directory.
5. Decompressed the tool locally.
6. Ran `jadx` against `a1_case1.apk`.
7. Verified that decompiled output included:
   - `AndroidManifest.xml`
   - Java source for the app package
   - resource files such as layouts and strings

### Validation
- Confirmed package name from the manifest.
- Confirmed `MainActivity`, `Login`, and `Profile` classes were readable.
- Confirmed screenshot evidence could be produced from the decompiled source.

## Task 2: App understanding and system model

### Goal
Understand app behavior, identify assets, and build a simple system model.

### Steps performed
1. Read the manifest to identify entry points and activities.
2. Inspected `MainActivity` to understand registration and credential storage.
3. Inspected `Login` to understand credential checking and session creation.
4. Inspected `Profile` to understand logout behavior.
5. Read layouts and strings to confirm intended UI flow.
6. Built a simple system model capturing:
   - UI components
   - local storage
   - session storage
   - sensitive assets
   - data flows

### Runtime note
- No local Android emulator or `adb` was available in this environment.
- Task 2 was therefore completed using static analysis, which the spec allows if runtime execution is not possible.

## Outputs produced
- [task1-task2.md](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/submission_draft/task1-task2.md)
- [login_flow_snippet.png](/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/submission_draft/evidence/login_flow_snippet.png)
