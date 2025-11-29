"""
报表API
封装报表相关接口，包括历史订单等功能
"""
import requests
from typing import Dict, Any, Optional, Union, List
from core.base.base_api import BaseAPI
from core.base.session_manager import session_manager
from core.utils.logger import logger


class ReportAPI(BaseAPI):
    """
    报表API类
    每个报表API接口命名需要与接口文档一致
    例如：/api/report/order/listPage 对应的方法名称为 report_order_listPage
    """
    
    # ===== 默认参数配置（集中管理默认值）=====
    DEFAULT_PAGE_NUM = 1
    DEFAULT_PAGE_SIZE = 50
    
    def __init__(self, account_name: str = "default"):
        """
        初始化报表API
        
        Args:
            account_name: 账号名称，用于加载对应的请求头配置
        """
        super().__init__()
        self.history_order_list = "/api/report/order/listPage"
        
        # 设置账号，加载对应的请求头和请求参数
        self.set_account(account_name)
    
    def set_account(self, account_name: str):
        """
        切换账号，加载对应的请求头和请求参数配置
        
        Args:
            account_name: 账号名称
        """
        session_manager.set_account(account_name)
        logger.info(f"ReportAPI已切换到账号: {account_name}")
    
    def get_order_list_page(
        self,
        page_num: int = None,
        page_size: int = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        order_status: Optional[List[int]] = None,
        sort_rule: Optional[Dict[str, str]] = None,
        return_response: bool = False
    ) -> Union[Dict[str, Any], requests.Response]:
        """
        获取历史订单列表（分页）
        
        Args:
            page_num: 页码，从1开始，默认使用 DEFAULT_PAGE_NUM
            page_size: 每页大小，默认使用 DEFAULT_PAGE_SIZE
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            order_status: 订单状态列表，如 [1, 2, 3]
            sort_rule: 排序规则，格式：{"field": "createTime", "order": "desc"}
            return_response: 是否返回响应对象（用于测试）
            
        Returns:
            如果 return_response=True，返回 requests.Response 对象
            否则返回订单列表响应数据字典
        """
        # 使用类常量作为默认值
        page_num = page_num if page_num is not None else self.DEFAULT_PAGE_NUM
        page_size = page_size if page_size is not None else self.DEFAULT_PAGE_SIZE
        
        logger.info(f"开始查询历史订单列表，页码: {page_num}, 每页大小: {page_size}")
        
        # 构建请求参数
        payload: Dict[str, Any] = {
            "pageNum": page_num,
            "pageSize": page_size
        }
        
        # 添加可选参数
        if start_date:
            payload["startDate"] = start_date
            logger.debug(f"开始日期: {start_date}")
        
        if end_date:
            payload["endDate"] = end_date
            logger.debug(f"结束日期: {end_date}")
        
        if order_status is not None:
            payload["orderStatus"] = order_status
            logger.debug(f"订单状态: {order_status}")
        
        if sort_rule is not None:
            payload["sortRule"] = sort_rule
            logger.debug(f"排序规则: {sort_rule}")
        
        # 发送POST请求
        response = self.client.post(self.history_order_list, json=payload)
        
        # 如果要求返回响应对象，直接返回
        if return_response:
            return response
        
        # 处理响应
        try:
            response_data = response.json()
            logger.info(f"查询历史订单列表成功，状态码: {response.status_code}")
            return response_data
        except ValueError:
            # 如果不是JSON响应，返回文本
            logger.warning(f"响应不是JSON格式: {response.text[:200]}")
            return {"text": response.text, "status_code": response.status_code}
    
    def report_order_listPage(
        self,
        params: Dict[str, Any]
    ) -> requests.Response:
        """
        /api/report/order/listPage - 获取历史订单列表
        内置基础断言：状态码验证
        
        Args:
            params: 参数字典，包含 pageNum, pageSize, startDate, endDate, orderStatus, sortRule 等
            
        Returns:
            requests.Response 对象（已通过状态码断言）
            
        Raises:
            AssertionError: 当状态码不符合预期时抛出
        """
        logger.info(f"[API调用] /api/report/order/listPage")
        logger.info(f"[请求参数] {params}")
        
        # 调用底层方法获取响应
        response = self.get_order_list_page(
            page_num=params.get("pageNum", self.DEFAULT_PAGE_NUM),
            page_size=params.get("pageSize", self.DEFAULT_PAGE_SIZE),
            start_date=params.get("startDate"),
            end_date=params.get("endDate"),
            order_status=params.get("orderStatus"),
            sort_rule=params.get("sortRule"),
            return_response=True
        )
        
        # 基础断言：状态码验证
        actual_status_code = response.status_code
        assert actual_status_code == 200, (
            f"状态码断言失败！返回状态码: {actual_status_code}, "
            f"响应内容: {response.text[:200]}"
        )
        logger.info(f"[状态码断言] ✓ 通过 - 状态码: {actual_status_code}")
        
        # 返回响应对象供测试用例进行业务逻辑断言
        return response

