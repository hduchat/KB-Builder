# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： text_split_handle.py
    @date：2024/3/27 18:19
    @desc:
"""
import io
import re
from typing import List

import fitz
import cv2
import uuid
import numpy as np
from paddleocr import PPStructure
from paddle.utils import try_import
from copy import deepcopy
from django.db.models import QuerySet
from PIL import Image as PILimage

from common.handle.base_split_handle import BaseSplitHandle
from common.util.split_model import SplitModel
from dataset.models import Image

# 默认的正则表达式列表，用于识别文本中的标题  
default_pattern_list = [re.compile('(?<=^)# .*|(?<=\\n)# .*'),
                        re.compile('(?<=\\n)(?<!#)## (?!#).*|(?<=^)(?<!#)## (?!#).*'),
                        re.compile("(?<=\\n)(?<!#)### (?!#).*|(?<=^)(?<!#)### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)#### (?!#).*|(?<=^)(?<!#)#### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)##### (?!#).*|(?<=^)(?<!#)##### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)###### (?!#).*|(?<=^)(?<!#)###### (?!#).*"),
                        re.compile("(?<!\n)\n\n+")]

pic_item = {"table","figure","equation"}#图片的结构类型

def convert_to_binary(roi_img):  
    # 假设roi_img是PIL图像，需转换为二进制  
    if isinstance(roi_img, PILimage.Image):  
        with io.BytesIO() as output:  
            roi_img.save(output, format='PNG')  # 可以根据需要更改格式  
            binary_data = output.getvalue()  
        return binary_data  
    # 如果roi_img已经是二进制数据，直接返回  
    return roi_img  

def get_title(index, sorted_res_cp,item):
    title = ""
    if (index > 0 and sorted_res_cp[index - 1]["type"].lower() == item  + '_caption'):
        title = [res_item['text'] for res_item in sorted_res_cp[index - 1]["res"]]
    if (index < len(sorted_res_cp) - 1 and sorted_res_cp[index + 1]["type"].lower() == item  + '_caption'):
        title = [res_item['text'] for res_item in sorted_res_cp[index + 1]["res"]]

    return title

def pic_process(result, images_list):
    res_cp = deepcopy(result)
    sorted_res_cp = sorted(res_cp, key=lambda k: k['bbox'][1])

    for index in range(len(sorted_res_cp)):#遍历
        region = sorted_res_cp[index]#范围
        roi_img = region.pop("img")#提取图片
        

        if (region["type"].lower() in pic_item):#检测是否为图片
            image_uuid = uuid.uuid1() 
        
            if len([i for i in images_list if i.id == image_uuid]) == 0:  
                # 创建Image对象并添加到列表中  
                 image = Image(id=image_uuid, image=convert_to_binary(PILimage.fromarray(roi_img)), image_name='22')  
                 images_list.append(image)  
                 return f'![](/api/image/{image_uuid})'
            
def pic_process_file(pdf_document, images_list):
    """  
    ocr提取图片
    """  
    ocr_engine = PPStructure(table=True, ocr=True, show_log=False)
    #初始化ocr模型
    content = ''

    fitz = try_import("fitz")#使用fitz库
    for page_number in range(len(pdf_document)):
        page =pdf_document.load_page(page_number)
        mat = fitz.Matrix(2, 2)# 设置缩放矩阵以提升图像分辨率  
        pm = page.get_pixmap(matrix=mat, alpha=False)  # 获取图像数据 


        # 如果大小过大则使用原始大小
        if pm.width > 2000 or pm.height > 2000:
            pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

        img = PILimage.frombytes("RGB", [pm.width, pm.height], pm.samples)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = ocr_engine(img)# 执行OCR识别  
        res_cp = deepcopy(result)
        sorted_res_cp = sorted(res_cp, key=lambda k: k['bbox'][1])

        for index in range(len(sorted_res_cp)):#遍历
            region = sorted_res_cp[index]#范围
            roi_img = region.pop("img")#提取图片
        
            if (region["type"].lower() in pic_item):#检测是否为图片
                image_uuid = uuid.uuid1() 
            
                if len([i for i in images_list if i.id == image_uuid]) == 0:  
                    # 创建Image对象并添加到列表中  
                    image = Image(id=image_uuid, image=convert_to_binary(PILimage.fromarray(roi_img)), image_name='22')  
                    images_list.append(image)  
                    title = get_title(index, sorted_res_cp, region["type"].lower() )
                    #title ='111111'
                    content += f'# {title}\n'
                    content += f'![](/api/image/{image_uuid})\n'
            
    return content    

def process_file(pdf_document, images_list):
    """  
    ocr提取文本并

    主要步骤:  
        - 初始化OCR引擎  
        - 读取PDF并转换为图像  
        - 对图像执行OCR并保存结果  
    """  
    ocr_engine = PPStructure(table=True, ocr=True, show_log=False)
    #初始化ocr模型
    content = ''

    fitz = try_import("fitz")#使用fitz库
    for page_number in range(len(pdf_document)):
        page =pdf_document.load_page(page_number)
        mat = fitz.Matrix(2, 2)# 设置缩放矩阵以提升图像分辨率  
        pm = page.get_pixmap(matrix=mat, alpha=False)  # 获取图像数据 

        # 如果大小过大则使用原始大小
        if pm.width > 2000 or pm.height > 2000:
            pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

        img = PILimage.frombytes("RGB", [pm.width, pm.height], pm.samples)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = ocr_engine(img)# 执行OCR识别  
        sorted_data_list = sorted(result,key=lambda k: k['bbox'][1])  # 按bbox排序
        
        #content += pic_process(result, images_list)
        
        for data in sorted_data_list:
            #print(data)
            res = data.get('res', [])
            type = data.get('type')#类型
            if type == 'text' or type == 'title' or type == 'reference':#提取对应类型的文本
                for item in res:
                    text = item.get("text")
                    if len(text) > 1:
                        content += text
                        #content = content.join(text)
            content += '\n'


    return content


class PdfocrSplitHandle(BaseSplitHandle):
    def handle(self, file, pattern_list: List, with_filter: bool, limit: int, overlap: int, get_buffer,save_image):
        try:
            image_list = []
            buffer = get_buffer(file)
            pdf_document = fitz.open(file.name, buffer)

            content = process_file(pdf_document, image_list)
            #content = pic_process_file(pdf_document, image_list)

            if len(image_list) > 0:
                save_image(image_list)
                #content += len(image_list)(str)
            if pattern_list is not None and len(pattern_list) > 0:
                split_model = SplitModel(pattern_list, with_filter, limit, overlap)
            else:
                split_model = SplitModel(default_pattern_list, with_filter=with_filter, limit=limit, overlap=overlap)
        except BaseException as e:
            return {'name': file.name,
                    'content': []}
        return {'name': file.name,
                'content': split_model.parse(content)
                }

    def support(self, file, get_buffer):
        file_name: str = file.name.lower()
        if file_name.endswith(".pdf"):
            return True
        return False
    
class Pdf_picocrSplitHandle(BaseSplitHandle):
    def handle(self, file, pattern_list: List, with_filter: bool, limit: int, overlap: int, get_buffer,save_image):
        try:
            image_list = []
            buffer = get_buffer(file)
            pdf_document = fitz.open(file.name, buffer)

            #content = process_file(pdf_document, image_list)
            content = pic_process_file(pdf_document, image_list)

            if len(image_list) > 0:
                save_image(image_list)
                #content += len(image_list)(str)
            if pattern_list is not None and len(pattern_list) > 0:
                split_model = SplitModel(pattern_list, with_filter, limit, overlap)
            else:
                split_model = SplitModel(default_pattern_list, with_filter=with_filter, limit=limit, overlap=overlap)
        except BaseException as e:
            return {'name': file.name,
                    'content': []}
        return {'name': file.name,
                'content': split_model.parse(content)
                }

    def support(self, file, get_buffer):
        file_name: str = file.name.lower()
        if file_name.endswith(".pdf"):
            return True
        return False
