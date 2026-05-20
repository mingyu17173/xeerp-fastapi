"""
统一日志工具模块
- 所有服务日志输出到项目根目录 logs/ 下
- 按服务名称生成日志文件：gateway.log, system.log, order.log 等
- 错误日志独立输出：gateway.error.log, system.error.log, order.error.log
- 每日自动压缩前一天的日志文件为 zip 格式
"""

import os
import logging
import zipfile
import shutil
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

# 确保日志目录存在
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志级别映射
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def setup_logger(service_name: str, log_level: str = 'INFO') -> logging.Logger:
    """
    配置服务日志记录器
    
    Args:
        service_name: 服务名称，用于生成日志文件名
        log_level: 日志级别，默认为 INFO
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(service_name)
    
    # 设置日志级别
    logger.setLevel(LOG_LEVELS.get(log_level.upper(), logging.INFO))
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 通用日志格式
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(module)s:%(funcName)s:%(lineno)d - %(message)s'
    )
    
    # 1. 主日志处理器：记录所有级别日志
    main_log_file = LOG_DIR / f"{service_name}.log"
    main_handler = TimedRotatingFileHandler(
        filename=main_log_file,
        when='midnight',       # 每天午夜轮换
        interval=1,            # 间隔1天
        backupCount=30,        # 保留30天日志
        encoding='utf-8',      # UTF-8编码
        delay=False            # 立即创建文件
    )
    main_handler.setFormatter(formatter)
    logger.addHandler(main_handler)
    
    # 2. 错误日志处理器：仅记录 ERROR 和 CRITICAL 级别
    error_log_file = LOG_DIR / f"{service_name}.error.log"
    error_handler = TimedRotatingFileHandler(
        filename=error_log_file,
        when='midnight',       # 每天午夜轮换
        interval=1,            # 间隔1天
        backupCount=30,        # 保留30天日志
        encoding='utf-8',      # UTF-8编码
        delay=False            # 立即创建文件
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)  # 只处理 ERROR 及以上级别
    logger.addHandler(error_handler)
    
    # 3. 控制台处理器：输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 设置自定义的日志轮换处理
    _setup_log_rotation(service_name, main_handler)
    _setup_log_rotation(f"{service_name}.error", error_handler)
    
    return logger

def _setup_log_rotation(base_name: str, handler: TimedRotatingFileHandler):
    """
    设置日志轮换处理，自动压缩旧日志
    
    Args:
        base_name: 基础文件名（不含.log后缀）
        handler: TimedRotatingFileHandler 实例
    """
    original_doRollover = handler.doRollover
    
    def custom_doRollover():
        # 执行原始的日志轮换
        original_doRollover()
        
        # 获取所有备份日志文件
        log_dir = LOG_DIR
        backup_pattern = f"{base_name}.log.*"
        
        for backup_file in log_dir.glob(backup_pattern):
            # 检查是否已经是压缩文件
            if backup_file.suffix == '.zip':
                continue
            
            # 检查是否已经处理过（以.processed结尾）
            if backup_file.suffix == '.processed':
                continue
            
            # 压缩备份文件
            zip_filename = str(backup_file) + '.zip'
            if not os.path.exists(zip_filename):
                try:
                    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(backup_file, backup_file.name)
                    
                    # 删除原备份文件
                    temp_file = backup_file.with_suffix('.processed')
                    backup_file.rename(temp_file)
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Failed to compress log file {backup_file}: {e}")
    
    handler.doRollover = custom_doRollover

def rotate_and_compress(service_name: str):
    """
    手动触发日志轮换并压缩
    
    Args:
        service_name: 服务名称
    """
    logger = logging.getLogger(service_name)
    for handler in logger.handlers:
        if isinstance(handler, TimedRotatingFileHandler):
            handler.doRollover()

def clean_old_logs(days_to_keep: int = 30):
    """
    清理指定天数前的日志文件
    
    Args:
        days_to_keep: 保留天数，默认30天
    """
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    
    for zip_file in LOG_DIR.glob('*.zip'):
        # 从文件名提取日期：服务名.log.YYYY-MM-DD.zip 或 服务名.error.log.YYYY-MM-DD.zip
        filename = zip_file.name
        
        # 尝试提取日期部分
        date_str = None
        
        # 模式1: gateway.log.2024-01-01.zip
        parts = filename.split('.')
        if len(parts) >= 4 and parts[-2] == 'log':
            date_str = parts[-3]
        # 模式2: gateway.error.log.2024-01-01.zip
        elif len(parts) >= 5 and parts[-2] == 'log':
            date_str = parts[-3]
        
        if date_str and date_str < cutoff_str:
            try:
                zip_file.unlink()
                print(f"Deleted old log: {zip_file}")
            except Exception as e:
                print(f"Failed to delete old log {zip_file}: {e}")

def get_log_file_path(service_name: str, error_log: bool = False) -> str:
    """
    获取服务日志文件路径
    
    Args:
        service_name: 服务名称
        error_log: 是否获取错误日志路径
    
    Returns:
        日志文件的绝对路径
    """
    if error_log:
        return str(LOG_DIR / f"{service_name}.error.log")
    return str(LOG_DIR / f"{service_name}.log")

def get_log_stats(service_name: str):
    """
    获取日志文件统计信息
    
    Args:
        service_name: 服务名称
    
    Returns:
        包含日志文件大小、最近修改时间等信息的字典
    """
    log_file = LOG_DIR / f"{service_name}.log"
    error_log_file = LOG_DIR / f"{service_name}.error.log"
    
    stats = {
        'service': service_name,
        'main_log': None,
        'error_log': None
    }
    
    if log_file.exists():
        stats['main_log'] = {
            'exists': True,
            'size': log_file.stat().st_size,
            'size_human': _format_size(log_file.stat().st_size),
            'last_modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat(),
            'file_path': str(log_file)
        }
    else:
        stats['main_log'] = {
            'exists': False,
            'size': 0,
            'size_human': '0 B',
            'last_modified': None,
            'file_path': str(log_file)
        }
    
    if error_log_file.exists():
        stats['error_log'] = {
            'exists': True,
            'size': error_log_file.stat().st_size,
            'size_human': _format_size(error_log_file.stat().st_size),
            'last_modified': datetime.fromtimestamp(error_log_file.stat().st_mtime).isoformat(),
            'file_path': str(error_log_file)
        }
    else:
        stats['error_log'] = {
            'exists': False,
            'size': 0,
            'size_human': '0 B',
            'last_modified': None,
            'file_path': str(error_log_file)
        }
    
    return stats

def _format_size(bytes_size: int) -> str:
    """
    将字节转换为人类可读的格式
    
    Args:
        bytes_size: 字节数
    
    Returns:
        人类可读的大小字符串
    """
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.2f} GB"

# 创建系统服务的默认日志记录器
logger = setup_logger('system')