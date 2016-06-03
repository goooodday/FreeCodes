
#######################################################
# 
# BuildDataset.py
# Created on:      02-6-2016 
# Original author: goooodday
# 
#######################################################

import os
import Image
import numpy as np
import matplotlib.pyplot as plt

%matplotlib notebook 

"""
BuildDataset 클래스 :
 결함 이미지 데이터를 Binary 데이터로 변환 및 라벨링 처리하는 함수 
"""
class BuildDataset(object):
    
    """
    BuildDataset 클래스 생성자 :
     클래스 멤버변수를 초기화 함.
    """
    def __init__(self, path):
        
        self.path = path
        self.valid_exts = ['.jpg','.png','.bmp']
        
        self.isBuildOK = False
        
        # 전체 이미지 개수
        self.TotalImageCount = 0
        # 결함 항목 수
        self.ClassCount = 0
        
        self.Width = 32
        self.Height = 32
        
        self.Total_Image = []
        self.Total_LabelText =[]
        self.Total_LabelNum = []
                
        
    """
    GetStorageInfo 멤버 메소드 :
     이미지 저장소의 디렉토리 개수와 각 디렉토리 내의 이미지 개수 확인.
     디렉토리 개수는 Class의 개수로 사용함.
    """    
    def GetStorageInfo(self):
        
        if self.path == '':
            return False
        
        # 해당 디렉토리의 하위 디렉토리 이름 조회
        Dir_list = sorted(os.listdir(self.path))

        for dir_name in Dir_list:
            fullpath = self.path + dir_name
            
            # 이미지 확장자에 해당되는 파일 리스트 조회
            image_files = ([fn for fn in os.listdir(fullpath) if os.path.splitext(fn)[1].lower() in self.valid_exts])
            
            self.TotalImageCount += len(image_files)
            #print ('Class %s (%d)' %(dir_name, len(image_files)))

        # 폴더의 개수로 Class 사용
        self.ClassCount = len(Dir_list)
        
        return True
    
    
    """
    BuildBinary 멤버 메소드 :
     DL에서 사용할 수 있도록 이미지와 라벨 구성으로 Binary 데이터를 생성.
    """     
    def BuildBinary(self):
        
        self.Total_Image   = np.ndarray((self.TotalImageCount, self.Width * self.Height))
        
        self.Total_LabelText = np.chararray(self.TotalImageCount, 20)
        self.Total_LabelNum = np.zeros(self.TotalImageCount)
        
        
        # 해당 디렉토리의 하위 디렉토리 이름 조회
        Dir_list = sorted(os.listdir(self.path))
        
        ImageCount = 0
        for dir_name in Dir_list:
            full_path = self.path + dir_name
            
            # 이미지 확장자에 해당되는 파일 조회
            for fn in os.listdir(full_path) :
                
                if os.path.splitext(fn)[1].lower() not in self.valid_exts :
                    continue
                
                #
                # 해당 이미지에 대한 처리 진행.
                #----------------------------------------------------------
                image_path = os.path.join(full_path, fn)
                
                # 원본 이미지 로딩
                img = Image.open(image_path)
                
                # DL 입력 사이즈로 변경
                img_resized = img.resize((self.Width, self.Height))
                img_row = np.reshape(img_resized, (1, -1))
                
                self.Total_Image[ImageCount, : ] = img_row
                self.Total_LabelText[ImageCount] = dir_name   # 이후에 결함 명을 추가.
                self.Total_LabelNum[ImageCount] = dir_name

                ImageCount += 1
                
        if ImageCount == self.TotalImageCount :
            self.isBuildOK = True
            print 'Build OK!'

    """
    SaveDataset 멤버 메소드 :
     DL 데이터셋으로 생성된 이미지를 선택하여 Plot으로 표시
     ** Plot뷰어에서만 동작이 가능함.
    """                
    def SaveDataset(self, path):
        
        # 라벨 데이터 수집
        Dataset_Label = np.reshape(self.Total_LabelNum, (self.Total_LabelNum.shape[0], 1))
        
        # 라벨 데이터 + 이미지 데이터 통합
        FullDataset = np.append(Dataset_Label, self.Total_Image, 1).astype(dtype=np.uint8)
        
        # 통합 데이터 저장
        FullDataset.tofile(path)
 

    """
    ViewImage 멤버 메소드 :
     DL 이미지셋중 선택된 이미지를 Plot으로 표시
     ** Plot뷰어에서만 동작이 가능함.
    """ 
    def ViewImage(self, id):
        
        if not self.isBuildOK :
            print 'Not Build Dataset~~~'
        
        currimg = np.reshape(self.Total_Image[id,:], (self.Width, -1))
        plt.imshow(currimg, cmap=plt.get_cmap('gray'))
        plt.show() 
                

def main():
    Image_storage = '/data1/input/'

    Save_path = '/data1/output/'
    
    # 데이터 생성 클래스 인스턴스 생성
    dlb = BuildDataset(Image_storage)
    
    # 저장소의 파일 정보 조회
    if (not dlb.GetStorageInfo()):
        print ('Not Dir Path~~~~')
        
    print ('Number of total images is %d' % (dlb.TotalImageCount))
    print ('Number of total defects is %d' % (dlb.ClassCount))
    
    # 바이너리 데이터 생성.
    dlb.BuildBinary()
    
    # 바이너리 데이터 이미지 표시
    #dlb.ViewImage(600)
    
    dlb.SaveDataset(Save_path + 'data_batch.bin')
    #dlb.SaveDataset(Save_path + 'test_batch.bin')
    
    
if __name__ == "__main__":
    main()    
