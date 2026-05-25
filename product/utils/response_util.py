# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: response_util.py
# @Software: PyCharm
# @Desc : 工具类

from typing import Any, Dict, List, Optional


class ResponseUtil:
    """
    响应工具类
    """

    @staticmethod
    def success(
        msg: str = '操作成功',
        data: Optional[List[Dict]] = None,
        total: Optional[int] = None,
        dict_content: Optional[Dict] = None,
        model_content: Optional[Any] = None,
    ) -> Dict:
        """
        成功响应
        """
        result = {
            'code': 200,
            'msg': msg,
        }
        
        if data is not None:
            result['data'] = data
        if total is not None:
            result['total'] = total
        if dict_content is not None:
            result.update(dict_content)
        if model_content is not None:
            result['data'] = model_content.model_dump(by_alias=True)
            
        return result

    @staticmethod
    def failure(msg: str = '操作失败') -> Dict:
        """
        失败响应
        """
        return {
            'code': 500,
            'msg': msg,
        }

    @staticmethod
    def error(msg: str = '系统错误') -> Dict:
        """
        错误响应
        """
        return {
            'code': 500,
            'msg': msg,
        }