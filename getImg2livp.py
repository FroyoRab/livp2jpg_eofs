# -*- coding: utf-8 -*-
# filename: getImg2livp.py
import os
import sys

class ScanLivpImg:
    def __init__(self):
        self.path_list = []
        temp = os.walk(sys.path[0])
        for path,dir_list,file_list in temp:
            for file_name in file_list:
                if self.__isLivp(file_name):
                    self.path_list.append(file_name)

    def __isLivp(self,filePath):
        if filePath.find(".livp") != -1 or filePath.find(".LIVP") != -1:
            return True

FileEofs = {
    'jpeg':b'\xff\xd8\xff\xe0',
    'heic':b"\x00\x00\x00\x20\x66\x74\x79\x70\x68\x65\x69\x63",
    'jpg':b'\xff\xd8\xff\xe1',
}

class GetImg:
    def __init__(self):
        file_list = ScanLivpImg().path_list
        for file_name in file_list:
            buf = bytearray(os.path.getsize(file_name))
            with open(file_name, "rb") as row_file:
                row_file.readinto(buf)
            
            file_type = None
            start_pos = -1
            # 逐个尝试查找图片文件
            for one_type in FileEofs.keys():
                start_pos = buf.find(FileEofs[one_type])
                if start_pos!=-1:
                    file_type = one_type
                    break
                
            else: print("Error, can not found jpeg\heic or jpg.")
            # zip 格式分文件标志
            end_post = buf.rfind(b"\x50\x4b\x03\x04")
            
            buf = buf[start_pos:end_post]
            saveFileName = file_name.split('.')[0] + '.' + one_type
            with open(saveFileName, "wb") as newjpg:
                newjpg.write(buf)
                
            # 尝试heic转换
            if one_type == "heic" : ConvertHeic2jpg(saveFileName)

def ConvertHeic2jpg(heicFilePath:str):
    try:
        from PIL import Image
        from pillow_heif import register_heif_opener
        register_heif_opener()
        #import PIL.Image as PILI
    except ImportError :
        print("未安装 pillow,pillow_heif 库, 跳过HEIC转换, 请通过 pip install pillow pillow_heif 进行安装。")
        return 
    with Image.open(heicFilePath) as img:
        img.convert('RGB').save(heicFilePath.split(".")[0]+".jpg")
    
if __name__ == "__main__":
    GetImg()
