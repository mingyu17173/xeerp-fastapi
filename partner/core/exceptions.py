# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: exceptions.py
# @Software: PyCharm
# @Desc : 核心配置

from fastapi import HTTPException, status

class PartnerNotFoundError(HTTPException):
    def __init__(self, detail: str = "往来单位不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PartnerCodeExistsError(HTTPException):
    def __init__(self, detail: str = "往来单位编码已存在"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InvalidPartnerTypeError(HTTPException):
    def __init__(self, detail: str = "无效的往来单位类型"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)