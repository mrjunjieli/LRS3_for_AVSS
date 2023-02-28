#!/bin/bash 


#train: select about 50h audio from the file 'train_selected_speaker'  
#and cut each utterancs to 4~6s (0:00 - (0:04~0:06),start time is 0:00)
#validation: select about 5h audio and cut to 4~6s (0:00 - (0:04~0:06))
#test: no operation 


input_audio_folder='/CDShare3/LRS3_process/audio'
output_audio_folder='/CDShare3/LRS3_process/Simulated/cutted'
ffmpeg_path='/Work18/2020/lijunjie/tools/ffmpeg/bin/ffmpeg'



if [ ! -d $output_audio_folder ]; then
  mkdir -p $output_audio_folder
fi




for kind in `ls $input_audio_folder/`; do 
  if [ $kind = 'pretrain' ] || [ $kind = 'trainval' ]
  then 
    speaker_list=$(cat ./${kind}_selected_speaker)
    for speaker in `ls $input_audio_folder/$kind`; do 
        if [[ $speaker_list =~ $speaker ]] 
          then 
            for wav_name in `ls $input_audio_folder/$kind/$speaker`; do 

                if [ ! -d $output_audio_folder/$kind/$speaker ];then 
                    mkdir -p $output_audio_folder/$kind/$speaker
                fi 

                wav_path=$input_audio_folder/$kind/$speaker/$wav_name

                result=`$ffmpeg_path -i $wav_path 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//`

                minute=${result:3:2}
                second=${result:6:2}
                duration=`expr $minute \* 60 + $second`
                # duration=$(echo "$minute * 60 + $second"|bc)


                if [ $duration -gt 6 ]
                then 
                    end_random=`echo "scale=2 ; ${RANDOM}/32767*2+4" | bc -l` # 生成4-6的随机数
                    #cut it from 00:00:00 to end_random 
                    $ffmpeg_path -i $wav_path -ss 00:00:00 -t 00:00:$end_random -acodec copy $output_audio_folder/$kind/$speaker/$wav_name
                elif [ $duration -gt 4 ] && [ $duration -lt 6 ]
                then 
                    cp $wav_path $output_audio_folder/$kind/$speaker/$wav_name 
                fi 
            done
        fi 
    done 
  elif [ $kind = 'test' ]
  then 
      for speaker in `ls $input_audio_folder/$kind`; do 
        for wav_name in `ls $input_audio_folder/$kind/$speaker`; do 
          if [ ! -d $output_audio_folder/$kind/$speaker ];then 
              mkdir -p $output_audio_folder/$kind/$speaker
          fi 
          wav_path=$input_audio_folder/$kind/$speaker/$wav_name
          cp $wav_path $output_audio_folder/$kind/$speaker/$wav_name 
        done
      done 
  fi 
done

