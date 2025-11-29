"""
断言助手
提供各种断言方法用于测试验证
"""
from typing import Any, Dict, List, Optional
from core.utils.logger import logger


class AssertHelper:
    """断言助手类"""
    
    @staticmethod
    def assert_status_code(response, expected_code: int):
        """
        断言HTTP状态码
        
        Args:
            response: requests.Response对象
            expected_code: 期望的状态码
        """
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"状态码断言失败: 期望 {expected_code}, 实际 {actual_code}"
        logger.info(f"✓ 状态码断言通过: {actual_code}")
    
    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = ""):
        """
        断言相等
        
        Args:
            actual: 实际值
            expected: 期望值
            message: 错误消息
        """
        assert actual == expected, \
            f"相等断言失败: 期望 {expected}, 实际 {actual}. {message}"
        logger.info(f"✓ 相等断言通过: {actual} == {expected}")
    
    @staticmethod
    def assert_not_equal(actual: Any, expected: Any, message: str = ""):
        """
        断言不相等
        
        Args:
            actual: 实际值
            expected: 期望值
            message: 错误消息
        """
        assert actual != expected, \
            f"不相等断言失败: 实际值 {actual} 不应该等于 {expected}. {message}"
        logger.info(f"✓ 不相等断言通过: {actual} != {expected}")
    
    @staticmethod
    def assert_in(item: Any, container: Any, message: str = ""):
        """
        断言包含
        
        Args:
            item: 要查找的项
            container: 容器（字符串、列表、字典等）
            message: 错误消息
        """
        assert item in container, \
            f"包含断言失败: {item} 不在 {container} 中. {message}"
        logger.info(f"✓ 包含断言通过: {item} 在容器中")
    
    @staticmethod
    def assert_not_in(item: Any, container: Any, message: str = ""):
        """
        断言不包含
        
        Args:
            item: 要查找的项
            container: 容器（字符串、列表、字典等）
            message: 错误消息
        """
        assert item not in container, \
            f"不包含断言失败: {item} 不应该在 {container} 中. {message}"
        logger.info(f"✓ 不包含断言通过: {item} 不在容器中")
    
    @staticmethod
    def assert_true(condition: bool, message: str = ""):
        """
        断言为真
        
        Args:
            condition: 条件
            message: 错误消息
        """
        assert condition is True, \
            f"真值断言失败: 条件为False. {message}"
        logger.info(f"✓ 真值断言通过")
    
    @staticmethod
    def assert_false(condition: bool, message: str = ""):
        """
        断言为假
        
        Args:
            condition: 条件
            message: 错误消息
        """
        assert condition is False, \
            f"假值断言失败: 条件为True. {message}"
        logger.info(f"✓ 假值断言通过")
    
    @staticmethod
    def assert_is_none(value: Any, message: str = ""):
        """
        断言为None
        
        Args:
            value: 值
            message: 错误消息
        """
        assert value is None, \
            f"None断言失败: 值 {value} 不是None. {message}"
        logger.info(f"✓ None断言通过")
    
    @staticmethod
    def assert_is_not_none(value: Any, message: str = ""):
        """
        断言不为None
        
        Args:
            value: 值
            message: 错误消息
        """
        assert value is not None, \
            f"非None断言失败: 值是None. {message}"
        logger.info(f"✓ 非None断言通过")
    
    @staticmethod
    def assert_response_json(response, expected: Dict[str, Any], 
                            check_keys: Optional[List[str]] = None):
        """
        断言响应JSON数据
        
        Args:
            response: requests.Response对象
            expected: 期望的JSON数据（部分匹配）
            check_keys: 需要检查的键列表，如果为None则检查expected中的所有键
        """
        try:
            actual = response.json()
        except ValueError:
            raise AssertionError(f"响应不是有效的JSON格式: {response.text}")
        
        if check_keys is None:
            check_keys = expected.keys()
        
        for key in check_keys:
            if key not in actual:
                raise AssertionError(f"响应中缺少键: {key}")
            if key in expected:
                AssertHelper.assert_equal(
                    actual[key], 
                    expected[key], 
                    f"键 '{key}' 的值不匹配"
                )
        
        logger.info(f"✓ JSON响应断言通过")
    
    @staticmethod
    def assert_response_contains(response, key: str, value: Any = None):
        """
        断言响应包含指定键（可选：值也匹配）
        
        Args:
            response: requests.Response对象
            key: 要检查的键
            value: 期望的值（可选）
        """
        try:
            actual = response.json()
        except ValueError:
            raise AssertionError(f"响应不是有效的JSON格式: {response.text}")
        
        assert key in actual, f"响应中缺少键: {key}"
        
        if value is not None:
            AssertHelper.assert_equal(actual[key], value, f"键 '{key}' 的值不匹配")
        
        logger.info(f"✓ 响应包含断言通过: {key}")
    
    @staticmethod
    def assert_response_code(response, expected_code: int):
        """
        断言响应中的code字段（业务状态码）
        
        Args:
            response: requests.Response对象
            expected_code: 期望的业务状态码
        """
        try:
            actual = response.json()
        except ValueError:
            raise AssertionError(f"响应不是有效的JSON格式: {response.text}")
        
        assert 'code' in actual, "响应中缺少 'code' 字段"
        AssertHelper.assert_equal(
            actual['code'], 
            expected_code, 
            "业务状态码不匹配"
        )
    
    @staticmethod
    def assert_response_message(response, expected_message: str, 
                               exact_match: bool = False):
        """
        断言响应中的message字段
        
        Args:
            response: requests.Response对象
            expected_message: 期望的消息（或消息的一部分）
            exact_match: 是否精确匹配
        """
        try:
            actual = response.json()
        except ValueError:
            raise AssertionError(f"响应不是有效的JSON格式: {response.text}")
        
        assert 'message' in actual, "响应中缺少 'message' 字段"
        
        if exact_match:
            AssertHelper.assert_equal(
                actual['message'], 
                expected_message, 
                "消息不匹配"
            )
        else:
            AssertHelper.assert_in(
                expected_message, 
                actual['message'], 
                "消息不包含期望的内容"
            )


# 全局断言助手实例
assert_helper = AssertHelper()

