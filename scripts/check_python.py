#!/usr/bin/env python3
"""Vérifie la version Python avant l'installation des dépendances du cours."""

from __future__ import annotations

import platform
import sys


REQUIRED = (3, 12)


def main() -> int:
    current = sys.version_info[:2]
    executable = sys.executable
    print(f"Python détecté : {platform.python_version()}")
    print(f"Exécutable      : {executable}")

    if current != REQUIRED:
        print(
            "\nERREUR : ce cours nécessite Python 3.12. "
            "Recréez .venv avec `py -3.12 -m venv .venv` sous Windows."
        )
        return 1

    print("Environnement compatible avec les dépendances du cours.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
