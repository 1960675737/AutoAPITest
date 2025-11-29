"""
API基类
所有API类的基类，提供通用功能
"""
import requests
from typing import Dict, Any, Optional
from core.base.http_client import http_client
from core.utils.logger import logger


class BaseAPI:
    """API基类"""
    
    def __init__(self):
        """初始化API基类"""
        self.client = http_client
        self.logger = logger
    
    def _handle_response(self, response, expected_status_code: int = 200) -> Dict[str, Any]:
        """
        处理响应
        
        Args:
            response: requests.Response对象
            expected_status_code: 期望的状态码
            
        Returns:
            响应JSON数据
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}, 响应内容: {response.text}")
            raise
        except ValueError as e:
            self.logger.error(f"JSON解析错误: {e}, 响应内容: {response.text}")
            return {"text": response.text}
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """发送GET请求"""
        response = self.client.get(endpoint, params=params, headers=headers, **kwargs)
        return self._handle_response(response)
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None,
             data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None,
             **kwargs) -> Dict[str, Any]:
        """发送POST请求"""
        response = self.client.post(endpoint, json=json, data=data, headers=headers, **kwargs)
        return self._handle_response(response)
    
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None,
            data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None,
            **kwargs) -> Dict[str, Any]:
        """发送PUT请求"""
        response = self.client.put(endpoint, json=json, data=data, headers=headers, **kwargs)
        return self._handle_response(response)
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """发送DELETE请求"""
        response = self.client.delete(endpoint, params=params, headers=headers, **kwargs)
        return self._handle_response(response)
    
    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None,
              data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None,
              **kwargs) -> Dict[str, Any]:
        """发送PATCH请求"""
        response = self.client.patch(endpoint, json=json, data=data, headers=headers, **kwargs)
        return self._handle_response(response)

