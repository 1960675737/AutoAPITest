"""
测试辅助工具类
提供通用的测试断言和工具方法
"""
from core.utils.logger import logger
from core.assert_helper import assert_helper


class BaseTest:
    """测试基类，提供通用的测试方法"""
    
    @staticmethod
    def assert_success_response(response, expected_code="200"):
        """
        通用成功响应断言
        
        Args:
            response: HTTP 响应对象
            expected_code: 期望的业务状态码，默认 "200"
            
        Returns:
            响应数据字典
        """
        # HTTP 状态码断言
        assert_helper.assert_status_code(response, 200)
        
        # 响应数据断言
        response_data = response.json()
        assert_helper.assert_is_not_none(response_data, "响应数据不应为空")
        
        # 业务状态码断言
        if "code" in response_data:
            assert_helper.assert_equal(
                str(response_data.get("code")),
                expected_code,
                f"业务状态码应为'{expected_code}'"
            )
        
        return response_data
    
    @staticmethod
    def assert_fail_response(response, expected_code="400"):
        """
        通用失败响应断言
        
        Args:
            response: HTTP 响应对象
            expected_code: 期望的业务错误码，默认 "400"
            
        Returns:
            响应数据字典
        """
        # HTTP 状态码可能是 200，但业务状态码表示失败
        response_data = response.json()
        assert_helper.assert_is_not_none(response_data, "响应数据不应为空")
        
        # 业务状态码断言
        if "code" in response_data:
            assert_helper.assert_equal(
                str(response_data.get("code")),
                expected_code,
                f"业务状态码应为'{expected_code}'"
            )
        
        return response_data
    
    @staticmethod
    def log_data_count(response_data, data_key="listData"):
        """
        记录响应数据数量
        
        Args:
            response_data: 响应数据字典
            data_key: 数据列表的键名，默认 "listData"
        """
        if "data" not in response_data:
            return
        
        data = response_data["data"]
        
        # 处理不同的数据格式
        if isinstance(data, dict):
            # 优先使用指定的 data_key
            if data_key in data:
                count = len(data.get(data_key, []))
                logger.info(f"✓ 查询到 {count} 条记录")
            # 回退到 "list"
            elif "list" in data:
                count = len(data.get("list", []))
                logger.info(f"✓ 查询到 {count} 条记录")
            
            # 记录总数（如果有）
            if "totalCount" in data:
                logger.info(f"✓ 总记录数: {data['totalCount']}")
        elif isinstance(data, list):
            logger.info(f"✓ 查询到 {len(data)} 条记录")
    
    @staticmethod
    def extract_value(response_data, path, default=None):
        """
        从响应数据中提取值（支持嵌套路径）
        
        Args:
            response_data: 响应数据字典
            path: 路径，如 "data.user.name" 或 "data.list[0].id"
            default: 默认值
            
        Returns:
            提取的值，如果路径不存在返回 default
            
        Examples:
            >>> extract_value({"data": {"user": {"name": "test"}}}, "data.user.name")
            'test'
            >>> extract_value({"data": {"list": [{"id": 1}]}}, "data.list[0].id")
            1
        """
        try:
            keys = path.split('.')
            value = response_data
            
            for key in keys:
                # 处理数组索引，如 list[0]
                if '[' in key and ']' in key:
                    key_name, index = key.split('[')
                    index = int(index.rstrip(']'))
                    value = value[key_name][index]
                else:
                    value = value[key]
            
            return value
        except (KeyError, IndexError, TypeError):
            return default

