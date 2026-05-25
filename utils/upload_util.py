# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : ERP微服务开发组
# @FileName: upload_util.py
# @Software: PyCharm
# @Desc : 工具类

import os
import random
import shutil
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from utils.constant_util import HttpStatusConstant, UploadSettings


class UploadUtil:
    """
    安全上传工具类
    功能：文件头校验防改后缀木马、危险文件拦截、文件大小限制、流式读写
    """

    # 文件头白名单，校验真实文件格式
    ALLOWED_FILE_HEADERS = {
        # 图片
        "jpg": ["FFD8FF"],
        "jpeg": ["FFD8FF"],
        "png": ["89504E47"],
        "gif": ["47494638"],
        "bmp": ["424D"],
        "webp": ["52494646"],
        # 压缩包
        "zip": ["504B0304", "504B0506", "504B0708"],
        "rar": ["52617221"],
        "7z": ["377ABCAF271C"],
        "tar": ["75737461"],
        "gz": ["1F8B"],
        # 文档
        "pdf": ["25504446"],
        "doc": ["D0CF11E0"],
        "docx": ["504B0304"],
        "xls": ["D0CF11E0"],
        "xlsx": ["504B0304"],
        "ppt": ["D0CF11E0"],
        "pptx": ["504B0304"],
        "txt": [""],
        "md": [""],
    }

    # 高危可执行脚本后缀，直接拦截
    DANGEROUS_EXTENSIONS = {
        "exe", "bat", "cmd", "sh", "py", "php", "jsp", "asp", "aspx",
        "dll", "so", "com", "vbs", "js", "jar", "war", "html", "htm"
    }

    @classmethod
    def generate_random_number(cls, length: int = 3) -> str:
        return f"{random.randint(0, 10**length - 1):0{length}d}"

    @classmethod
    def check_file_exists(cls, filepath: str) -> bool:
        return os.path.isfile(filepath)

    @classmethod
    async def check_file_real_type(cls, file: UploadFile, ext: str):
        if ext not in cls.ALLOWED_FILE_HEADERS:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "不支持的文件类型")

        file.file.seek(0)
        header_bytes = file.file.read(16)
        file.file.seek(0)

        if not header_bytes:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "禁止上传空文件")

        header_hex = header_bytes.hex().upper()
        allowed_headers = cls.ALLOWED_FILE_HEADERS[ext]
        match_flag = any(header_hex.startswith(h) for h in allowed_headers)

        if not match_flag:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "文件格式异常，拦截恶意文件")

    @classmethod
    def check_file_extension(cls, file: UploadFile) -> bool:
        if not file.filename or "." not in file.filename:
            return False
        ext = file.filename.strip().lower().rsplit(".", 1)[-1]
        if ext in cls.DANGEROUS_EXTENSIONS:
            return False
        return ext in UploadSettings.DEFAULT_ALLOWED_EXTENSION

    @classmethod
    def get_file_extension(cls, file: UploadFile) -> str:
        return file.filename.strip().lower().rsplit(".", 1)[-1]

    @classmethod
    async def check_file_size(cls, file: UploadFile):
        """校验文件大小，超出限制直接拦截"""
        file_size = await file.read()
        size_len = len(file_size)
        # 重置文件指针
        await file.seek(0)
        if size_len > UploadSettings.MAX_FILE_SIZE:
            max_mb = UploadSettings.MAX_FILE_SIZE / 1024 / 1024
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"文件过大，最大允许{max_mb}MB")

    @classmethod
    def create_folder(cls, folder_path: str):
        os.makedirs(folder_path, exist_ok=True)

    @classmethod
    def generate_save_filename(cls, ext: str) -> str:
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = cls.generate_random_number(3)
        return f"{time_str}_{random_str}.{ext}"

    @classmethod
    async def save_upload_file(
        cls,
        file: UploadFile,
        save_folder: str,
        filename: str = None
    ) -> tuple[str, str]:
        if not file or not file.filename:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "文件不能为空")

        # 1.后缀校验
        if not cls.check_file_extension(file):
            raise HTTPException(HttpStatusConstant.BAD_REQUEST, "文件格式非法或存在风险")
        ext = cls.get_file_extension(file)

        # 2.大小校验
        await cls.check_file_size(file)

        # 3.真实文件头校验
        await cls.check_file_real_type(file, ext)

        # 4.创建目录并保存
        cls.create_folder(save_folder)
        save_filename = filename or cls.generate_save_filename(ext)
        save_path = os.path.join(save_folder, save_filename)

        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return save_path, save_filename

    @classmethod
    def delete_file(cls, filepath: str):
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
        except Exception:
            pass

    @classmethod
    async def generate_file_stream(cls, filepath: str):
        if not cls.check_file_exists(filepath):
            raise HTTPException(404, "文件不存在")
        with open(filepath, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk