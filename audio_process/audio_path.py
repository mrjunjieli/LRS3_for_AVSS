'''
This part of the code is mainly to 
generate a txt file of mixed audio, 
the file format is: spk1 SDR spk2 SDR.
'''

import os
import random
from tqdm import tqdm 

sdr_min=-5
sdr_max=10

#step 1 
# get all audio path 
pretrain_audio_path={}
trainval_audio_path={}
test_audio_path={}

path = '/CDShare3/LRS3_process/Simulated/cutted/'

print('Start step 1 ')
for speaker in tqdm(os.listdir(os.path.join(path,'pretrain'))):
    for wav_file in os.listdir(os.path.join(path,"pretrain",speaker)):
        wav_file_path = os.path.join(path,"pretrain",speaker,wav_file)
        if speaker not in pretrain_audio_path.keys():
            pretrain_audio_path[speaker] = [wav_file_path]
        else:
            pretrain_audio_path[speaker].append(wav_file_path)
for speaker in tqdm(os.listdir(os.path.join(path,'trainval'))):
    for wav_file in os.listdir(os.path.join(path,"trainval",speaker)):
        wav_file_path = os.path.join(path,"trainval",speaker,wav_file)
        if speaker not in trainval_audio_path.keys():
            trainval_audio_path[speaker] = [wav_file_path]
        else:
            trainval_audio_path[speaker].append(wav_file_path)
for speaker in tqdm(os.listdir(os.path.join(path,'test'))):
    for wav_file in os.listdir(os.path.join(path,"test",speaker)):
        wav_file_path = os.path.join(path,"test",speaker,wav_file)
        if speaker not in test_audio_path.keys():
            test_audio_path[speaker] = [wav_file_path]
        else:
            test_audio_path[speaker].append(wav_file_path)
print('Finish step 1')        



#step 2
#  write path into file 
#each wav could be used twice 
# 


output_folder='./mixed_audio/'

#step 2.1 generate mixed audio from different speakers 
#
print('Start step 2.1')

output_folder_d = os.path.join(output_folder,'different')
os.makedirs(output_folder_d,exist_ok=True)

#pretrain
print('  pretrain...')
speaker_list = list(pretrain_audio_path.keys())
wav_list=[]
for value in pretrain_audio_path.values():
    wav_list+=value
wav_list_count=[0]*len(wav_list)
result_list=[]

while(len(speaker_list)>=2):
    speaker1=random.choice(speaker_list)
    speaker2 = random.choice(list(set(speaker_list)-set([speaker1])))

    wav_1 = random.choice(pretrain_audio_path[speaker1])
    wav_2=  random.choice(pretrain_audio_path[speaker2])

    index_1 = wav_list.index(wav_1)
    index_2 = wav_list.index(wav_2)

    wav_list_count[index_1]+=1
    wav_list_count[index_2]+=1

    if wav_list_count[index_1]>=2:
        pretrain_audio_path[speaker1].remove(wav_1)
        if len(pretrain_audio_path[speaker1])==0:
            del pretrain_audio_path[speaker1]
            speaker_list.remove(speaker1)
    if wav_list_count[index_2]>=2:
        pretrain_audio_path[speaker2].remove(wav_2)
        if len(pretrain_audio_path[speaker2])==0:
            del pretrain_audio_path[speaker2]
            speaker_list.remove(speaker2)

    snr1 = round(random.uniform(sdr_min,sdr_max),2)
    snr2 = round(random.uniform(sdr_min,sdr_max),2) 

    result = str(wav_1)+' '+str(snr1)+' '+str(wav_2)+' '+str(snr2)  
    result_list.append(result)

with open(os.path.join(output_folder_d,'mix_2_spk_pretrain.txt'),'w') as p:
    for line in result_list:
        p.write(line+'\n')


#trainval
print('  trainval...')
speaker_list = list(trainval_audio_path.keys())
wav_list=[]
for value in trainval_audio_path.values():
    wav_list+=value

wav_list_count=[0]*len(wav_list)
result_list=[]

while(len(speaker_list)>=2):
    speaker1=random.choice(speaker_list)
    speaker2 = random.choice(list(set(speaker_list)-set([speaker1])))

    wav_1 = random.choice(trainval_audio_path[speaker1])
    wav_2=  random.choice(trainval_audio_path[speaker2])

    index_1 = wav_list.index(wav_1)
    index_2 = wav_list.index(wav_2)

    wav_list_count[index_1]+=1
    wav_list_count[index_2]+=1

    if wav_list_count[index_1]>=2:
        trainval_audio_path[speaker1].remove(wav_1)
        if len(trainval_audio_path[speaker1])==0:
            del trainval_audio_path[speaker1]
            speaker_list.remove(speaker1)
    if wav_list_count[index_2]>=2:
        trainval_audio_path[speaker2].remove(wav_2)
        if len(trainval_audio_path[speaker2])==0:
            del trainval_audio_path[speaker2]
            speaker_list.remove(speaker2)

    snr1 = round(random.uniform(sdr_min,sdr_max),2)
    snr2 = round(random.uniform(sdr_min,sdr_max),2) 

    result = str(wav_1)+' '+str(snr1)+' '+str(wav_2)+' '+str(snr2)  
    result_list.append(result)

with open(os.path.join(output_folder_d,'mix_2_spk_trainval.txt'),'w') as p:
    for line in result_list:
        p.write(line+'\n')

#test
print('  test...')
speaker_list = list(test_audio_path.keys())
wav_list=[]
for value in test_audio_path.values():
    wav_list+=value
wav_list_count=[0]*len(wav_list)
result_list=[]

while(len(speaker_list)>=2):
    speaker1=random.choice(speaker_list)
    speaker2 = random.choice(list(set(speaker_list)-set([speaker1])))

    wav_1 = random.choice(test_audio_path[speaker1])
    wav_2=  random.choice(test_audio_path[speaker2])

    index_1 = wav_list.index(wav_1)
    index_2 = wav_list.index(wav_2)

    wav_list_count[index_1]+=1
    wav_list_count[index_2]+=1

    if wav_list_count[index_1]>=2:
        test_audio_path[speaker1].remove(wav_1)
        if len(test_audio_path[speaker1])==0:
            del test_audio_path[speaker1]
            speaker_list.remove(speaker1)
    if wav_list_count[index_2]>=2:
        test_audio_path[speaker2].remove(wav_2)
        if len(test_audio_path[speaker2])==0:
            del test_audio_path[speaker2]
            speaker_list.remove(speaker2)

    snr1 = round(random.uniform(sdr_min,sdr_max),2)
    snr2 = round(random.uniform(sdr_min,sdr_max),2) 

    result = str(wav_1)+' '+str(snr1)+' '+str(wav_2)+' '+str(snr2)  
    result_list.append(result)

with open(os.path.join(output_folder_d,'mix_2_spk_test.txt'),'w') as p:
    for line in result_list:
        p.write(line+'\n')

print('Finish step 2.1 ')




#step 2.2 generate mixed audio from same speakers 
#
print('start step 2.2')

output_folder_s = os.path.join(output_folder,'same')
os.makedirs(output_folder_s,exist_ok=True)

#pretrain
print('  pretrain...')
speaker_list = list(pretrain_audio_path.keys())
wav_list=[]
for value in pretrain_audio_path.values():
    wav_list+=value
wav_list_count=[0]*len(wav_list)
result_list=[]

while(len(speaker_list)>=1):
    speaker1=random.choice(speaker_list)
    if len(pretrain_audio_path[speaker1])<=1:
        del pretrain_audio_path[speaker1]
        speaker_list.remove(speaker1)
        continue
    

    wav_1 = random.choice(pretrain_audio_path[speaker1])
    wav_2=  random.choice(list(set(pretrain_audio_path[speaker1])-set([wav_1])))

    index_1 = wav_list.index(wav_1)
    index_2 = wav_list.index(wav_2)

    wav_list_count[index_1]+=1
    wav_list_count[index_2]+=1

    if wav_list_count[index_1]>=2:
        pretrain_audio_path[speaker1].remove(wav_1)
    if wav_list_count[index_2]>=2:
        pretrain_audio_path[speaker1].remove(wav_2)
    if len(pretrain_audio_path[speaker1])<=1:
        del pretrain_audio_path[speaker1]
        speaker_list.remove(speaker1)

    snr1 = round(random.uniform(sdr_min,sdr_max),2)
    snr2 = round(random.uniform(sdr_min,sdr_max),2) 

    result = str(wav_1)+' '+str(snr1)+' '+str(wav_2)+' '+str(snr2)  
    result_list.append(result)

with open(os.path.join(output_folder_s,'mix_2_spk_pretrain.txt'),'w') as p:
    for line in result_list:
        p.write(line+'\n')


#trainval
print('  trainval...')
speaker_list = list(trainval_audio_path.keys())
wav_list=[]
for value in trainval_audio_path.values():
    wav_list+=value

wav_list_count=[0]*len(wav_list)
result_list=[]

while(len(speaker_list)>=1):
    speaker1=random.choice(speaker_list)
    if len(trainval_audio_path[speaker1])<=1:
        del trainval_audio_path[speaker1]
        speaker_list.remove(speaker1)
        continue

    wav_1 = random.choice(trainval_audio_path[speaker1])
    wav_2=  random.choice(list(set(trainval_audio_path[speaker1])-set([wav_1])))

    index_1 = wav_list.index(wav_1)
    index_2 = wav_list.index(wav_2)

    wav_list_count[index_1]+=1
    wav_list_count[index_2]+=1

    if wav_list_count[index_1]>=2:
        trainval_audio_path[speaker1].remove(wav_1)
    if wav_list_count[index_2]>=2:
        trainval_audio_path[speaker1].remove(wav_2)
    if len(trainval_audio_path[speaker1])<=1:
        del trainval_audio_path[speaker1]
        speaker_list.remove(speaker1)

    snr1 = round(random.uniform(sdr_min,sdr_max),2)
    snr2 = round(random.uniform(sdr_min,sdr_max),2) 

    result = str(wav_1)+' '+str(snr1)+' '+str(wav_2)+' '+str(snr2)  
    result_list.append(result)

with open(os.path.join(output_folder_s,'mix_2_spk_trainval.txt'),'w') as p:
    for line in result_list:
        p.write(line+'\n')

#test
print('  test...')
speaker_list = list(test_audio_path.keys())
wav_list=[]
for value in test_audio_path.values():
    wav_list+=value
wav_list_count=[0]*len(wav_list)
result_list=[]

while(len(speaker_list)>=1):
    speaker1=random.choice(speaker_list)
    if len(test_audio_path[speaker1])<=1:
        del test_audio_path[speaker1]
        speaker_list.remove(speaker1)
        continue

    wav_1 = random.choice(test_audio_path[speaker1])
    wav_2=  random.choice(list(set(test_audio_path[speaker1])-set([wav_1])))

    index_1 = wav_list.index(wav_1)
    index_2 = wav_list.index(wav_2)

    wav_list_count[index_1]+=1
    wav_list_count[index_2]+=1

    if wav_list_count[index_1]>=2:
        test_audio_path[speaker1].remove(wav_1)
    if wav_list_count[index_2]>=2:
        test_audio_path[speaker1].remove(wav_2)
    if len(test_audio_path[speaker1])<=1:
        del test_audio_path[speaker1]
        speaker_list.remove(speaker1)

    snr1 = round(random.uniform(sdr_min,sdr_max),2)
    snr2 = round(random.uniform(sdr_min,sdr_max),2) 

    result = str(wav_1)+' '+str(snr1)+' '+str(wav_2)+' '+str(snr2)  
    result_list.append(result)

with open(os.path.join(output_folder_s,'mix_2_spk_test.txt'),'w') as p:
    for line in result_list:
        p.write(line+'\n')

print('Finish step 2.2 ')