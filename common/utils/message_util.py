# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: message_util.py
# @Software: PyCharm
# @Desc : 工具类

from utils.log_util import logger


def message_service(sms_code: str):
    logger.info(f'短信验证码为{sms_code}')
