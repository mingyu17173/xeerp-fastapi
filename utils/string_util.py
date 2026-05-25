# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: string_util.py
# @Software: PyCharm
# @Desc : 工具类

from typing import Dict, List, Optional
from utils.constant_util import CommonConstant


class StringUtil:
    """字符串工具类（企业增强版）"""

    @classmethod
    def is_blank(cls, string: Optional[str]) -> bool:
        """
        校验字符串是否为 None / 空 / 全空格
        修复原逻辑：None 应视为 blank
        """
        if string is None:
            return True
        return len(string.strip()) == 0

    @classmethod
    def is_not_blank(cls, string: Optional[str]) -> bool:
        return not cls.is_blank(string)

    @classmethod
    def is_empty(cls, string: Optional[str]) -> bool:
        """校验是否为 None 或 空字符串 ''"""
        return string is None or len(string) == 0

    @classmethod
    def is_not_empty(cls, string: Optional[str]) -> bool:
        return not cls.is_empty(string)

    @classmethod
    def is_http(cls, link: Optional[str]) -> bool:
        """判断是否以 http/https 开头"""
        if cls.is_blank(link):
            return False
        return link.startswith(CommonConstant.HTTP) or link.startswith(CommonConstant.HTTPS)

    # ====================== 忽略大小写判断 ======================
    @classmethod
    def contains_ignore_case(cls, search_str: Optional[str], compare_str: Optional[str]) -> bool:
        if cls.is_blank(search_str) or cls.is_blank(compare_str):
            return False
        return compare_str.lower() in search_str.lower()

    @classmethod
    def contains_any_ignore_case(cls, search_str: Optional[str], compare_str_list: List[str]) -> bool:
        if cls.is_blank(search_str) or not compare_str_list:
            return False
        return any(cls.contains_ignore_case(search_str, s) for s in compare_str_list)

    @classmethod
    def equals_ignore_case(cls, str1: Optional[str], str2: Optional[str]) -> bool:
        if str1 is None or str2 is None:
            return False
        return str1.lower() == str2.lower()

    @classmethod
    def equals_any_ignore_case(cls, search_str: Optional[str], compare_str_list: List[str]) -> bool:
        if cls.is_blank(search_str) or not compare_str_list:
            return False
        return any(cls.equals_ignore_case(search_str, s) for s in compare_str_list)

    # ====================== 开头匹配 ======================
    @classmethod
    def startswith_case(cls, search_str: Optional[str], prefix: Optional[str]) -> bool:
        if cls.is_blank(search_str) or cls.is_blank(prefix):
            return False
        return search_str.startswith(prefix)

    @classmethod
    def startswith_any_case(cls, search_str: Optional[str], prefix_list: List[str]) -> bool:
        if cls.is_blank(search_str) or not prefix_list:
            return False
        return any(search_str.startswith(p) for p in prefix_list)

    # ====================== 驼峰 / 下划线 转换 ======================
    @classmethod
    def to_camel_case(cls, name: Optional[str]) -> str:
        """下划线转大驼峰（兼容空、None、已驼峰字符串）"""
        if cls.is_blank(name):
            return ""

        name = name.strip().lower()
        if "_" not in name:
            return name.capitalize()

        return "".join(part.capitalize() for part in name.split("_") if part)

    # ====================== 字典忽略大小写查找 ======================
    @classmethod
    def get_mapping_value_by_key_ignore_case(
        cls,
        mapping: Dict[str, str],
        key: Optional[str]
    ) -> str:
        """按key忽略大小写获取字典值，不存在返回空串"""
        if cls.is_blank(key) or not mapping:
            return ""

        lower_key = key.lower()
        for k, v in mapping.items():
            if k.lower() == lower_key:
                return v

        return ""