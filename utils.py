import traceback
import os
from pathlib import Path

def aex(want, got, prefix=""):
    if got != want:
        print(f"{prefix}got {got}, expected {want}")


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        lineno = list(traceback.walk_stack(None))[0][1]
        aex(want, got, prefix=f"{lineno}: {f.__qualname__} ")

def splitlines(lines: str) -> list[str]:
    return [line.strip() for line in lines.split("\n")]

def read_input(filename: str, relative_file: str) -> list[str]:
    relative_filepath = Path(relative_file).parent
    with open(relative_filepath / filename) as infile:
        return [line.strip() for line in infile.readlines()]
