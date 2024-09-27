# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： text_split_handle.py
    @date：2024/3/27 18:19
    @desc:
"""
import re
from typing import List

import fitz
import cv2
import numpy as np
from paddleocr import PPStructure
from paddle.utils import try_import
from PIL import Image

from common.handle.base_split_handle import BaseSplitHandle
from common.util.split_model import SplitModel

default_pattern_list = [re.compile('(?<=^)# .*|(?<=\\n)# .*'),
                        re.compile('(?<=\\n)(?<!#)## (?!#).*|(?<=^)(?<!#)## (?!#).*'),
                        re.compile("(?<=\\n)(?<!#)### (?!#).*|(?<=^)(?<!#)### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)#### (?!#).*|(?<=^)(?<!#)#### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)##### (?!#).*|(?<=^)(?<!#)##### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)###### (?!#).*|(?<=^)(?<!#)###### (?!#).*"),
                        re.compile("(?<!\n)\n\n+")]

def process_file(pdf_document):
    """  
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

        img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    #print(2)

        result = ocr_engine(img)# 执行OCR识别  
        sorted_data_list = sorted(result,key=lambda k: k['bbox'][1])  # 按bbox排序
        
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
            buffer = get_buffer(file)
            pdf_document = fitz.open(file.name, buffer)

            content = process_file(pdf_document)


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
