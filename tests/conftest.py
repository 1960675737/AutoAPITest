"""
pytest 配置文件（必须放在 tests 目录）
定义全局 fixtures 和测试会话配置
"""
import pytest
from core.utils.logger import logger


@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """
    测试会话级别的设置
    在整个测试套件开始前和结束后执行
    """
    logger.info("=" * 60)
    logger.info("开始执行测试套件")
    logger.info("=" * 60)
    yield
    logger.info("=" * 60)
    logger.info("测试套件执行完成")
    logger.info("=" * 60)


@pytest.fixture(scope="function", autouse=True)
def test_case_log():
    """
    测试用例级别的日志分隔
    每个测试方法执行前后自动添加分隔线
    """
    logger.info("-" * 60)
    yield
    logger.info("-" * 60)


