# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: common_util.py
# @Software: PyCharm
# @Desc : 工具类

import io
import os
import re
import pandas as pd
from typing import Any, Dict, List, Literal, Union
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.expression import TextClause, null
from typing import Any, Dict, List, Literal, Union
from core.database import Base
from core.env import CachePathConfig

def worship():
    print("""""")


class SqlalchemyUtil:
    """
    sqlalchemy工具类
    """

    @classmethod
    def base_to_dict(
        cls, obj: Union[Base, Dict], transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ):
        """
        将sqlalchemy模型对象转换为字典

        :param obj: sqlalchemy模型对象或普通字典
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 字典结果
        """
        if isinstance(obj, Base):
            base_dict = obj.__dict__.copy()
            base_dict.pop('_sa_instance_state', None)
            for name, value in base_dict.items():
                if isinstance(value, InstrumentedList):
                    base_dict[name] = cls.serialize_result(value, 'snake_to_camel')
        elif isinstance(obj, dict):
            base_dict = obj.copy()
        if transform_case == 'snake_to_camel':
            return {CamelCaseUtil.snake_to_camel(k): v for k, v in base_dict.items()}
        elif transform_case == 'camel_to_snake':
            return {SnakeCaseUtil.camel_to_snake(k): v for k, v in base_dict.items()}

        return base_dict

    @classmethod
    def serialize_result(
        cls, result: Any, transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ):
        """
        将sqlalchemy查询结果序列化

        :param result: sqlalchemy查询结果
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 序列化结果
        """
        if isinstance(result, (Base, dict)):
            return cls.base_to_dict(result, transform_case)
        elif isinstance(result, list):
            return [cls.serialize_result(row, transform_case) for row in result]
        elif isinstance(result, Row):
            if all([isinstance(row, Base) for row in result]):
                return [cls.base_to_dict(row, transform_case) for row in result]
            elif any([isinstance(row, Base) for row in result]):
                return [cls.serialize_result(row, transform_case) for row in result]
            else:
                result_dict = result._asdict()
                if transform_case == 'snake_to_camel':
                    return {CamelCaseUtil.snake_to_camel(k): v for k, v in result_dict.items()}
                elif transform_case == 'camel_to_snake':
                    return {SnakeCaseUtil.camel_to_snake(k): v for k, v in result_dict.items()}
                return result_dict
        return result

    @classmethod
    def get_server_default_null(cls, dialect_name: str, need_explicit_null: bool = True) -> Union[TextClause, None]:
        """
        根据数据库方言动态返回值为null的server_default

        :param dialect_name: 数据库方言名称
        :param need_explicit_null: 是否需要显式DEFAULT NULL
        :return: 不同数据库方言对应的null_server_default
        """
        if need_explicit_null and dialect_name == 'postgresql':
            return null()
        return None


class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str):
        """
        下划线形式字符串(snake_case)转换为小驼峰形式字符串(camelCase)

        :param snake_str: 下划线形式字符串
        :return: 小驼峰形式字符串
        """
        # 分割字符串
        words = snake_str.split('_')
        # 小驼峰命名，第一个词首字母小写，其余词首字母大写
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @classmethod
    def transform_result(cls, result: Any):
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='snake_to_camel')


class SnakeCaseUtil:
    """
    小驼峰形式(camelCase)转下划线形式(snake_case)工具方法
    """

    @classmethod
    def camel_to_snake(cls, camel_str: str):
        """
        小驼峰形式字符串(camelCase)转换为下划线形式字符串(snake_case)

        :param camel_str: 小驼峰形式字符串
        :return: 下划线形式字符串
        """
        # 在大写字母前添加一个下划线，然后将整个字符串转为小写
        words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', words).lower()

    @classmethod
    def transform_result(cls, result: Any):
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='camel_to_snake')



# ==============================
# 文件大小格式化
# ==============================
def bytes2human(n: int, format_str: str = "%(value).1f%(symbol)s") -> str:
    symbols = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    for i, s in enumerate(symbols[1:], start=1):
        if n < 1024 ** i:
            return format_str % {"value": n / (1024 ** (i - 1)), "symbol": symbols[i - 1]}
    return format_str % {"value": n, "symbol": symbols[0]}


def bytes2file_response(bytes_info):
    yield bytes_info


# ==============================
# Excel 导出（高性能 1万+ 行 ✅ 修复 fill 报错）
# ==============================
def export_list2excel(list_data: List[Dict]) -> bytes:
    if not list_data:
        return b""
    df = pd.DataFrame(list_data)
    bio = io.BytesIO()
    df.to_excel(bio, index=False, engine="openpyxl")
    return bio.getvalue()


# ==============================
# Excel 模板生成（✅ 彻底修复样式报错）
# ==============================
def get_excel_template(
        header_list: List[str],
        selector_header_list: List[str],
        option_list: List[Dict]
) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "导入模板"

    headers = header_list
    ws.append(headers)

    # 样式
    fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")
    align = Alignment(horizontal="center", vertical="center")

    # 【修复】先写入再设置样式，避免 cell.fill 报错
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = fill
        cell.alignment = align
        ws.column_dimensions[get_column_letter(col)].width = 18

    # 下拉框
    for head in selector_header_list:
        if head not in headers:
            continue
        idx = headers.index(head) + 1
        opts = []
        for o in option_list:
            if o.get(head):
                opts = o.get(head)
                break
        formula = '"' + ",".join(opts) + '"'
        dv = DataValidation(type="list", formula1=formula, allow_blank=True)
        col_name = get_column_letter(idx)
        dv.add(f"{col_name}2:{col_name}1048576")
        ws.add_data_validation(dv)

    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)
    return bio.getvalue()



def get_filepath_from_url(url: str):
    """
    工具方法：根据请求参数获取文件路径

    :param url: 请求参数中的url参数
    :return: 文件路径
    """
    file_info = url.split('?')[1].split('&')
    task_id = file_info[0].split('=')[1]
    file_name = file_info[1].split('=')[1]
    task_path = file_info[2].split('=')[1]
    filepath = os.path.join(CachePathConfig.PATH, task_path, task_id, file_name)

    return filepath
