# -*- coding: utf-8 -*-
# filename: getLivpImgPath.py
import os
import re
import sys

class scanLivpImg:
    def __init__(self):
        self.pathList = []
        temp = os.walk(sys.path[0])
        for path,dir_list,file_list in temp:
            for file_name in file_list:
                if self.__isLivp(file_name):
                    self.pathList.append(file_name)

    def __isLivp(self,filePath):
        if filePath.find(".livp") != -1 or filePath.find(".LIVP") != -1:
            return True