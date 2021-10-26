from typing import List
import utils
import os, sys
from pathlib import Path
import logging

current_dir = os.path.dirname(os.path.realpath(__file__))
logger = utils.setup_logger("bin2ir", "outputs/ir2bins.log")

logging.basicConfig(
    level=logging.DEBUG,  
    filename="./outputs/code2ir.log",
    filemode="a",  
    format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)
SRC_DIR = Path("data-raw/poj-binary_code-clone/ProgramData")

GCC_PATH = "/usr/bin/g++"
# g++ -O0 -s -m32 31.c -o 31.a
GCC_ARM_32_PATH = "/usr/bin/arm-linux-gnueabihf-g++"
# arm-linux-gnueabihf-g++ -O0 -s 31.c -o 31.a
GCC_ARM_64_PATH = "/usr/bin/aarch64-linux-gnu-g++"
# aarch64-linux-gnu-g++ -O0 -s 31.c -o 31.a

CLANG_PATH = "/home/opt/llvm-6.0/bin/clang++"
# clang++ -O0 -s -m32 -target armv7-unknown-linux-gnu 31.c -o 31.a
ARC_CMDS = [
    [GCC_PATH, "-s", "-m32", "-xc++", "-std=c++11"],  # gcc-x86-32
    [GCC_PATH, "-s", "-m64", "-xc++", "-std=c++11"],  # gcc-x86-64
    [GCC_ARM_32_PATH, "-s", "-xc++", "-std=c++11"],  # gcc-arm-32
    [GCC_ARM_64_PATH, "-s", "-xc++", "-std=c++11"],  # gcc-arm-64
    [CLANG_PATH, "-s", "-m32", "-xc++", "-std=c++11"],  # clang-x86-32
    [CLANG_PATH, "-s", "-m64", "-xc++", "-std=c++11"],  # clang-x86-64
    #arm-linux-gnueabi/bin/ld: cannot find -lstdc++
    #[CLANG_PATH, "-s", "-m32", "-target", "arm-unknown-linux-gnu", "-xc++", "-std=c++11"],  # clang-arm-32
    [CLANG_PATH, "-s", "-m64", "-target", "arm-unknown-linux-gnu", "-xc++", "-std=c++11", "-I/usr/include/x86_64-linux-gnu/c++/7"],  # clang-arm-64
]
ARC_NAMES = [
    "gcc-x86-32",
    "gcc-x86-64",
    "gcc-arm-32",
    "gcc-arm-64",
    "clang-x86-32",
    "clang-x86-64",
    #"clang-arm-32",
    "clang-arm-64",
]

OPTIMITIONS = ["-O0", "-O1", "-O2", "-O3"]
TIMEOUT = 60
TIME_OUT_OPTIONS = ["timeout", "-s9", str(TIMEOUT)]

SRC_DIR = Path("data-raw/poj-binary_code-clone/ProgramData")
DST_DIR = Path("data-raw/poj-binary_code-clone/bins")


def cmds():
    for question in os.listdir(SRC_DIR):
        for solution in os.listdir(SRC_DIR / question):
            full_path = SRC_DIR / f"{question}/{solution}"
            for i, arc_cmd in enumerate(ARC_CMDS):
                for optimition in OPTIMITIONS:
                    dst_file_dir = DST_DIR / f"{ARC_NAMES[i]}/{optimition}/{question}"
                    dst_file_dir.mkdir(parents=True, exist_ok=True)
                    dst_file_path = dst_file_dir / f"{solution}.a"
                    if dst_file_path.exists():
                        continue
                    # print(f"processing {full_path}")
                    cmd = (
                        TIME_OUT_OPTIONS
                        + arc_cmd
                        + [optimition, str(full_path), "-o", str(dst_file_path)]
                    )
                    print(cmd)
                    yield cmd


utils.run_cmds_parallel(cmds(), logger)


