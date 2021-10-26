import os
import sys
from pathlib import Path
import random
import shutil

dataset_dir=Path(sys.argv[1])  #../data-raw/cross-language-clone/AtCoder
output_dir=Path(sys.argv[2])#../data-raw/cross-language-clone/AtCoder_splits
output_dir.mkdir(parents=True, exist_ok=True)
train_percent = 0.6
val_percent = 0.2
test_percent = 0.2
MIN_SAMPLE_SIZE=10
LANGUAGES=["c", "cpp", "java"]

def random_split(samples):
    random.shuffle(samples)
    total_count= len(samples)
    train_split = int(total_count*train_percent)
    val_split = int(total_count*(train_percent+val_percent))
    return samples[:train_split], samples[train_split:val_split], samples[val_split:]

for question in os.listdir(dataset_dir):
    sample_enough = True
    for language in LANGUAGES:
        solution_dir = dataset_dir/f"{question}/{language}"   
        if not solution_dir.exists():
            sample_enough=False  
            break    
        solution_files = os.listdir(solution_dir)
        if len(solution_files) < MIN_SAMPLE_SIZE :
            sample_enough=False            
            break
    if not sample_enough:
        print(f"too few samples in {dataset_dir/question}")
        continue

    for language in LANGUAGES:
        solution_dir = dataset_dir/f"{question}/{language}" 
        solution_files = os.listdir(solution_dir)
        spilt_files = random_split(solution_files)            
        for i,spilt in enumerate(["train","val", "test"]):
            target_dir = output_dir/f"{spilt}/{question}/{language}" 
            target_dir.mkdir(parents=True, exist_ok=True)
            target_files = [target_dir/f for f in spilt_files[i]]  
            src_files = [solution_dir/f for f in spilt_files[i]]  
            for src,dst in zip(src_files, target_files):
                if src.is_file():
                    shutil.copyfile(src,dst)

