from typing import List
import utils
import os,sys
from pathlib import Path
import logging

current_dir = os.path.dirname(os.path.realpath(__file__))

TIMEOUT = 60

cmd_func = lambda x, y: ["timeout", "-s9", str(TIMEOUT)]+[CLANG_PATH] + \
    f"-emit-llvm -S -xc++ -std=c++11 -Wno-everything".split(" ")+[x,"-o", y]


SRC_DIR = Path("data-raw/poj-binary_code-clone/ProgramData")
DST_DIR = Path("data-raw/poj-binary_code-clone/irs")

def cmds():
    for question in os.listdir(SRC_DIR):
        dst_file_dir = DST_DIR / question
        dst_file_dir.mkdir(parents=True, exist_ok=True)
        for solution in os.listdir(SRC_DIR / question):
            full_path = SRC_DIR / f"{question}/{solution}"
            dst_file_path = dst_file_dir / f"{solution}.ll"
            print(f"processing {full_path}")
            yield cmd_func(str(full_path), str(dst_file_path))
            
utils.run_cmds_parallel(cmds())

#/mnt/opt/llvm-6.0/bin/clang -emit-llvm -S -xc++ -std=c++11 -Wno-everything data-raw/poj-binary_code-clone/ProgramData/92/1007.txt -o data-raw/poj-binary_code-clone/irs/92/1007.txt.ll 
        