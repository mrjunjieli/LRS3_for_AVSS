from re import X
import face_recognition
import numpy as np
import os 
import time
import cv2 
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from torch.utils.data import Dataset,DataLoader
from tqdm import tqdm 



start = time.time()
path_save_name = "./LRS3_image.scp"



# CHUNCK_SIZE=2
BATCH_SIZE=50
NUX_PROCESS=4
face_Height=112 
face_Width=112
lip_Height=112
lip_Width=112

def read_path_of_each_speaker(sp_path):
    frame_path_list=[]
    for frame in os.listdir(sp_path):
        frame_path = os.path.join(sp_path,frame)
        frame_path_list.append(frame_path)
    with open(path_save_name,'a+') as p:
        for path in frame_path_list:
            p.write(path+'\n')


def extract_lip(face_path,frame_array,face_location,face_folder,lip_folder):
    new_path = face_path.replace(face_folder,lip_folder)
    
    os.makedirs(os.path.dirname(new_path),exist_ok=True)

    if len(face_location)==0:
         mouth = cv2.resize(frame_array,(lip_Width,lip_Height))
        #!!!!NOTICE: you need to change 100 to the number less than 60, because this line makes the memory of image get larger.
         cv2.imwrite(new_path,mouth,[int(cv2.IMWRITE_JPEG_QUALITY), 50])
    else:
            
        face_landmarks = face_recognition.face_landmarks(frame_array, face_locations=face_location)[0]
        co = 0
        marks = np.zeros((2, 24))
        for facial_feature in face_landmarks.keys():
            if facial_feature == 'top_lip':
                lip = face_landmarks[facial_feature]
                for i in lip:
                    marks[0, co] = i[0]
                    marks[1, co] = i[1]
                    co += 1
            if facial_feature == 'bottom_lip':
                lip = face_landmarks[facial_feature]
                for i in lip:
                    marks[0, co] = i[0]
                    marks[1, co] = i[1]
                    co += 1
        X_left, Y_left, X_right, Y_right = [int(np.amin(marks, axis=1)[0]), int(np.amin(marks, axis=1)[1]),
                                            int(np.amax(marks, axis=1)[0]),int(np.amax(marks, axis=1)[1])]        
        border =3
        X_left=X_left-border
        X_right=X_right+border
        Y_left-=border
        Y_right+=border


        width = abs(X_right-X_left)
        height = abs(Y_right-Y_left)
        width = max([width,height])
        height = width 

        X_right = X_left+width
        h_center = (Y_left+Y_right)/2 
        Y_left  = int(h_center-height/2)
        Y_right = int(h_center+height/2)

        if X_left<0:
            X_left=0
        if Y_left<0:
            Y_left=0
        if X_right>frame_array.shape[0]:
            X_right=frame_array.shape[0]
        if Y_right>frame_array.shape[0]:
            Y_right=frame_array.shape[0]

        mouth = frame_array[Y_left:Y_right,X_left:X_right]
        mouth = cv2.resize(mouth,(lip_Width,lip_Height))
        #!!!!NOTICE: you need to change 100 to the number less than 60, because this line makes the memory of image get larger.
        cv2.imwrite(new_path,mouth,[int(cv2.IMWRITE_JPEG_QUALITY), 50])


def extract_face_singleprocess(idx,face_locations,frame_path_list,frame_array_list,frame_folder,face_folder,lip_folder):
    old_path = frame_path_list[idx]
    face_location = face_locations[idx]
    frame_array=frame_array_list[idx]
    new_path = old_path.replace(frame_folder,face_folder)
    os.makedirs(os.path.dirname(new_path),exist_ok=True)

    if len(face_location)!=0:
        x_left,y_right,x_right,y_left = face_location[0]
        face_image = frame_array[x_left:x_right,y_left:y_right]
        # face_image= cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        face_image = cv2.resize(face_image,(face_Height,face_Width))
        
        #!!!!NOTICE: you need to change 100 to the number less than 60, because this line makes the memory of image get larger.
        cv2.imwrite(new_path,face_image,[int(cv2.IMWRITE_JPEG_QUALITY), 30]) 
    else:
        frame_array_new = cv2.resize(frame_array,(face_Height,face_Width))
        
        #!!!!NOTICE: you need to change 100 to the number less than 60, because this line makes the memory of image get larger.
        cv2.imwrite(new_path,frame_array_new,[int(cv2.IMWRITE_JPEG_QUALITY), 30])

    extract_lip(new_path,frame_array,face_location,face_folder,lip_folder)



def extract_face(frame_path_list,frame_array_list,frame_folder,face_folder,lip_folder):
    '''
    extract face from each frame
    '''

    face_locations = face_recognition.batch_face_locations(frame_array_list, 
            number_of_times_to_upsample=1,batch_size=BATCH_SIZE)

    idx_list = [idx for idx in range(len(face_locations))]
    for idx in idx_list:
        extract_face_singleprocess(idx,face_locations,frame_path_list,frame_array_list,frame_folder,face_folder,lip_folder)

    # with ProcessPoolExecutor(NUX_PROCESS) as ex:
    #     func = partial(extract_face_singleprocess,face_locations=face_locations,frame_path_list=frame_path_list,
    #                 frame_array_list=frame_array_list,frame_folder=frame_folder,face_folder=face_folder,lip_folder=lip_folder)
    #     ex.map(func, idx_list)


class FramesDataset(Dataset):
    '''
    Load image data
    '''
    def __init__(self,s1_scp=None):
        super(FramesDataset,self).__init__()
        self.path_list=self.handle_scp(s1_scp)
    
    def __len__(self):
        return len(self.path_list)

    def __getitem__(self,index):
        return  self.load_fram(self.path_list,index),self.path_list[index]


    def handle_scp(self,s1_scp):
        path_list = []
        with open(s1_scp, 'r') as f:
            for line in f.readlines():
                path_list.append(line.strip())
        return path_list
    
    def load_fram(self,path_list,index):
        path = path_list[index]
        frame_array = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        if type(frame_array) is not np.ndarray:
            frame_array = np.zeros((face_Height,face_Width)).astype(int)
        return frame_array
    
def collate_fn_(dataBatch):

    frame_list = [batch[0] for batch in dataBatch]
    path_list = [batch[1] for batch in dataBatch]

    return {
        'frame':frame_list,
        'path':path_list
    }

class FrameDataloder(DataLoader):
    def __init__(self,*args, **kwargs):
        super(FrameDataloder,self).__init__(*args, **kwargs)



def main_process(frame_folder,face_folder,lip_folder,path_file_name):
    '''
    frame_folder: raw frame extracted from video. The folder contains [pretrain,trainval,test]
    face_folder: The output folder used to save 'face region' of frame. 
    '''
    face_folder = os.path.join(face_folder)
    frame_folder = os.path.join(frame_folder)
    lip_folder = os.path.join(lip_folder)

    flag=2
    if flag<=1:
        #Step1 write path of each image to file
        if os.path.exists(path_save_name):
            os.remove(path_save_name)
        for kind_ in ['pretrain','trainval','test']:
            kind_path = os.path.join(frame_folder,kind_)
            sp_path_list=[]
            for speaker in os.listdir(kind_path):
                sp_path = os.path.join(kind_path,speaker)
                sp_path_list.append(sp_path)
            with ProcessPoolExecutor(NUX_PROCESS) as ex:
                func = partial(read_path_of_each_speaker,)
                ex.map(func, sp_path_list)
        print('Step 1 finished...')

    if flag <=2:
        print('Step 2: extract face from frames start..')
        
        dataset = FramesDataset(path_file_name)
        dataLoader = FrameDataloder(dataset,batch_size=BATCH_SIZE*10 ,num_workers=NUX_PROCESS,
                collate_fn=collate_fn_,drop_last=False,shuffle=False,prefetch_factor=4)

        for idx,eg in enumerate(tqdm(dataLoader)):
            frame_array_list = eg['frame']
            frame_path_list=eg['path']
            extract_face(frame_path_list,frame_array_list,frame_folder,face_folder,lip_folder)




if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--LRS3file', type=str,default='./LRS3_image.scp')
    
    args = parser.parse_args()
    main_process('/CDShare3/LRS3_process/frames','/CDShare3/LRS3_process/faces',"/CDShare3/LRS3_process/lips",args.LRS3file)
    

    print((time.time()-start)/60)
