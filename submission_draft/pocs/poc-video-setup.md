# PoC Video Setup Plan

This file explains what is needed to create the required PoC videos and the fastest way to do it on this machine.

## Current machine status

At the moment this machine does **not** have:
- `adb`
- Android emulator
- `scrcpy`
- `ffmpeg`

It **does** have:
- `brew`
- Java
- the APK
- decompiled source and PoC scripts

## What is required to create the PoC video

To create a working PoC video for the assignment, I need two things:

1. **A way to run the APK**
   - Either a physical Android device with USB debugging enabled
   - Or an Android emulator installed locally

2. **A way to record the demonstration**
   - Either `scrcpy --record`
   - Or `adb shell screenrecord`
   - Or a desktop recorder such as `ffmpeg`

## Fastest practical path

The fastest and lowest-friction path is:

### Option A: Use a physical Android device

Requirements:
- Android phone
- USB cable
- Developer Options enabled
- USB debugging enabled

Tooling to install:
```bash
brew install android-platform-tools scrcpy ffmpeg
```

Verification:
```bash
adb devices
```

Install the APK:
```bash
adb install -r "/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/a1_case1.apk"
```

Record the video:
```bash
scrcpy --record "/Users/saatwik/Desktop/Uni Stuff/USYD Y2 S1/Intro to cyber /Assignment1/submission_draft/pocs/poc-demo.mp4"
```

## Slower path

### Option B: Install an Android emulator locally

Requirements:
- Android Studio or Android command-line emulator tools
- A downloadable Android system image

This path works, but it is much heavier because it requires:
- emulator installation
- device image download
- AVD creation
- boot time and configuration

## What I can demonstrate once the APK is running

### Minimum PoC video
1. Launch the app
2. Register a user
3. Log in successfully
4. Show that the app creates a session after login
5. Show the vulnerable code in `Login.generateSessionToken()`
6. Show the deterministic token-generation PoC script on the host machine

### Stronger PoC video
To show the vulnerability more convincingly, I would ideally also have:
- a rooted/emulated environment or instrumentation capability
- access to session storage or token values at runtime

That would allow a better demo of:
- token observation
- candidate reproduction
- session abuse attempt

Without instrumentation, we can still produce a valid PoC video by showing:
- the real app flow
- the exact vulnerable code
- the deterministic reproduction script
- the link between session creation and weak randomness

## Recommended recording script

Use this shot order:

1. Open the app on the device
2. Register a test account
3. Log in with that account
4. Pause and briefly show the vulnerable code location:
   - `Login.generateSessionToken()`
5. Run the PoC script on the laptop:
   - `token_generator_demo.py`
6. Explain why `java.util.Random` is inappropriate for session tokens
7. End with the secure fix using `SecureRandom`

## Best next step

If you can provide a physical Android device with USB debugging enabled, I can set up the tooling on this machine and produce the PoC video workflow from there. That is much faster than building a full emulator setup from scratch.
