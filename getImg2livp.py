# -*- coding: utf-8 -*-
# filename: getImg2livp.py
import os.path
from getLivpImgPath import scanLivpImg
class getImg:
    def __init__(self):
        file_list = scanLivpImg().pathList
        for file_name in file_list:
            buf = bytearray(os.path.getsize(file_name))
            with open(file_name, "rb") as file:
                file.readinto(buf)
            start_pos = buf.find(b"\xff\xd8\xff\xe1")
            end_post = buf.rfind(b"\x50\x4b\x03\x04")
            buf = buf[start_pos:end_post]
            newjpg = open(self.getName(file_name), "wb")
            newjpg.write(buf)
            newjpg.close()

    def getName(self,livpName):
        return livpName.split(".")[0]+".jpg"