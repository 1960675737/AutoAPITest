"""
报表测试用例
测试历史订单列表等报表相关功能
"""
import pytest
from bizs.apis.report_api import ReportAPI
from bizs.apis.auth_api import AuthAPI
from core.utils.yaml_loader import YamlLoader
from core.utils.logger import logger
from core.assert_helper import assert_helper


class TestReport:
    """报表测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        # 使用默认账号，会自动加载 account_info_config.yaml 中的请求头
        cls.report_api = ReportAPI(account_name="default")
        cls.auth_api = AuthAPI()
        # 从 bizs/data/report_cases.yaml 加载测试数据
        cls.test_data = YamlLoader.load_test_data("report_cases.yaml")
        logger.info("=" * 50)
        logger.info("开始执行报表测试")
        logger.info(f"已加载测试数据: {list(cls.test_data.keys())}")
        logger.info("请求头将从 config/account_info_config.yaml 加载")
        logger.info("请求参数从 bizs/data/report_cases.yaml 读取")
        logger.info("=" * 50)
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        logger.info("=" * 50)
        logger.info("报表测试执行完成")
        logger.info("=" * 50)
    
    def setup_method(self):
        """每个测试方法执行前的初始化"""
        logger.info("-" * 50)
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        logger.info("-" * 50)
    
    def test_history_order_list_with_date_filter(self):
        """测试历史订单列表 - 指定时间筛选"""
        case_name = "history_order_list"
        case_key = "指定时间筛选"
        # 直接从 report_cases.yaml 读取参数
        case_data = self.test_data[case_name][case_key]
        
        logger.info(f"执行测试用例: {case_name} - {case_key}")
        logger.info(f"请求参数: {case_data}")
        
        # 直接从 YAML 文件读取的参数直接使用
        response = self.report_api.get_order_list_page_by_dict(
            params=case_data,
            return_response=True
        )
        
        # 断言状态码
        assert_helper.assert_status_code(response, 200)
        
        # 断言响应数据
        response_data = response.json()
        
        # 打印完整响应内容用于调试
        logger.info(f"完整响应数据: {response_data}")
        
        # 检查响应结构
        assert_helper.assert_is_not_none(
            response_data,
            "响应数据不应为空"
        )
        
        # 如果响应包含分页信息，进行断言
        if "code" in response_data:
            # 业务状态码可能是字符串 '200' 或整数 200
            code = response_data.get("code")
            # 转换为字符串进行比较，'200' 表示成功
            assert_helper.assert_equal(
                str(code),
                "200",
                "业务状态码应为'200'（成功）"
            )
        
        # 检查是否包含数据列表
        if "data" in response_data:
            data = response_data["data"]
            if isinstance(data, dict) and "list" in data:
                logger.info(f"查询到 {len(data.get('list', []))} 条订单记录")
            elif isinstance(data, list):
                logger.info(f"查询到 {len(data)} 条订单记录")
        
        logger.info(f"✓ 测试用例 {case_name} - {case_key} 通过")
    
    
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

