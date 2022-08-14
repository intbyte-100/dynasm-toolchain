import os
import subprocess
import argparse

from os.path import exists
from pathlib import Path

global miniluaPath
global minilua
global dynasm
global arch


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def compile_minilua():
    print(Colors.OKGREEN + "[Task: minilua compilation]: started" + Colors.ENDC)
    process = subprocess.Popen(["gcc", "-o", "minilua", "-lm", "minilua.c"], cwd=miniluaPath)
    process.wait()
    if process.returncode != 0:
        print(Colors.FAIL + "[Error: minilua compilation]: failed")
        exit(1)
    print(Colors.OKGREEN + "[Task: minilua compilation]: finished")


def minilua_executable():
    if not exists(miniluaPath + "minilua"):
        print(Colors.WARNING + "[Info]: lua interpreter is required")
        compile_minilua()
    return miniluaPath + "minilua"


def start_preprocessor(file, outfile):
    if arch is None:
        print(Colors.FAIL + "[Error: dynasm]: arch is not specified")
        exit(-1)

    print(Colors.OKGREEN + "[Task: dynasm]: starting preprocessor for", file, Colors.ENDC)
    process = subprocess.Popen([minilua, dynasm + "preprocessor/dynasm.lua", "-o", outfile, "-D", arch, file])
    process.wait()

    if process.returncode != 0:
        print(Colors.FAIL + "[Error: dynasm]: preprocessing failed")
        return

    print(Colors.OKGREEN + "[Task: dynasm]: preprocessing finished. Output file is", outfile)


def output_file_name(src_dir, src_file):
    return str(src_file).replace(".dasm", "")


if __name__ == "__main__":
    if os.name == "nt":
        os.system("color")
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
        src += list(Path(args.dir).rglob("*.dasm.[ch]"))

    if args.files is not None:
        src += args.files

    minilua = minilua_executable()

    for file in src:
        start_preprocessor(file, output_file_name(args.dir, file))
