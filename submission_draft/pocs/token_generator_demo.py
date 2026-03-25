#!/usr/bin/env python3
"""
Educational PoC for INFO5995 Assignment 1.

Shows deterministic token generation behavior using a Java Random-compatible PRNG.
This demonstrates why non-cryptographic PRNGs are unsuitable for session tokens.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
TOKEN_LEN = 16


@dataclass
class JavaRandom:
    """Minimal java.util.Random-compatible generator."""

    seed: int

    _MULTIPLIER = 0x5DEECE66D
    _ADDEND = 0xB
    _MASK = (1 << 48) - 1

    def __post_init__(self) -> None:
        self.seed = (self.seed ^ self._MULTIPLIER) & self._MASK

    def _next(self, bits: int) -> int:
        self.seed = (self.seed * self._MULTIPLIER + self._ADDEND) & self._MASK
        return self.seed >> (48 - bits)

    def next_int(self, bound: int) -> int:
        if bound <= 0:
            raise ValueError("bound must be > 0")
        if (bound & (bound - 1)) == 0:
            return (bound * self._next(31)) >> 31
        while True:
            bits = self._next(31)
            value = bits % bound
            if bits - value + (bound - 1) >= 0:
                return value


def generate_token_from_seed(seed: int) -> str:
    rng = JavaRandom(seed)
    chars = []
    for _ in range(TOKEN_LEN):
        chars.append(ALPHABET[rng.next_int(len(ALPHABET))])
    return "".join(chars)


def generate_sequence(seed: int, count: int) -> list[str]:
    out = []
    current_seed = seed
    for _ in range(count):
        out.append(generate_token_from_seed(current_seed))
        current_seed += 1
    return out


def brute_force_seed(target: str, start_seed: int, end_seed: int) -> list[int]:
    matches: list[int] = []
    for seed in range(start_seed, end_seed + 1):
        if generate_token_from_seed(seed) == target:
            matches.append(seed)
    return matches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Java Random session-token determinism demo"
    )
    parser.add_argument("--seed", type=int, help="Seed used for token generation demo")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of sequential demo tokens to print (default: 1)",
    )
    parser.add_argument(
        "--target",
        type=str,
        help="Target token to brute-force in a seed window (optional)",
    )
    parser.add_argument(
        "--start-seed",
        type=int,
        help="Start of brute-force seed window (inclusive)",
    )
    parser.add_argument(
        "--end-seed",
        type=int,
        help="End of brute-force seed window (inclusive)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.target is not None:
        if args.start_seed is None or args.end_seed is None:
            raise SystemExit("--target requires --start-seed and --end-seed")
        matches = brute_force_seed(args.target, args.start_seed, args.end_seed)
        if matches:
            print("Match seeds:", ", ".join(str(s) for s in matches))
        else:
            print("No matching seed in the provided window.")
        return 0

    if args.seed is None:
        raise SystemExit("Provide --seed for generation mode or --target for brute-force mode.")

    tokens = generate_sequence(args.seed, args.count)
    for i, token in enumerate(tokens, start=1):
        print(f"{i}: seed={args.seed + i - 1} token={token}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
