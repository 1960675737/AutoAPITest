"""
测试运行入口
"""
import sys
import os
import pytest
from core.utils.logger import logger
from core.utils.config_loader import config


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("接口自动化测试框架")
    logger.info("=" * 60)
    
    # 获取测试目录
    test_dir = os.path.join(os.path.dirname(__file__), "tests")
    
    # 获取报告目录
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)
    
    # 构建pytest参数
    pytest_args = [
        test_dir,
        "-v",  # 详细输出
        "-s",  # 显示print输出
        "--tb=short",  # 简短的错误回溯
        f"--html={report_dir}/report.html",  # HTML报告
        "--self-contained-html",  # 独立的HTML报告
        f"--junitxml={report_dir}/report.xml",  # XML报告
    ]
    
    # 如果配置了日志级别，可以添加日志相关参数
    log_level = config.get('logging.level', 'INFO')
    if log_level:
        pytest_args.extend(["-o", f"log_cli_level={log_level}"])
    
    # 运行测试
    logger.info(f"开始运行测试，测试目录: {test_dir}")
    logger.info(f"报告将保存到: {report_dir}")
    
    exit_code = pytest.main(pytest_args)
    
    logger.info("=" * 60)
    if exit_code == 0:
        logger.info("所有测试通过！")
    else:
        logger.warning(f"测试执行完成，退出码: {exit_code}")
    logger.info("=" * 60)
    
    return exit_code


if __name__ == "__main__":
    print("开始运行测试")
    sys.exit(main())

