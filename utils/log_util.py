# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: log_util.py
# @Software: PyCharm
# @Desc : 工具类

import os
import logging
import zipfile
import shutil
import time
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# ===================== 项目路径 =====================
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# ===================== 彩色日志格式 =====================
class ColorFormatter(logging.Formatter):
    grey = "\033[90m"
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"
    reset = "\033[0m"

    base_format = "%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + base_format + reset,
        logging.INFO: green + base_format + reset,
        logging.WARNING: yellow + base_format + reset,
        logging.ERROR: red + base_format + reset,
        logging.CRITICAL: red + base_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# ===================== Windows 安全日志切割 =====================
class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        if self.stream:
            try:
                self.stream.flush()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

        current_time = int(time.time())
        t = self.rolloverAt - self.interval
        time_tuple = time.localtime(t)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, time_tuple))

        if os.path.exists(dfn):
            pass
        elif os.path.exists(self.baseFilename):
            renamed = False
            for attempt in range(5):
                try:
                    os.rename(self.baseFilename, dfn)
                    renamed = True
                    break
                except PermissionError:
                    time.sleep(0.25)
            if not renamed:
                try:
                    shutil.copy2(self.baseFilename, dfn)
                    with open(self.baseFilename, 'w', encoding='utf-8') as f:
                        f.truncate(0)
                except Exception:
                    pass

            if self.backupCount > 0:
                for old in self.getFilesToDelete():
                    try:
                        os.remove(old)
                    except Exception:
                        pass

            self._compress(dfn)

        if not self.delay:
            self.stream = self._open()

        new_rollover = self.computeRollover(current_time)
        while new_rollover <= current_time:
            new_rollover += self.interval
        self.rolloverAt = new_rollover

    def _compress(self, file_path):
        try:
            zip_path = f"{file_path}.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(file_path, os.path.basename(file_path))
            os.remove(file_path)
        except Exception:
            pass

# ===================== 日志初始化 =====================
def setup_logger(service_name: str, log_level: str = "INFO") -> logging.Logger:
    logger=logging.getLogger(service_name)
    logger.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    logger.handlers.clear()

    file_fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s")

    # 主日志
    main_file = LOG_DIR / f"{service_name}.log"
    main_handler = SafeTimedRotatingFileHandler(
        filename=str(main_file),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
        delay=True
    )
    main_handler.setFormatter(file_fmt)
    logger.addHandler(main_handler)

    # 错误日志
    err_file = LOG_DIR / f"{service_name}.error.log"
    err_handler = SafeTimedRotatingFileHandler(
        filename=str(err_file),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
        delay=True
    )
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(file_fmt)
    logger.addHandler(err_handler)

    # 控制台彩色输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)

    return logger

# ===================== 工具函数 =====================
def clean_old_logs(days=30):
    expire = datetime.now() - timedelta(days=days)
    for f in LOG_DIR.glob("*.zip"):
        try:
            if datetime.fromtimestamp(f.stat().st_mtime) < expire:
                f.unlink()
        except Exception:
            pass

# ===================== 默认实例 =====================
logger = setup_logger("system")