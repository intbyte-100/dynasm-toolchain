import os
import subprocess
import argparse

from os.path import exists
from pathlib import Path

global miniluaPath
global minilua
global dynasm
global arch


def compile_minilua():
    print("[Task: minilua compilation]: started")
    process = subprocess.Popen(["gcc", "-o", "minilua", "-lm", "minilua.c"], cwd=miniluaPath)
    process.wait()
    if process.returncode != 0:
        print("[Task: minilua compilation]: failed")
        exit(1)
    print("[Task: minilua compilation]: finished")


def minilua_executable():
    if not exists(miniluaPath + "minilua"):
        print("[Info]: lua interpreter is required")
        compile_minilua()
    return miniluaPath + "minilua"


if __name__ == "__main__":
    src = []
    miniluaPath = os.getcwd() + "/minilua/"
    dynasm = os.getcwd() + "/dynasm/"

    parser = argparse.ArgumentParser(description="DynAsm toolchain v1.0.0")
    parser.add_argument("--arch", help="set specified arch")
    parser.add_argument("--dir", help="set source directory")
    parser.add_argument("files", type=str, nargs="*", help="source code files")

    args = parser.parse_args()
    arch = args.arch

    if args.dir is not None:
        src += list(Path(args.dir).rglob("*.[(dasm.c)(dasm.h]"))

    if args.files is not None:
        src += args.files


