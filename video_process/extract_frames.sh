#!/bin/bash 

raw_folder='/CDShare/LRS3/'
output_folder='/CDShare3/LRS3_process/temp'
ffmpeg_path='/Work18/2020/lijunjie/tools/ffmpeg/bin/ffmpeg'

if [ ! -d $output_folder ]; then
  mkdir $output_folder
fi

for kind in `ls $raw_folder/`; do 
    if [ -d $raw_folder/$kind ]; then 
        if [ ! -d $output_folder/$kind ]; then
        mkdir $output_folder/$kind
        fi
        for sp in `ls $raw_folder/$kind/`; do 
            if [ ! -d $output_folder/$kind/$sp ]; then
            mkdir $output_folder/$kind/$sp
            fi
            for file in `ls $raw_folder/$kind/$sp`; do
            file_path=$raw_folder/$kind/$sp/$file
            filename=$(echo $file | cut -d . -f1)
            $ffmpeg_path -i $file_path -vf fps=25 -f image2 $output_folder/$kind/$sp/$filename-%04d.jpg
            done
        done
    fi
done