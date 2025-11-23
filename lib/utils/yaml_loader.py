"""
YAML文件加载器
用于加载测试数据文件
"""
import os
import yaml
from typing import Dict, Any, Optional


class YamlLoader:
    """YAML文件加载器类"""
    
    @staticmethod
    def load(file_path: str) -> Dict[str, Any]:
        """
        加载YAML文件
        
        Args:
            file_path: YAML文件路径（相对路径或绝对路径）
            
        Returns:
            解析后的字典数据
        """
        # 如果是相对路径，从项目根目录开始
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            file_path = os.path.join(project_root, file_path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_test_data(file_name: str) -> Dict[str, Any]:
        """
        加载测试数据文件
        
        Args:
            file_name: 测试数据文件名（如 'login_cases.yaml'）
            
        Returns:
            测试数据字典
        """
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        data_path = os.path.join(project_root, "data", file_name)
        return YamlLoader.load(data_path)
    
    @staticmethod
    def get_case_data(file_name: str, case_name: str) -> Optional[Dict[str, Any]]:
        """
        获取指定用例的数据
        
        Args:
            file_name: 测试数据文件名
            case_name: 用例名称
            
        Returns:
            用例数据字典，如果不存在返回None
        """
        data = YamlLoader.load_test_data(file_name)
        return data.get(case_name)

