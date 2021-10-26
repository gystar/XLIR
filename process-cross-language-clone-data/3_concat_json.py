import enum
import os
import sys
import subprocess
import json
import base64
from pathlib import Path

ir_dir = sys.argv[1]
json_dir = sys.argv[2]
out_dir = sys.argv[3]
label_file=sys.argv[4]

Path(out_dir).mkdir(parents=True, exist_ok=True)
out_inst = open(os.path.join(out_dir, 'insts.json'), 'w')
out_state = open(os.path.join(out_dir, 'states.json'), 'w')
out_pos = open(os.path.join(out_dir, 'pos.json'), 'w')
label_list = []

def process_inst(in_file):
    with open(in_file) as f:
        func = []
        for line in f:
            data = json.loads(line.strip())
            if data is not None:
                func += data
        out_inst.write(json.dumps(func) + '\n')

def process_states(in_file):
    with open(in_file) as f:
        func = []
        for line in f:
            data = json.loads(line.strip())
            if data is not None:
                func += data
        out_state.write(json.dumps(func) + '\n')

def process_pos(in_file):
    with open(in_file) as f:
        func = []
        for line in f:
            data = json.loads(line.strip())
            if data is not None:
                func += data
        out_pos.write(json.dumps(func) + '\n')

LANGUAGES=["c", "cpp", "java"]

questions = os.listdir(ir_dir)
questions.sort()
for label, question in enumerate(questions):
    for l, language in enumerate(LANGUAGES):
        try:
            for f in os.listdir(os.path.join(ir_dir, question, language)):
                in_filename = os.path.join(ir_dir, question, language, f)
                name = f[:-3]
                if f.endswith('.ll') or f.endswith(".bc"):       
                    file_dir = Path(os.path.join(json_dir, question, language))                    
                    #print('Processing %s' % f)
                    label_list.append(f"{str(label)}, {str(l)}")
                    process_inst(file_dir / f'{name}.insts.json')
                    process_states(file_dir / f'{name}.states.json')
                    process_pos(file_dir / f'{name}.pos.json')                            
        except Exception as e:
            print(e)
with open(os.path.join(out_dir, label_file), 'w') as f:
    f.write('\n'.join(label_list) + '\n')