"""
配置加载器
用于加载和管理配置文件
"""
import os
import yaml
from typing import Dict, Any


class ConfigLoader:
    """配置加载器类"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化配置加载器"""
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        # 获取项目根目录
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        config_path = os.path.join(project_root, "config", "config.yaml")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key_path: 配置键路径，使用点号分隔，如 'base.base_url'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            所有配置的字典
        """
        return self._config.copy()
    
    def reload(self):
        """重新加载配置"""
        self._load_config()


# 全局配置实例
config = ConfigLoader()

