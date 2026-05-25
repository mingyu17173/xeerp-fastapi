# -*- coding: utf-8 -*-
from datetime import datetime, date


class DateTimeUtil:

    @staticmethod
    def now() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def today() -> str:
        return date.today().strftime("%Y-%m-%d")

    @staticmethod
    def format(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(fmt)