"""
账号配置加载器
用于加载和管理账号的请求头配置和URL参数配置
"""
import os
import yaml
from typing import Dict, Any, Optional


class AccountLoader:
    """账号配置加载器类"""
    
    _instance = None
    _account_config = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(AccountLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化账号配置加载器"""
        if self._account_config is None:
            self._load_account_config()
    
    def _load_account_config(self):
        """加载账号配置文件"""
        # 获取项目根目录
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        config_path = os.path.join(project_root, "config", "account_info_config.yaml")
        
        if not os.path.exists(config_path):
            # 如果配置文件不存在，使用空配置
            self._account_config = {"accounts": {"default": {"headers": {}}}}
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._account_config = yaml.safe_load(f) or {"accounts": {"default": {"headers": {}}}}
        except Exception as e:
            from core.utils.logger import logger
            logger.warning(f"加载账号配置文件失败: {e}，使用默认配置")
            self._account_config = {"accounts": {"default": {"headers": {}}}}
    
    def get_account_headers(self, account_name: str = "default") -> Dict[str, str]:
        """
        获取指定账号的请求头
        从配置文件中读取账号信息并映射为请求头字段：
        - account_id -> X-Saas-Account-Id
        - org_id -> X-Saas-Org-Id
        - store_id -> X-Saas-Store-Id
        - tenant_id -> X-Saas-Tenant-Id
        - Cookie -> Cookie (直接使用)
        
        Args:
            account_name: 账号名称，默认为 "default"
            
        Returns:
            账号的请求头字典
        """
        accounts = self._account_config.get("accounts", {})
        
        # 如果账号不存在，尝试使用默认账号
        if account_name not in accounts:
            if "default" in accounts:
                account_name = "default"
            else:
                return {}
        
        account_config = accounts.get(account_name, {})
        headers = {}
        
        # 字段映射关系
        field_mapping = {
            "account_id": "X-Saas-Account-Id",
            "org_id": "X-Saas-Org-Id",
            "store_id": "X-Saas-Store-Id",
            "tenant_id": "X-Saas-Tenant-Id"
        }
        
        # 映射字段到请求头
        for field, header_name in field_mapping.items():
            if field in account_config:
                headers[header_name] = str(account_config[field])
        
        # 直接使用Cookie字段（如果存在）
        if "Cookie" in account_config:
            headers["Cookie"] = account_config["Cookie"]
        
        return headers
    
    def get_account_params(self, account_name: str = "default") -> Dict[str, str]:
        """
        获取指定账号的URL查询参数
        自动提取配置中除预定义请求头字段外的所有字段作为URL参数
        配置文件中的参数名应与实际URL参数名保持一致
        
        Args:
            account_name: 账号名称，默认为 "default"
            
        Returns:
            账号的URL查询参数字典
            
        Example:
            配置文件中：
                account1:
                    org_id: "123"
                    wsgsig: "abc123"
                    custom_param: "value"
            
            返回的params：
                {"wsgsig": "abc123", "custom_param": "value"}
        """
        accounts = self._account_config.get("accounts", {})
        
        # 如果账号不存在，尝试使用默认账号
        if account_name not in accounts:
            if "default" in accounts:
                account_name = "default"
            else:
                return {}
        
        account_config = accounts.get(account_name, {})
        
        # 定义已知的请求头相关字段（这些字段不会被作为URL参数）
        header_fields = {
            "account_id",
            "org_id", 
            "store_id",
            "tenant_id",
            "Cookie"
        }
        
        # 提取所有非请求头字段作为URL参数
        params = {}
        for key, value in account_config.items():
            if key not in header_fields:
                params[key] = str(value)
        
        return params
    
    def get_all_accounts(self) -> Dict[str, Any]:
        """
        获取所有账号配置
        
        Returns:
            所有账号配置的字典
        """
        return self._account_config.get("accounts", {}).copy()
    
    def has_account(self, account_name: str) -> bool:
        """
        检查账号是否存在
        
        Args:
            account_name: 账号名称
            
        Returns:
            True表示存在，False表示不存在
        """
        accounts = self._account_config.get("accounts", {})
        return account_name in accounts
    
    def reload(self):
        """重新加载账号配置"""
        self._load_account_config()


# 全局账号配置实例
account_loader = AccountLoader()

