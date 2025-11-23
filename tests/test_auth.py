"""
认证测试用例
测试登录、登出等认证相关功能
"""
import pytest
import requests
from lib.apis.auth_api import AuthAPI
from lib.utils.yaml_loader import YamlLoader
from lib.utils.logger import logger
from lib.assert_helper import assert_helper


class TestAuth:
    """认证测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        cls.auth_api = AuthAPI()
        cls.test_data = YamlLoader.load_test_data("login_cases.yaml")
        logger.info("=" * 50)
        logger.info("开始执行认证测试")
        logger.info("=" * 50)
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        logger.info("=" * 50)
        logger.info("认证测试执行完成")
        logger.info("=" * 50)
    
    def setup_method(self):
        """每个测试方法执行前的初始化"""
        logger.info("-" * 50)
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        logger.info("-" * 50)
    
    def test_success_login(self):
        """测试成功登录"""
        case_name = "success_login"
        case_data = self.test_data[case_name]
        
        logger.info(f"执行测试用例: {case_name}")
        
        # 准备测试数据
        username = case_data["username"]
        password = case_data["password"]
        expected = case_data["expected"]
        
        # 执行登录
        response = self.auth_api.client.post(
            self.auth_api.login_endpoint,
            json={"username": username, "password": password}
        )
        
        # 断言状态码
        assert_helper.assert_status_code(response, expected.get("status_code", 200))
        
        # 断言响应数据
        response_data = response.json()
        
        if "code" in expected:
            assert_helper.assert_equal(
                response_data.get("code"), 
                expected["code"],
                "业务状态码不匹配"
            )
        
        if "message" in expected:
            assert_helper.assert_in(
                expected["message"],
                response_data.get("message", ""),
                "响应消息不匹配"
            )
        
        # 如果期望有Token，检查Token是否存在
        if expected.get("has_token", False):
            assert_helper.assert_true(
                self.auth_api.is_logged_in(),
                "登录后应该保存Token"
            )
        
        logger.info(f"✓ 测试用例 {case_name} 通过")
    
    def test_wrong_username(self):
        """测试用户名错误"""
        case_name = "wrong_username"
        case_data = self.test_data[case_name]
        
        logger.info(f"执行测试用例: {case_name}")
        
        username = case_data["username"]
        password = case_data["password"]
        expected = case_data["expected"]
        
        response = self.auth_api.client.post(
            self.auth_api.login_endpoint,
            json={"username": username, "password": password}
        )
        
        assert_helper.assert_status_code(response, expected.get("status_code", 200))
        
        response_data = response.json()
        
        if "code" in expected:
            assert_helper.assert_equal(
                response_data.get("code"),
                expected["code"],
                "业务状态码不匹配"
            )
        
        if "message" in expected:
            assert_helper.assert_in(
                expected["message"],
                response_data.get("message", ""),
                "响应消息不匹配"
            )
        
        logger.info(f"✓ 测试用例 {case_name} 通过")
    
    def test_wrong_password(self):
        """测试密码错误"""
        case_name = "wrong_password"
        case_data = self.test_data[case_name]
        
        logger.info(f"执行测试用例: {case_name}")
        
        username = case_data["username"]
        password = case_data["password"]
        expected = case_data["expected"]
        
        response = self.auth_api.client.post(
            self.auth_api.login_endpoint,
            json={"username": username, "password": password}
        )
        
        assert_helper.assert_status_code(response, expected.get("status_code", 200))
        
        response_data = response.json()
        
        if "code" in expected:
            assert_helper.assert_equal(
                response_data.get("code"),
                expected["code"],
                "业务状态码不匹配"
            )
        
        logger.info(f"✓ 测试用例 {case_name} 通过")
    
    def test_empty_username(self):
        """测试空用户名"""
        case_name = "empty_username"
        case_data = self.test_data[case_name]
        
        logger.info(f"执行测试用例: {case_name}")
        
        username = case_data["username"]
        password = case_data["password"]
        expected = case_data["expected"]
        
        response = self.auth_api.client.post(
            self.auth_api.login_endpoint,
            json={"username": username, "password": password}
        )
        
        assert_helper.assert_status_code(response, expected.get("status_code", 400))
        
        logger.info(f"✓ 测试用例 {case_name} 通过")
    
    def test_empty_password(self):
        """测试空密码"""
        case_name = "empty_password"
        case_data = self.test_data[case_name]
        
        logger.info(f"执行测试用例: {case_name}")
        
        username = case_data["username"]
        password = case_data["password"]
        expected = case_data["expected"]
        
        response = self.auth_api.client.post(
            self.auth_api.login_endpoint,
            json={"username": username, "password": password}
        )
        
        assert_helper.assert_status_code(response, expected.get("status_code", 400))
        
        logger.info(f"✓ 测试用例 {case_name} 通过")
    
    def test_logout(self):
        """测试登出"""
        logger.info("执行测试用例: test_logout")
        
        # 先登录
        self.auth_api.login("test_user", "test_password", auto_save_token=True)
        
        # 执行登出
        response = self.auth_api.client.post(self.auth_api.logout_endpoint)
        
        # 断言状态码
        assert_helper.assert_status_code(response, 200)
        
        # 断言Token已清除
        assert_helper.assert_false(
            self.auth_api.is_logged_in(),
            "登出后Token应该被清除"
        )
        
        logger.info("✓ 测试用例 test_logout 通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

