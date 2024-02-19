# -*- coding: utf-8 -*-
# filename: getImg2livp.py
import os
import sys
try:
    from loguru import logger
except ImportError:
    import logging as logger
    logger.basicConfig(level=logger.INFO, stream=sys.stdout)

class ScanLivpImg:
    def __init__(self):
        self.path_list = []
        temp = os.walk(sys.path[0])
        logger.info("="*6+"查找livp"+"="*6)
        for path,dir_list,file_list in temp:
            for file_name in file_list:
                if self.__isLivp(file_name):
                    logger.info(f'发现livp文件:{path}/{file_name}')
                    self.path_list.append(f"{path}/{file_name}")

    def __isLivp(self,filename):
        if filename.split('.')[-1].upper() == 'LIVP':
            return True

FileEofs = {
    'jpeg':b'\xff\xd8\xff\xe0',
    'heic':b"\x00\x00\x00\x20\x66\x74\x79\x70\x68\x65\x69\x63",
    'jpg':b'\xff\xd8\xff\xe1',
}

def convertLivp2Img(file_list:list):
    for file_name in file_list:
        logger.info("="*6+file_name+"="*6)
        logger.info(f"获取{file_name}二进制内容……")
        # 读取二进制内容
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
                logger.info(f"识别到livp中包含{one_type}图片,尝试提取……")
                break
        else: 
            logger.exception("Error, can not found jpeg\heic or jpg.")
            return
        # zip 格式分文件标志
        end_post = buf.rfind(b"\x50\x4b\x03\x04")
        buf = buf[start_pos:end_post]
        save_file_name = file_name.split('.')[0] + '.' + one_type
        with open(save_file_name, "wb") as newjpg:
            newjpg.write(buf)
        logger.info(f"已提取{save_file_name}。")
            
        # 尝试heic转换
        if one_type == "heic" : 
            logger.info(f"尝试转换heic文件至jpg……")
            convertHeic2jpg(save_file_name)

def convertHeic2jpg(heicFilePath:str):
    try:
        from PIL import Image
        from pillow_heif import register_heif_opener
        register_heif_opener()
        #import PIL.Image as PILI
    except ImportError :
        logger.error("未安装 pillow,pillow_heif 库, 跳过HEIC转换, 请通过 pip install pillow pillow_heif 进行安装。")
        return 
    with Image.open(heicFilePath) as img:
        save_file_name = heicFilePath.split(".")[0]+".jpg"
        img.convert('RGB').save(save_file_name)
        logger.info(f"已转换heic文件至{save_file_name}。")
    
if __name__ == "__main__":
    convertLivp2Img(ScanLivpImg().path_list)
    # support cmd exe
    os.system('pause')
