"""
会话管理器
用于管理Token和会话信息
"""
import os
import time
from typing import Optional
from lib.utils.config_loader import config
from lib.utils.logger import logger


class SessionManager:
    """会话管理器类"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化会话管理器"""
        self._token: Optional[str] = None
        self._token_expire_time: Optional[float] = None
        self._token_storage = config.get('auth.token_storage', 'memory')
        self._token_file = config.get('auth.token_file', 'logs/token.txt')
        self._token_expire = config.get('auth.token_expire', 3600)
        
        # 如果使用文件存储，尝试从文件加载token
        if self._token_storage == 'file':
            self._load_token_from_file()
    
    def set_token(self, token: str):
        """
        设置Token
        
        Args:
            token: Token字符串
        """
        self._token = token
        
        # 计算过期时间
        if self._token_expire > 0:
            self._token_expire_time = time.time() + self._token_expire
        else:
            self._token_expire_time = None
        
        # 如果使用文件存储，保存到文件
        if self._token_storage == 'file':
            self._save_token_to_file()
        
        logger.info(f"Token已设置，过期时间: {self._token_expire_time}")
    
    def get_token(self) -> Optional[str]:
        """
        获取Token
        
        Returns:
            Token字符串，如果不存在或已过期返回None
        """
        # 检查Token是否过期
        if self._token_expire_time and time.time() > self._token_expire_time:
            logger.warning("Token已过期")
            self._token = None
            self._token_expire_time = None
            if self._token_storage == 'file':
                self._clear_token_file()
            return None
        
        return self._token
    
    def clear_token(self):
        """清除Token"""
        self._token = None
        self._token_expire_time = None
        
        if self._token_storage == 'file':
            self._clear_token_file()
        
        logger.info("Token已清除")
    
    def is_token_valid(self) -> bool:
        """
        检查Token是否有效
        
        Returns:
            True表示有效，False表示无效或已过期
        """
        token = self.get_token()
        return token is not None
    
    def _save_token_to_file(self):
        """保存Token到文件"""
        try:
            # 确保目录存在
            token_dir = os.path.dirname(self._token_file)
            if token_dir and not os.path.exists(token_dir):
                os.makedirs(token_dir, exist_ok=True)
            
            with open(self._token_file, 'w', encoding='utf-8') as f:
                f.write(f"{self._token}\n{self._token_expire_time or ''}")
            logger.debug(f"Token已保存到文件: {self._token_file}")
        except Exception as e:
            logger.error(f"保存Token到文件失败: {e}")
    
    def _load_token_from_file(self):
        """从文件加载Token"""
        try:
            if os.path.exists(self._token_file):
                with open(self._token_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        self._token = lines[0].strip()
                        if len(lines) > 1 and lines[1].strip():
                            self._token_expire_time = float(lines[1].strip())
                logger.debug(f"Token已从文件加载: {self._token_file}")
        except Exception as e:
            logger.error(f"从文件加载Token失败: {e}")
            self._token = None
            self._token_expire_time = None
    
    def _clear_token_file(self):
        """清除Token文件"""
        try:
            if os.path.exists(self._token_file):
                os.remove(self._token_file)
                logger.debug(f"Token文件已清除: {self._token_file}")
        except Exception as e:
            logger.error(f"清除Token文件失败: {e}")


# 全局会话管理器实例
session_manager = SessionManager()

