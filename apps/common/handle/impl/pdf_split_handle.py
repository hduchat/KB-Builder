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

from common.handle.base_split_handle import BaseSplitHandle
from common.util.split_model import SplitModel

#正则表达式列表，用于识别和分割文本
default_pattern_list = [re.compile('(?<=^)# .*|(?<=\\n)# .*'),
                        re.compile('(?<=\\n)(?<!#)## (?!#).*|(?<=^)(?<!#)## (?!#).*'),
                        re.compile("(?<=\\n)(?<!#)### (?!#).*|(?<=^)(?<!#)### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)#### (?!#).*|(?<=^)(?<!#)#### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)##### (?!#).*|(?<=^)(?<!#)##### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)###### (?!#).*|(?<=^)(?<!#)###### (?!#).*"),
                        re.compile("(?<!\n)\n\n+")]

#定义一个函数，从特定页面将pdf转为字符串
def number_to_text(pdf_document, page_number):
    page = pdf_document.load_page(page_number)
    text = page.get_text()
    return text

class PdfocrSplitHandle(BaseSplitHandle):
    def handle(self, file, pattern_list: List, with_filter: bool, limit: int, overlap: int, get_buffer,save_image):
        try:
            buffer = get_buffer(file)
            pdf_document = fitz.open(file.name, buffer)
            content = "\n".join([number_to_text(pdf_document, page_number) for page_number in range(len(pdf_document))])
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


class PdfSplitHandle(BaseSplitHandle):
    def handle(self, file, pattern_list: List, with_filter: bool, limit: int, overlap: int, get_buffer,save_image):
        try:
            buffer = get_buffer(file)
            pdf_document = fitz.open(file.name, buffer)
            content = "\n".join([number_to_text(pdf_document, page_number) for page_number in range(len(pdf_document))])
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
