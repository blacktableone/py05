#!/usr/bin/env python3
"""Oracle: reads the Matrix configuration from the environment."""

import os
import sys

try:
    from dotenv import load_dotenv
    HAS_DOTENV: bool = True
except ImportError:
    HAS_DOTENV = False

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
ENV_PATH: str = os.path.join(BASE_DIR, ".env")
GITIGNORE_PATH: str = os.path.join(BASE_DIR, ".gitignore")
VALID_MODES: tuple[str, ...] = ("development", "production")
VALID_LEVELS: tuple[str, ...] = (
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
)


def env_ignored_by_git() -> bool:
    """Return True if .env is listed in ex1/.gitignore."""
    if not os.path.exists(GITIGNORE_PATH):
        return False
    with open(GITIGNORE_PATH, "r", encoding="utf-8") as file:
        return ".env" in [line.strip() for line in file]


def no_hardcoded_secret(api_key: str) -> bool:
    """Return True if the real API key is not written in this file."""
    if not api_key:
        return True
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as file:
        return api_key not in file.read()


def main() -> int:
    """Run the Oracle and return an exit code."""
    if HAS_DOTENV:
        # override=False: real environment variables win over .env
        load_dotenv(ENV_PATH, override=False)

    mode: str = os.getenv("MATRIX_MODE", "").strip()
    database_url: str = os.getenv("DATABASE_URL", "").strip()
    api_key: str = os.getenv("API_KEY", "").strip()
    log_level: str = os.getenv("LOG_LEVEL", "").strip().upper()
    zion_endpoint: str = os.getenv("ZION_ENDPOINT", "").strip()

    missing: list[str] = []
    warnings: list[str] = []

    if not HAS_DOTENV:
        warnings.append("python-dotenv is not installed, .env ignored")
    if mode not in VALID_MODES:
        warnings.append(f"Invalid or missing MATRIX_MODE: '{mode}'")
        mode = "development"
    production: bool = mode == "production"
    if log_level not in VALID_LEVELS:
        default_level = "WARNING" if production else "DEBUG"
        warnings.append(f"Invalid or missing LOG_LEVEL, using {default_level}")
        log_level = default_level

    print("ORACLE STATUS: Consulting the configuration...")
    print("\nConfiguration loaded:")
    print(f"Mode: {mode}")

    if not database_url:
        print("Database: Not configured")
        missing.append("DATABASE_URL")
    elif "localhost" in database_url or database_url.startswith("sqlite"):
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to remote instance")

    if api_key:
        print("API Access: Authenticated")
    else:
        print("API Access: Not configured")
        missing.append("API_KEY")

    print(f"Log Level: {log_level}")

    if zion_endpoint:
        print("Remote Network: Online")
    else:
        print("Remote Network: Offline")
        missing.append("ZION_ENDPOINT")

    if missing or warnings:
        print("\nConfiguration warnings:")
        for message in warnings:
            print(f"[WARNING] {message}")
        for name in missing:
            print(f"[WARNING] Missing {name}")

    print("\nConfiguration security check:")
    if no_hardcoded_secret(api_key):
        print("[OK] No hardcoded secrets detected")
    else:
        print("[FAIL] Secret found in source code!")
    if env_ignored_by_git():
        print("[OK] .env file properly ignored by git")
    else:
        print("[WARNING] Add .env to .gitignore")
    print("[OK] Production overrides available")

    # The visible difference between development and production
    print()
    if production:
        print("Production mode: Debugging details are hidden.")
        if missing:
            print("PRODUCTION ERROR: required settings are missing.")
            return 1
    else:
        print("Development mode: Detailed debugging is enabled.")
        print(f"[DEBUG] Database URL: {database_url or 'none'}")
        print(f"[DEBUG] Zion endpoint: {zion_endpoint or 'none'}")

    print("\nThe Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
