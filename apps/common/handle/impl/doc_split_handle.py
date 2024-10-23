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
import traceback
import uuid
from typing import List

from docx import Document, ImagePart
from docx.table import Table
from docx.text.paragraph import Paragraph

from common.handle.base_split_handle import BaseSplitHandle
from common.util.split_model import SplitModel
from dataset.models import Image

# 默认的正则表达式列表，用于识别文本中的标题
default_pattern_list = [re.compile('(?<=^)# .*|(?<=\\n)# .*'),
                        re.compile('(?<=\\n)(?<!#)## (?!#).*|(?<=^)(?<!#)## (?!#).*'),
                        re.compile("(?<=\\n)(?<!#)### (?!#).*|(?<=^)(?<!#)### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)#### (?!#).*|(?<=^)(?<!#)#### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)##### (?!#).*|(?<=^)(?<!#)##### (?!#).*"),
                        re.compile("(?<=\\n)(?<!#)###### (?!#).*|(?<=^)(?<!#)###### (?!#).*")]


def image_to_mode(image, doc: Document, images_list, get_image_id):
    """  
    将图片元素转换为Markdown格式。  
    
    流程:  
    1. 获取每个图片的id。  
    2. 根据id获取对应的图片部分。  
    3. 检查图片是否已经存在，若不存在则添加到images_list中。  
    4. 返回对应的Markdown格式字符串。  

    输入
    image: 文档中的图片元素。  
    doc: Document对象。  
    images_list: 用于存储文档中图片的列表。  
    :param get_image_id: 获取唯一图片ID的函数。 

    输出
    图片对应的Markdown字符串，格式为`![](/api/image/{image_uuid})`。  
    """  
    for img_id in image.xpath('.//a:blip/@r:embed'):  # 获取图片id
        part = doc.part.related_parts[img_id]  # 根据图片id获取对应的图片
        if isinstance(part, ImagePart):
            image_uuid = get_image_id(img_id)
            if len([i for i in images_list if i.id == image_uuid]) == 0:
                image = Image(id=image_uuid, image=part.blob, image_name=part.filename)
                images_list.append(image)
            return f'![](/api/image/{image_uuid})'


def get_paragraph_element_txt(paragraph_element, doc: Document, images_list, get_image_id):
    """  
    获取段落元素的文本内容，包括图片。  
    
    流程:  
    1. 检查段落元素中是否包含图片。  
    2. 若包含图片，则将其转换为Markdown格式并组合成字符串。  
    3. 若段落元素有文本内容，则返回文本内容。  
    4. 发生异常时打印错误信息并返回空字符串。  

    输入：
    paragraph_element: 段落元素。  
    doc: Document对象。  
    images_list: 用于存储文档中图片的列表。  
    get_image_id: 获取唯一图片ID的函数。  

    输出：
        段落的文本内容或转为Markdown字符串形式的图片。  
    """  
    try:
        images = paragraph_element.xpath(".//pic:pic")
        if len(images) > 0:
            return "".join(
                [item for item in [image_to_mode(image, doc, images_list, get_image_id) for image in images] if
                 item is not None])
        elif paragraph_element.text is not None:
            return paragraph_element.text
        return ""
    except Exception as e:
        print(e)
    return ""


def get_paragraph_txt(paragraph: Paragraph, doc: Document, images_list, get_image_id):
    """  
    获取段落的文本内容，将所有元素转换为文本。  
    
    流程:  
    1. 遍历段落中的所有元素。  
    2. 调用get_paragraph_element_txt函数获取每个元素的文本内容。  
    3. 将所有元素的文本内容组合成一个字符串。  
    4. 发生异常时返回空字符串。  
    """  
    try:
        return "".join([get_paragraph_element_txt(e, doc, images_list, get_image_id) for e in paragraph._element])
    except Exception as e:
        return ""


def get_cell_text(cell, doc: Document, images_list, get_image_id):
    """  
    获取表格单元格的文本内容。  
    
    流程:  
    1. 遍历单元格中的所有段落。  
    2. 调用get_paragraph_txt函数获取每个段落的文本内容。  
    3. 将所有段落的文本内容组合成一个字符串，并替换换行符为`</br>`。  
    4. 发生异常时返回空字符串。  
    """  
    try:
        return "".join(
            [get_paragraph_txt(paragraph, doc, images_list, get_image_id) for paragraph in cell.paragraphs]).replace(
            "\n", '</br>')
    except Exception as e:
        return ""


def get_image_id_func():
    """  
    创建一个用于获取唯一图片ID的闭包函数。  
    
    流程:  
    1. 定义一个字典image_map用于存储图片ID和UUID的映射。  
    2. 定义内部函数get_image_id，根据图片ID获取UUID。  
    3. 如果图片ID不存在于映射中，则生成一个新的UUID并存储。  
    4. 返回get_image_id函数。  
    """  
    image_map = {}

    def get_image_id(image_id):
        _v = image_map.get(image_id)
        if _v is None:
            image_map[image_id] = uuid.uuid1()
            return image_map.get(image_id)
        return _v

    return get_image_id


class DocSplitHandle(BaseSplitHandle):
    @staticmethod
    def paragraph_to_md(paragraph: Paragraph, doc: Document, images_list, get_image_id):
        """  
        将段落转换为Markdown格式。  
        
        流程:  
        1. 获取段落的样式名称(psn)。  
        2. 判断样式名称是否以'Heading'开头，以确定是否为标题。  
        3. 根据标题的级别生成相应数量的`#`符号和标题文本。  
        4. 若非标题段落，则调用get_paragraph_txt函数获取段落文本内容。  
        5. 发生异常时返回段落的文本内容。 
        """   
        try:
            psn = paragraph.style.name
            if psn.startswith('Heading'):
                return "".join(["#" for i in range(int(psn.replace("Heading ", '')))]) + " " + paragraph.text
        except Exception as e:
            return paragraph.text
        return get_paragraph_txt(paragraph, doc, images_list, get_image_id)

    @staticmethod
    def table_to_md(table, doc: Document, images_list, get_image_id):
        rows = table.rows

        # 创建 Markdown 格式的表格
        md_table = '| ' + ' | '.join(
            [get_cell_text(cell, doc, images_list, get_image_id) for cell in rows[0].cells]) + ' |\n'
        md_table += '| ' + ' | '.join(['---' for i in range(len(rows[0].cells))]) + ' |\n'
        for row in rows[1:]:
            md_table += '| ' + ' | '.join(
                [get_cell_text(cell, doc, images_list, get_image_id) for cell in row.cells]) + ' |\n'
        return md_table

    def to_md(self, doc, images_list, get_image_id):
        """  
        将文档转换为Markdown格式。  
        
        流程:  
        1. 遍历文档中的所有元素。  
        2. 如果元素是表格，则添加为Table对象。  
        3. 如果元素是段落，则添加为Paragraph对象。  
        4. 调用paragraph_to_md和table_to_md函数将元素转换为Markdown格式。  
        5. 将所有Markdown字符串组合成一个完整的Markdown文档。  
        """  
        elements = []
        for element in doc.element.body:
            if element.tag.endswith('tbl'):
                # 处理表格
                table = Table(element, doc)
                elements.append(table)
            elif element.tag.endswith('p'):
                # 处理段落
                paragraph = Paragraph(element, doc)
                elements.append(paragraph)
        return "\n".join(
            [self.paragraph_to_md(element, doc, images_list, get_image_id) if isinstance(element,
                                                                                         Paragraph) else self.table_to_md(
                element,
                doc,
                images_list, get_image_id)
             for element
             in elements])

    def handle(self, file, pattern_list: List, with_filter: bool, limit: int, overlap: int, get_buffer, save_image):
        """  
        处理文件并将其内容转换为Markdown格式。  
        
        流程:  
        1. 初始化图片列表。  
        2. 调用get_buffer函数获取文件的字节流。  
        3. 创建Document对象。  
        4. 调用to_md函数将文档内容转换为Markdown格式。  
        5. 如果有图片则调用save_image函数保存图片。  
        6. 根据传入的pattern_list或者默认的default_pattern_list创建SplitModel。  
        7. 调用split_model的parse方法切分Markdown内容。  
        8. 捕获并处理任何异常，输出错误信息。  
        9. 返回包含文件名和切分内容的字典。   
        """  
        try:
            image_list = []
            buffer = get_buffer(file)
            doc = Document(io.BytesIO(buffer))
            content = self.to_md(doc, image_list, get_image_id_func())
            if len(image_list) > 0:
                save_image(image_list)
            if pattern_list is not None and len(pattern_list) > 0:
                split_model = SplitModel(pattern_list, with_filter, limit, overlap)
            else:
                split_model = SplitModel(default_pattern_list, with_filter=with_filter, limit=limit, overlap=overlap)
        except BaseException as e:
            traceback.print_exception(e)
            return {'name': file.name,
                    'content': []}
        return {'name': file.name,
                'content': split_model.parse(content)
                }

    def support(self, file, get_buffer):
        """  
        检查文件类型是否支持处理。  
        
        流程:  
        1. 获取文件名并转换为小写。  
        2. 检查文件名是否以.docx或.doc结尾。  
        3. 根据文件扩展名判断是否支持处理。  

        :param file: 文件对象。  
        :param get_buffer: 获取文件缓冲区的函数。  
        :return: 布尔值，表示文件是否支持处理。  
        """  
        file_name: str = file.name.lower()
        if file_name.endswith(".docx") or file_name.endswith(".doc"):
            return True
        return False
