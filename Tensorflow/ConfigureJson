
#######################################################
# 
# ConfigureJson.py
# Created on:      02-6-2016 
# Original author: goooodday 
# 
#######################################################

import os
import json


"""
configItems 클래스 :
   환경설정 정보를 담기위한 데이터 클래스 정의
"""
class configItems(object):
    
    """
    configItems 클래스 생성자 :
     클래스 멤버변수를 초기화 함.
    """
    def __init__(self):
        self.in_path = ''
        self.class_count = 0
        self.image_type = ''
        
        self.out_path = ''
        self.train_path = ''
        self.test_path = ''


"""
ConfigureJson 클래스 :
   JSON 형식의 환경설정 파일을 로딩 및 파싱하여 configItems 데이터 클래스로 로딩함. 
"""

class ConfigureJson(object):

    """
    ConfigureJson 클래스 생성자 :
     클래스 멤버변수를 초기화 함.
    """
    def __init__(self):
        self.json_contents = {}

    """
    jsonReader 메서드 :
     JSON 형식의 환경설정 파일을 로딩 함.
    """
    def jsonReader(self, fileName):
        
        with open(fileName, 'r') as f:
            self.json_contents = json.loads(f.read())
        
    """
    jsonParser 메서드 :
     환경설정 파일의 설정 항목을 configItems 데이터 클래스로 파싱하여 로드함.
    """
    def jsonParser(self):
        items = configItems()
        
        items.in_path = self.json_contents['input_Imagesets']['dir_path']
        items.class_count = self.json_contents['input_Imagesets']['class_count']
        items.image_type = self.json_contents['input_Imagesets']['Image_Type']
        
        items.out_path = self.json_contents['output_Data']['dir_path']
        items.train_path = self.json_contents['output_Data']['train_path']
        items.test_path = self.json_contents['output_Data']['test_path']
        
        return items    

def main():
    conf = ConfigureJson()
    conf.jsonReader("/data1/Notebooks/Test_Source/test.txt")
    
    ITEMs = conf.jsonParser()
    print 'Input parameters ....'
    print ITEMs.in_path, ITEMs.class_count, ITEMs.image_type
    
    print 'Output datas....'
    print ITEMs.out_path, ITEMs.train_path, ITEMs.test_path

    
if __name__ == "__main__":
    main()    
