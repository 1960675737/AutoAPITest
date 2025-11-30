"""
报表API
封装报表相关接口，包括历史订单等功能
"""
from typing import Dict, Any, Optional, List
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
        sort_rule: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        获取历史订单列表（分页）
        
        Args:
            page_num: 页码，从1开始，默认使用 DEFAULT_PAGE_NUM
            page_size: 每页大小，默认使用 DEFAULT_PAGE_SIZE
            start_date: 开始日期，格式：YYYY-MM-DD
            end_date: 结束日期，格式：YYYY-MM-DD
            order_status: 订单状态列表，如 [1, 2, 3]
            sort_rule: 排序规则，格式：{"field": "createTime", "order": "desc"}
            
        Returns:
            订单列表响应数据字典（已自动处理响应和错误）
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
        
        # 使用 BaseAPI 的 post 方法发送请求（自动处理响应和错误）
        response_data = self.post(self.history_order_list, json=payload)
        logger.info(f"查询历史订单列表成功")
        
        return response_data
    
    def report_order_listPage(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        /api/report/order/listPage - 获取历史订单列表
        使用 BaseAPI 的 post 方法，自动处理响应和错误
        
        Args:
            params: 参数字典，包含 pageNum, pageSize, startDate, endDate, orderStatus, sortRule 等
            
        Returns:
            响应数据字典（已通过 BaseAPI 的响应处理和错误处理）
            
        Note:
            BaseAPI.post() 已经自动处理了 HTTP 状态码验证和 JSON 解析
            如果请求失败会抛出异常，成功则返回解析后的字典
        """
        logger.info(f"[API调用] /api/report/order/listPage")
        logger.info(f"[请求参数] {params}")
        
        # 调用底层方法获取响应数据（使用 BaseAPI 的封装）
        response_data = self.get_order_list_page(
            page_num=params.get("pageNum", self.DEFAULT_PAGE_NUM),
            page_size=params.get("pageSize", self.DEFAULT_PAGE_SIZE),
            start_date=params.get("startDate"),
            end_date=params.get("endDate"),
            order_status=params.get("orderStatus"),
            sort_rule=params.get("sortRule")
        )
        
        logger.info(f"[API调用成功] 已获取响应数据")
        
        # 返回响应数据字典供测试用例进行业务逻辑断言
        return response_data

