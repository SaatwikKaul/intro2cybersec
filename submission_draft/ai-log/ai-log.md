# AI Usage Log (Assignment 1 Case 1)

Date: 2026-03-05  
Task: APK reverse engineering and vulnerability identification for `a1_case1.apk`

## Entry 1: Tooling selection and setup
- Prompt summary: identify decompilation toolchain and setup steps for this environment.
- AI-assisted actions:
  - Checked for existing tools (`jadx`, `apktool`, `aapt`) and confirmed missing binaries.
  - Downloaded portable JADX release and unpacked locally in `Assignment1/tools/jadx`.
  - Executed JADX CLI to decompile APK into `Assignment1/decompiled`.
- Validation:
  - Confirmed output directories `sources/` and `resources/`.
  - Confirmed manifest and app classes were readable.

## Entry 2: Static analysis for model and assets
- Prompt summary: extract package/activity information and identify auth/session components.
- AI-assisted actions:
  - Parsed `AndroidManifest.xml` for package name and entrypoint activity.
  - Located app classes in `com/example/mastg_test0016/`.
  - Reviewed `MainActivity`, `Login`, and `Profile` for registration/login/session behavior.
- Validation:
  - Cross-checked resource layouts and strings against class behavior.
  - Confirmed app flow: register -> login -> session creation -> profile -> logout.

## Entry 3: Vulnerability discovery (randomness focus)
- Prompt summary: locate random-like values and assess security relevance.
- AI-assisted actions:
  - Searched decompiled sources for `Random`, `token`, `session`, `nextInt`.
  - Built random-value inventory table (security vs non-security uses).
  - Identified core weakness: `Login.generateSessionToken()` uses `java.util.Random`.
- Validation:
  - Verified code location and usage path:
    - Token generation in `Login.java` lines 183-189.
    - Token persistence in `Login.java` lines 174-177.

## Entry 4: Mitigation and report drafting
- Prompt summary: propose technically sound mitigation and map findings to rubric.
- AI-assisted actions:
  - Drafted fix with `SecureRandom` and 128-bit token entropy.
  - Drafted threat model and attack scenario centered on predictability risk.
  - Produced report draft and PoC documentation aligned to rubric sections.
- Validation:
  - Checked rubric coverage:
    - System/threat model, vulnerability explanation, mitigation.
    - Evidence references to concrete file locations/lines.

## References used
- Local files:
  - `Assignment1/assignment1-spec-1.pdf`
  - `Assignment1/assignment1-rubric-1.pdf`
  - Decompiled output under `Assignment1/decompiled/`
- Tools:
  - JADX CLI (`v1.5.5` portable release)
