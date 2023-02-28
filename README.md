# Instruction for generating data for AVSS 

Before run this script, you need to install dlib first. 

You can follow this  [blog](https://zhuanlan.zhihu.com/p/381278186) to install. 

This script is only for LRS3 dataset. You need to rewrite something for other datasets. 

    you need to modify path to your own path before running.

## Step 1 Audio process 
1. extract audio 
```shell 
cd audio_process 
./extract_audio.sh
```

2. (optional) cut audio of some speakers to 4~6 s 
```shell
./audio_cut.sh 
```

3. generate text file of mixed audio 
```python
python audio_path.py
```
4. mix audio. This code refers to [Deep Clustering](https://www.merl.com/demos/deep-clustering)
```
/opt18/matlab_2015b/bin/matlab -nosplash -nodesktop -r create_wav_2speakers
```

## Step 2  Video process 

1. extract frames 
```shell
cd video_process 
./extract_frames.sh
```
2. generate file_path_of_frame and save it to LRS3_image.scp 
```
by yourself
```
3. detect and crop face + lip regions 
```python 
python extrac_face_and_lip.py
```
4. convert image sequences to npy 
```
python convert_npy.py 
```

    Thanks for [KaiLi](https://github.com/JusperLee),
    This script is based on his [repo](https://github.com/JusperLee/LRS3-For-Speech-Separation)

