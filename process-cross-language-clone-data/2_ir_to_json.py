import os
import sys
import subprocess
import json
from multiprocessing import Pool
from pathlib import Path

OPT_PATH = "/usr/bin/opt-10"

def process(in_file, inst_file, state_file, pos_file, max_len):
    cmd = [OPT_PATH, '-load', '../bin/libanalysis.so']
# need this .so library
    cmd += '-staticanalysis -max-len'.split()
    cmd += [max_len, '-truncate', '-concat-func']
    cmd += ['-inst-out', inst_file]
    cmd += ['-state-out', state_file]
    cmd += ['-pos-out', pos_file]
    #cmd += '-o /dev/null'.split()
    print(" ".join(cmd))
    print(in_file)
    subprocess.run(cmd, stdin=open(in_file), stderr=subprocess.STDOUT)

in_dir = sys.argv[1]
out_dir = sys.argv[2]
processes = int(sys.argv[3])
max_len = sys.argv[4]
LANGUAGES=["c", "cpp", "java"]

pool = Pool(processes=processes)

for question in os.listdir(in_dir):
    for language in LANGUAGES:
        try:
            for f in os.listdir(os.path.join(in_dir, question, language)):
                in_filename = os.path.join(in_dir, question, language, f)
                name = f[:-3]
                file_out_dir = os.path.join(out_dir, question, language)
                Path(file_out_dir).mkdir(parents=True, exist_ok= True)
                args = (in_filename, os.path.join(file_out_dir, f'{name}.insts.json'), \
                     os.path.join(file_out_dir, f'{name}.states.json'), os.path.join(file_out_dir, f'{name}.pos.json'), max_len)
                pool.apply_async(process, args)
        except:
            pass

pool.close()
pool.join()

#for f in os.listdir(in_dir):
#    in_filename = os.path.join(in_dir, f)
#    if os.path.isfile(in_filename):
#        if f.endswith('.ll'):
#            index = f[:-3]
#            print('Processing %s' % index)
#            process(os.path.join(in_dir, index + '.ll'), os.path.join(out_dir, index + '.insts.json'),
#                os.path.join(out_dir, index + '.states.json'), os.path.join(out_dir, index + '.pos.json'))
