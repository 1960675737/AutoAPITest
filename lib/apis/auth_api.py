"""
认证API
封装登录、登出等认证相关接口
"""
from typing import Dict, Any, Optional
from lib.core.base_api import BaseAPI
from lib.core.session_manager import session_manager
from lib.utils.logger import logger


class AuthAPI(BaseAPI):
    """认证API类"""
    
    def __init__(self):
        """初始化认证API"""
        super().__init__()
        self.login_endpoint = "/api/auth/login"
        self.logout_endpoint = "/api/auth/logout"
        self.refresh_token_endpoint = "/api/auth/refresh"
    
    def login(self, username: str, password: str, 
              auto_save_token: bool = True) -> Dict[str, Any]:
        """
        登录接口
        
        Args:
            username: 用户名
            password: 密码
            auto_save_token: 是否自动保存Token
            
        Returns:
            登录响应数据
        """
        logger.info(f"开始登录，用户名: {username}")
        
        payload = {
            "username": username,
            "password": password
        }
        
        response = self.client.post(self.login_endpoint, json=payload)
        
        # 处理响应
        try:
            response_data = response.json()
            
            # 如果登录成功且需要自动保存Token
            if auto_save_token and response.status_code == 200:
                # 尝试从响应中提取Token
                token = self._extract_token(response_data)
                if token:
                    session_manager.set_token(token)
                    logger.info("Token已自动保存")
            
            return response_data
            
        except ValueError:
            # 如果不是JSON响应，返回文本
            return {"text": response.text, "status_code": response.status_code}
    
    def logout(self) -> Dict[str, Any]:
        """
        登出接口
        
        Returns:
            登出响应数据
        """
        logger.info("开始登出")
        
        response = self.client.post(self.logout_endpoint)
        
        # 清除Token
        session_manager.clear_token()
        logger.info("Token已清除")
        
        try:
            return response.json()
        except ValueError:
            return {"text": response.text, "status_code": response.status_code}
    
    def refresh_token(self) -> Dict[str, Any]:
        """
        刷新Token接口
        
        Returns:
            刷新Token响应数据
        """
        logger.info("开始刷新Token")
        
        response = self.client.post(self.refresh_token_endpoint)
        
        try:
            response_data = response.json()
            
            # 如果刷新成功，更新Token
            if response.status_code == 200:
                token = self._extract_token(response_data)
                if token:
                    session_manager.set_token(token)
                    logger.info("Token已刷新")
            
            return response_data
            
        except ValueError:
            return {"text": response.text, "status_code": response.status_code}
    
    def _extract_token(self, response_data: Dict[str, Any]) -> Optional[str]:
        """
        从响应数据中提取Token
        
        Args:
            response_data: 响应数据字典
            
        Returns:
            Token字符串，如果不存在返回None
        """
        # 常见的Token字段名
        token_fields = ['token', 'access_token', 'accessToken', 'auth_token', 'authToken']
        
        for field in token_fields:
            if field in response_data:
                token = response_data[field]
                if isinstance(token, str) and token:
                    return token
        
        # 如果响应数据中有data字段，尝试从data中提取
        if 'data' in response_data and isinstance(response_data['data'], dict):
            for field in token_fields:
                if field in response_data['data']:
                    token = response_data['data'][field]
                    if isinstance(token, str) and token:
                        return token
        
        return None
    
    def is_logged_in(self) -> bool:
        """
        检查是否已登录（通过Token判断）
        
        Returns:
            True表示已登录，False表示未登录
        """
        return session_manager.is_token_valid()

