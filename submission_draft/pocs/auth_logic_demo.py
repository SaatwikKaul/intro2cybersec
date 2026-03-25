#!/usr/bin/env python3
"""
Demonstrates the credential logic equivalent to the APK:
- Registration appends lines.
- Login accepts any line that matches username+password.
This shows account-collision / parallel-password behavior.
"""

from __future__ import annotations


def check_credentials(file_content: str, username: str, password: str) -> bool:
    for line in file_content.splitlines():
        parts = line.split(" ")
        if len(parts) == 4 and parts[0] == "Username:" and parts[2] == "Password:":
            if username == parts[1].strip() and password == parts[3].strip():
                return True
    return False


def main() -> int:
    # Simulate two "registrations" for the same username with different passwords.
    content = ""
    content += "Username: alice Password: victimPass\n"
    content += "Username: alice Password: attackerPass\n"

    print("Credential file content:")
    print(content)

    print("Login alice/victimPass  ->", check_credentials(content, "alice", "victimPass"))
    print("Login alice/attackerPass->", check_credentials(content, "alice", "attackerPass"))
    print("Login alice/wrongPass   ->", check_credentials(content, "alice", "wrongPass"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
