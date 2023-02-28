import os
import sys 
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
import numpy as np 
from tqdm import tqdm
import os 
import time
import cv2 


faces_folder='/CDShare3/LRS3_process/faces'
lips_folder='/CDShare3/LRS3_process/lips'


faces_npy_folder = '/CDShare3/LRS3_process/faces_npy'
lips_npy_folder = '/CDShare3/LRS3_process/lips_npy'


NUX_PROCESS=20




def npy_trans(sp_path,input_folder,output_folder):
    new_sp_path = sp_path.replace(input_folder,output_folder)
    utt_dict=dict()
    os.makedirs(new_sp_path,exist_ok=True)

    for image in sorted(os.listdir(sp_path)):
        image_path = os.path.join(sp_path,image)
        utt = image.split('-')[0]
        image_array = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
        if utt not in utt_dict.keys():
            utt_dict[utt]=[]
            utt_dict[utt].append(image_array)
        else:
            utt_dict[utt].append(image_array)
    for utt_key in utt_dict.keys():
        
        output_path = os.path.join(new_sp_path,utt_key+'.npy')
        utt_image_array= np.array(utt_dict[utt_key])

        np.save(output_path,utt_image_array)

def npy_transform(input_folder,output_folder):
    for kind in ['trainval','test']:
        os.makedirs(os.path.join(output_folder,kind),exist_ok=True)
        kind_path = os.path.join(input_folder,kind)
        sp_path_list = []
        for sp in os.listdir(kind_path):
            sp_path = os.path.join(kind_path,sp)
            sp_path_list.append(sp_path)
        with ProcessPoolExecutor(NUX_PROCESS) as ex:
            func = partial(npy_trans,input_folder=input_folder,output_folder=output_folder)
            ex.map(func, sp_path_list)
            # npy_trans(sp_path,input_folder,output_folder)

    print('finish'+str(input_folder))




#convert collection of images to npy 
npy_transform(faces_folder,faces_npy_folder)
npy_transform(lips_folder,lips_npy_folder)





