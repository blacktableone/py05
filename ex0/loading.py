#!/usr/bin/env python3

print("\nREAGENT STATUS: Loading reagents...")
print("\nChecking dependencies:")

all_present = True

try:
    import pandas
    print(f"[OK] pandas ({pandas.__version__}) - Data manipulation ready")
except ImportError:
    print("[MISSIING] pandas")
    print("	pip:	pip install pandas")
    print("	Poetry:	poetry add pandas")
    all_present = False


try:
    import numpy
    print(f"[OK] numpy ({numpy.__version__}) - Numerical computation ready")
except ImportError:
    print("[MISISING] numpy")
    print("	pip:	pip install numpy")
    print("	Poetry:	poetry add numpy")
    all_present = False


print()
print("pip vs Poetry:")
print(
    "requirements.txt declares what to install; "
    "pip resolves it at install time."
)
print("pyproject.toml declares the same constraints, and Poetry pins the")
print("resolved versions in poetry.lock so every install is identical.")

print()

if all_present:
    print("All reagents present and accounted for.")
else:
    print("Some reagents are missing.")
