from pathlib import Path
import utils
import os,sys


logger = utils.setup_logger("bin2ir", "outputs/bins2ir.log")
# python /mnt/opt/retdec_4.0/bin/retdec-decompiler.py --keep-unreachable-funcs --stop-after bin2llvmir -o 31.ll 31.a
DECOMPILER_PATH = "/mnt/opt/retdec_4.0/bin/retdec-decompiler.py"
cmd_func = lambda x, y: [
    "python",
    DECOMPILER_PATH,
    "--keep-unreachable-funcs",
    "--stop-after",
    "bin2llvmir",
    "-o",
    y,
    x,
]

SRC_DIR = Path("data-raw/poj-binary_code-clone/bins")
DST_DIR = Path("data-raw/poj-binary_code-clone/bin_irs")
def cmds():
    for arch in os.listdir(SRC_DIR):
        for optimition in os.listdir(SRC_DIR/arch):
            for question in os.listdir(SRC_DIR /f"{arch}/{optimition}"):
                for solution in os.listdir(SRC_DIR /f"{arch}/{optimition}/{question}"):
                    full_path = SRC_DIR / f"{arch}/{optimition}/{question}/{solution}"
                    dst_file_dir = DST_DIR / f"{arch}/{optimition}/{question}"
                    dst_file_dir.mkdir(parents=True, exist_ok=True)
                    dst_file_path = dst_file_dir / f"{solution}.ll" 
                    if dst_file_path.exists():
                        continue
                    cmd = cmd_func(str(full_path), str(dst_file_path))
                    print(cmd)
                    yield cmd

utils.run_cmds_parallel(cmds())



