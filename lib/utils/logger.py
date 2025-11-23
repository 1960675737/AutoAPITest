"""
日志工具
提供统一的日志记录功能
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from lib.utils.config_loader import config


class Logger:
    """日志工具类"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str = "api_test") -> logging.Logger:
        """
        获取日志记录器（单例模式）
        
        Args:
            name: 日志记录器名称
            
        Returns:
            logging.Logger实例
        """
        if name not in Logger._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, config.get('logging.level', 'INFO')))
            
            # 避免重复添加handler
            if logger.handlers:
                return logger
            
            # 日志格式
            formatter = logging.Formatter(
                config.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            
            # 控制台输出
            if config.get('logging.console', True):
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.DEBUG)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)
            
            # 文件输出
            log_file = config.get('logging.file_path', 'logs/api_test.log')
            if log_file:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                
                # 使用RotatingFileHandler实现日志轮转
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=10 * 1024 * 1024,  # 10MB
                    backupCount=5,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            
            Logger._loggers[name] = logger
        
        return Logger._loggers[name]


# 全局日志实例
logger = Logger.get_logger()

