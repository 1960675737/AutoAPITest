"""
报表测试用例
测试历史订单列表等报表相关功能
"""
import pytest
from bizs.apis.report_api import ReportAPI
from core.utils.yaml_loader import YamlLoader
from core.utils.logger import logger
from core.test_helper import BaseTest
from core.assert_helper import assert_helper


@pytest.fixture(scope="class")
def report_api():
    """报表 API fixture"""
    return ReportAPI(account_name="default")


@pytest.fixture(scope="class")
def test_data():
    """测试数据 fixture"""
    return YamlLoader.load_test_data("report_cases.yaml")


class TestReport(BaseTest):
    """报表测试类"""
    
    def test_history_order_list_with_date_filter(self, report_api, test_data):
        """测试历史订单列表 - 指定时间筛选"""
        # 1. 获取测试数据
        case_data = test_data["history_order_list"]["指定时间筛选"]
        logger.info(f"请求参数: {case_data}")
        
        # 2. 调用API（使用 BaseAPI 的 post 方法，自动处理响应和错误）
        response_data = report_api.report_order_listPage(params=case_data)
        
        # 3. 断言响应数据
        assert_helper.assert_is_not_none(response_data, "响应数据不应为空")
        
        # 业务状态码断言
        if "code" in response_data:
            assert_helper.assert_equal(
                str(response_data.get("code")),
                "200",
                f"业务状态码应为'200'"
            )
            logger.info(f"[业务状态码断言] ✓ 通过 - 状态码: {response_data.get('code')}")
        
        # 4. 记录数据数量
        self.log_data_count(response_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

