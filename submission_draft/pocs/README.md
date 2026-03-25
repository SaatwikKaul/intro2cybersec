# PoC Notes (Case 1 APK)

## Objective
Demonstrate why session token generation with `java.util.Random` is weak for security-sensitive use.

## Vulnerable code reference
- `Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java`
  - Token creation call: lines 174-177
  - Weak token generator: lines 183-189

## Reproducibility steps
1. Decompile APK with JADX:
   - `JAVA_OPTS='-Duser.home=/tmp/jadxhome' HOME=/tmp/jadxhome Assignment1/tools/jadx/bin/jadx -d Assignment1/decompiled Assignment1/a1_case1.apk`
2. Confirm vulnerable token generation:
   - `rg -n "generateSessionToken|new Random|sessionToken" Assignment1/decompiled/sources/com/example/mastg_test0016/Login.java`
3. Run deterministic PRNG demo:
   - `python3 Assignment1/submission_draft/pocs/token_generator_demo.py --seed 123456789 --count 3`

## Demo script purpose
`token_generator_demo.py` includes a Java `Random`-compatible implementation to show:
- Same seed => same token sequence (determinism)
- Why deterministic PRNGs are inappropriate for session tokens

`auth_logic_demo.py` mirrors the APK credential parser behavior to show:
- Duplicate registrations for the same username create multiple valid passwords.
- Login passes if any stored line matches, which enables account-collision style abuse.

Optional seeded-window demo (assumption-based):
- `python3 Assignment1/submission_draft/pocs/token_generator_demo.py --target <TOKEN> --start-seed <N> --end-seed <M>`
- This demonstrates how bounded seed search can recover candidate seeds if token seeding assumptions hold.

## Attack narrative linkage (for report)
1. Reverse engineer token algorithm and alphabet from APK.
2. Observe or capture token/timing in a realistic attacker model.
3. Reproduce candidate PRNG outputs.
4. Attempt token prediction/replay for session hijacking where token trust exists.

## Notes
- This app is a training sample and appears local-only; PoC illustrates cryptographic weakness in token generation design.
- The core grading focus is accurate vulnerability reasoning and threat-model clarity.
