"""
HTTP客户端
提供通用的HTTP请求封装
"""
import requests
from typing import Dict, Any, Optional
from lib.utils.config_loader import config
from lib.utils.logger import logger
from lib.core.session_manager import session_manager


class HttpClient:
    """HTTP客户端类"""
    
    def __init__(self):
        """初始化HTTP客户端"""
        self.base_url = config.get('base.base_url', '')
        self.timeout = config.get('base.timeout', 30)
        self.verify_ssl = config.get('base.verify_ssl', True)
        self.session = requests.Session()
    
    def _get_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        获取请求头（自动添加Token）
        
        Args:
            headers: 自定义请求头
            
        Returns:
            完整的请求头字典
        """
        default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 自动添加Token
        token = session_manager.get_token()
        if token:
            default_headers['Authorization'] = f'Bearer {token}'
        
        # 合并自定义请求头
        if headers:
            default_headers.update(headers)
        
        return default_headers
    
    def _build_url(self, endpoint: str) -> str:
        """
        构建完整URL
        
        Args:
            endpoint: API端点路径
            
        Returns:
            完整的URL
        """
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求日志"""
        logger.info(f"[请求] {method.upper()} {url}")
        if 'json' in kwargs:
            logger.debug(f"[请求体] {kwargs['json']}")
        if 'params' in kwargs:
            logger.debug(f"[请求参数] {kwargs['params']}")
        if 'headers' in kwargs:
            logger.debug(f"[请求头] {kwargs['headers']}")
    
    def _log_response(self, response: requests.Response):
        """记录响应日志"""
        logger.info(f"[响应] 状态码: {response.status_code}")
        try:
            logger.debug(f"[响应体] {response.json()}")
        except:
            logger.debug(f"[响应体] {response.text[:500]}")
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法（GET, POST, PUT, DELETE等）
            endpoint: API端点路径
            params: URL参数
            json: JSON请求体
            data: 表单数据
            headers: 自定义请求头
            **kwargs: 其他requests参数
            
        Returns:
            requests.Response对象
        """
        url = self._build_url(endpoint)
        request_headers = self._get_headers(headers)
        
        # 记录请求日志
        self._log_request(method, url, params=params, json=json, data=data, headers=request_headers)
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=json,
                data=data,
                headers=request_headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            
            # 记录响应日志
            self._log_response(response)
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self.request('GET', endpoint, params=params, headers=headers, **kwargs)
    
    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None,
             data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None,
             **kwargs) -> requests.Response:
        """发送POST请求"""
        return self.request('POST', endpoint, json=json, data=data, headers=headers, **kwargs)
    
    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None,
            data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None,
            **kwargs) -> requests.Response:
        """发送PUT请求"""
        return self.request('PUT', endpoint, json=json, data=data, headers=headers, **kwargs)
    
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        return self.request('DELETE', endpoint, params=params, headers=headers, **kwargs)
    
    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None,
              data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None,
              **kwargs) -> requests.Response:
        """发送PATCH请求"""
        return self.request('PATCH', endpoint, json=json, data=data, headers=headers, **kwargs)


# 全局HTTP客户端实例
http_client = HttpClient()

