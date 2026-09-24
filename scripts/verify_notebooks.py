#!/usr/bin/env python3
"""Exécute les notebooks du cours dans un noyau neuf et signale les erreurs."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


ROOT = Path(__file__).resolve().parents[1]


def discover(target: str | None) -> list[Path]:
    if target:
        day = target if target.startswith("jour_") else f"jour_{int(target):02d}"
        paths = list((ROOT / day).glob("*.ipynb"))
        paths += list((ROOT / "corrections" / day).glob("*.ipynb"))
    else:
        paths = []
        for day_number in range(1, 4):
            day = f"jour_{day_number:02d}"
            paths.extend((ROOT / day).glob("*.ipynb"))
            paths.extend((ROOT / "corrections" / day).glob("*.ipynb"))
    return sorted(paths)


def execute(path: Path, timeout: int) -> None:
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
    )
    client.execute()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", help="jour_01, jour_02 ou jour_03")
    parser.add_argument("--timeout", type=int, default=300, help="timeout par cellule en secondes")
    args = parser.parse_args()

    notebooks = discover(args.target)
    if not notebooks:
        print("Aucun notebook trouvé.")
        return 2

    failures: list[tuple[Path, str]] = []
    started = time.perf_counter()
    for position, path in enumerate(notebooks, start=1):
        relative = path.relative_to(ROOT)
        print(f"[{position:02d}/{len(notebooks):02d}] {relative}", flush=True)
        try:
            execute(path, args.timeout)
        except (CellExecutionError, Exception) as exc:  # rapport lisible pour un atelier
            failures.append((relative, str(exc)))
            print("  ECHEC", flush=True)
        else:
            print("  OK", flush=True)

    duration = time.perf_counter() - started
    print(f"\n{len(notebooks) - len(failures)}/{len(notebooks)} notebooks valides en {duration:.1f} s")
    if failures:
        for path, message in failures:
            print(f"\n--- {path} ---\n{message}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
