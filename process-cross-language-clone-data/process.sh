#!/bin/bash
input_dir=../data-raw/cross-language-clone/bc/AtCoder
splits_dir=../data-raw/cross-language-clone/bc/AtCoder_splits
output_dir=../data-bin/cross-language-clone/AtCoder
moco_path=../data-bin/pretrain
max_len=511
process=24

#python 1_split_dataset.py $input_dir $splits_dir
python 2_ir_to_json.py $splits_dir/train $output_dir/json/train/ $process $max_len
python 2_ir_to_json.py $splits_dir/val $output_dir/json/val/ $process $max_len
python 2_ir_to_json.py $splits_dir/test $output_dir/json/test/ $process $max_len
python 3_concat_json.py $splits_dir/val/ $output_dir/json/val/ $output_dir/concat_json/val/ label.txt
python 3_concat_json.py $splits_dir/test/ $output_dir/json/test/ $output_dir/concat_json/test/ label.txt
python 3_concat_json.py $splits_dir/train/ $output_dir/json/train/ $output_dir/concat_json/train/ label.txt
python 4_json_to_rawtext.py $output_dir/concat_json/train/ $output_dir/rawtext/train $moco_path $max_len
python 4_json_to_rawtext.py $output_dir/concat_json/val/ $output_dir/rawtext/val $moco_path $max_len
python 4_json_to_rawtext.py  $output_dir/concat_json/test/ $output_dir/rawtext/test $moco_path $max_len
cp $output_dir/rawtext/train/* $output_dir/result/train
cp $output_dir/concat_json/train/label.txt $output_dir/result/train
cp $output_dir/rawtext/val/* $output_dir/result/val
cp $output_dir/concat_json/val/label.txt $output_dir/result/val
cp $output_dir/rawtext/test/* $output_dir/result/test
cp $output_dir/concat_json/test/label.txt $output_dir/result/test
cd ../model
./scripts/classification_preprocess.sh $output_dir/result ../data-bin/poj-classification $moco_path
