# AutoAPI - 接口自动化测试框架

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![pytest](https://img.shields.io/badge/pytest-9.0+-green.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

一个基于 Python 和 Pytest 的现代化接口自动化测试框架，提供完整的 API 测试解决方案。

## ✨ 核心特性

### 🚀 高效便捷
- **多账号支持** - 灵活切换不同测试账号，支持请求头和 URL 参数自动配置
- **智能 Token 管理** - 自动管理认证 Token，支持内存/文件存储
- **统一 HTTP 封装** - 自动添加请求头、Cookie、URL 参数，简化接口调用

### 🎯 测试友好
- **Pytest 深度集成** - 使用 fixtures、参数化等 pytest 最佳实践
- **数据驱动测试** - YAML 格式测试数据，支持复杂场景配置
- **丰富的断言方法** - 提供多种开箱即用的断言工具

### 📊 易于维护
- **清晰的分层架构** - Core 核心层、Bizs 业务层、Tests 测试层
- **测试基类复用** - BaseTest 提供通用断言和数据处理方法
- **完善的日志记录** - 详细的请求/响应日志，便于问题排查

---

## 📁 项目结构

```
AutoAPI/
├── core/                          # 核心层（通用工具和基础设施）
│   ├── base/                      # 基础模块
│   │   ├── base_api.py           # API 基类
│   │   ├── http_client.py        # HTTP 客户端封装
│   │   └── session_manager.py    # 会话管理（Token、账号）
│   ├── utils/                     # 工具模块
│   │   ├── account_loader.py     # 账号配置加载器
│   │   ├── config_loader.py      # 配置文件加载器
│   │   ├── logger.py             # 日志工具
│   │   └── yaml_loader.py        # YAML 数据加载器
│   ├── assert_helper.py          # 断言辅助工具
│   └── test_helper.py            # 测试辅助工具（BaseTest）
├── bizs/                          # 业务层（API 封装和测试数据）
│   ├── apis/                      # API 封装
│   │   └── report_api.py         # 报表接口
│   └── data/                      # 测试数据
│       └── report_cases.yaml     # 报表测试数据
├── tests/                         # 测试层（测试用例）
│   ├── conftest.py               # pytest 配置（fixtures）
│   ├── test_report.py            # 报表测试用例
│   └── README.md                 # 测试编写指南
├── config/                        # 配置文件
│   ├── config.yaml               # 框架配置
│   └── account_info_config.yaml  # 账号配置（请求头、Cookie）
├── logs/                          # 日志文件
├── reports/                       # 测试报告
├── run.py                         # 测试运行入口
├── requirements.txt               # Python 依赖
└── README.md                      # 项目文档
```

### 📂 目录说明

| 目录/文件 | 说明 |
|----------|------|
| `core/` | 核心层，包含通用工具、基础设施，可复用于任何项目 |
| `bizs/` | 业务层，包含 API 封装和测试数据，与具体业务相关 |
| `tests/` | 测试层，包含测试用例和 pytest 配置 |
| `config/` | 配置文件，包括框架配置和账号配置 |

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.13+
- pip

### 2. 安装依赖

```bash
# 克隆项目
git clone git@github.com:1960675737/AutoAPITest.git
cd AutoAPI

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置框架

#### 编辑 `config/config.yaml`

```yaml
base:
  base_url: "https://admin-api.zaporder.com"  # API 基础 URL
  timeout: 30                                  # 请求超时（秒）
  verify_ssl: true                            # 是否验证 SSL 证书

logging:
  level: "INFO"                               # 日志级别
  file: "logs/api_test.log"                  # 日志文件路径
```

#### 编辑 `config/account_info_config.yaml`

```yaml
accounts:
  default:  # 默认账号
    org_id: "your_org_id"
    account_id: "your_account_id"
    store_id: "your_store_id"
    tenant_id: "your_tenant_id"
    wsgsig: "your_wsgsig_param"              # URL 查询参数
    Cookie: "your_cookie_string"             # Cookie 字符串
```

### 4. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个测试文件
pytest tests/test_report.py -v

# 显示详细输出（包括日志）
pytest tests/test_report.py -v -s

# 生成 HTML 测试报告
pytest tests/ -v --html=reports/report.html --self-contained-html
```

---

## 🔧 核心模块详解

### 1. HTTP 客户端 (`core/base/http_client.py`)

提供统一的 HTTP 请求封装，自动处理：

- ✅ 自动添加账号请求头（X-Saas-Account-Id 等）
- ✅ 自动添加 URL 参数（wsgsig 等）
- ✅ 自动添加 Cookie
- ✅ 自动添加 Token（如果有）
- ✅ 详细的请求/响应日志

**使用示例：**

```python
from core.base.http_client import http_client

# GET 请求
response = http_client.get("/api/users/123")

# POST 请求（JSON）
response = http_client.post(
    "/api/users",
    json={"name": "test", "age": 25}
)

# 带自定义请求头
response = http_client.post(
    "/api/data",
    json={"key": "value"},
    headers={"Custom-Header": "value"}
)
```

---

### 2. 会话管理器 (`core/base/session_manager.py`)

管理 Token 和账号配置：

- ✅ Token 存储（内存/文件）
- ✅ Token 自动过期检查
- ✅ 多账号切换
- ✅ 请求头和 URL 参数自动加载

**使用示例：**

```python
from core.base.session_manager import session_manager

# 设置 Token
session_manager.set_token("your_token_here")

# 获取 Token
token = session_manager.get_token()

# 切换账号
session_manager.set_account("account_name")

# 获取当前账号的请求头
headers = session_manager.get_account_headers()

# 获取当前账号的 URL 参数
params = session_manager.get_account_params()
```

---

### 3. 账号配置加载器 (`core/utils/account_loader.py`)

自动加载并映射账号配置：

**字段映射：**

| 配置字段 | 映射到请求头 |
|----------|-------------|
| `account_id` | `X-Saas-Account-Id` |
| `org_id` | `X-Saas-Org-Id` |
| `store_id` | `X-Saas-Store-Id` |
| `tenant_id` | `X-Saas-Tenant-Id` |
| `Cookie` | `Cookie` |
| `wsgsig` | URL 参数 `wsgsig` |

---

### 4. 测试基类 (`core/test_helper.py`)

提供通用的测试方法，减少重复代码：

**主要方法：**

```python
from core.test_helper import BaseTest

class TestYourAPI(BaseTest):
    def test_something(self):
        # 1. 断言成功响应
        response_data = self.assert_success_response(response)
        
        # 2. 断言失败响应
        response_data = self.assert_fail_response(response, expected_code="400")
        
        # 3. 记录数据数量
        self.log_data_count(response_data)
        
        # 4. 提取嵌套值
        user_name = self.extract_value(response_data, "data.user.name")
        first_id = self.extract_value(response_data, "data.list[0].id")
```

---

### 5. 断言助手 (`core/assert_helper.py`)

提供丰富的断言方法：

```python
from core.assert_helper import assert_helper

# 状态码断言
assert_helper.assert_status_code(response, 200)

# 相等断言
assert_helper.assert_equal(actual, expected, "错误消息")

# 包含断言
assert_helper.assert_in(item, container, "错误消息")

# 非空断言
assert_helper.assert_is_not_none(value, "错误消息")

# JSON 响应断言
assert_helper.assert_response_json(response, "key", "expected_value")
```

---

## 📝 编写测试用例

### 1. 准备测试数据

在 `bizs/data/` 目录创建 YAML 文件：

```yaml
# bizs/data/report_cases.yaml
history_order_list:
  指定时间筛选:
    pageNum: 1
    pageSize: 50
    startDate: "2025-11-29"
    endDate: "2025-11-29"
    orderStatus: []
    sortRule:
      field: ""
      order: ""
```

---

### 2. 封装 API

在 `bizs/apis/` 目录创建 API 类：

```python
# bizs/apis/report_api.py
from core.base.base_api import BaseAPI

class ReportAPI(BaseAPI):
    """报表 API 封装"""
    
    def __init__(self, account_name="default"):
        super().__init__()
        self.history_order_list = "/api/report/order/listPage"
        self.set_account(account_name)
    
    def get_order_list_page(self, page_num=1, page_size=50, 
                           start_date=None, end_date=None,
                           return_response=False):
        """获取历史订单列表"""
        payload = {
            "pageNum": page_num,
            "pageSize": page_size,
            "startDate": start_date,
            "endDate": end_date
        }
        
        response = self.client.post(self.history_order_list, json=payload)
        
        if return_response:
            return response
        
        return response.json()
```

---

### 3. 编写测试用例

在 `tests/` 目录创建测试文件：

```python
# tests/test_report.py
import pytest
from bizs.apis.report_api import ReportAPI
from core.utils.yaml_loader import YamlLoader
from core.test_helper import BaseTest

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
    
    def test_history_order_list(self, report_api, test_data):
        """测试历史订单列表"""
        # 1. 获取测试数据
        case_data = test_data["history_order_list"]["指定时间筛选"]
        
        # 2. 发送请求
        response = report_api.get_order_list_page_by_dict(
            params=case_data,
            return_response=True
        )
        
        # 3. 断言响应
        response_data = self.assert_success_response(response)
        
        # 4. 记录数据数量
        self.log_data_count(response_data)
```

---

## 💡 最佳实践

### 1. **使用 pytest fixtures**

✅ **推荐：**
```python
@pytest.fixture(scope="class")
def api():
    return ReportAPI()

class TestReport:
    def test_xxx(self, api):  # 自动注入
        pass
```

❌ **不推荐：**
```python
class TestReport:
    def setup_class(cls):
        cls.api = ReportAPI()
```

---

### 2. **继承 BaseTest**

✅ **推荐：**
```python
from core.test_helper import BaseTest

class TestYourAPI(BaseTest):
    def test_xxx(self):
        response_data = self.assert_success_response(response)
```

❌ **不推荐：**
```python
class TestYourAPI:
    def test_xxx(self):
        assert response.status_code == 200
        response_data = response.json()
        # ... 重复的断言代码
```

---

### 3. **数据驱动测试**

✅ **推荐：**
```python
# 使用 YAML 管理测试数据
test_data = YamlLoader.load_test_data("cases.yaml")
case_data = test_data["case_name"]["case_key"]
```

❌ **不推荐：**
```python
# 硬编码测试数据
data = {
    "key1": "value1",
    "key2": "value2",
    # ...
}
```

---

### 4. **清晰的测试步骤**

✅ **推荐：**
```python
def test_xxx(self):
    # 1. 准备数据
    data = {...}
    
    # 2. 发送请求
    response = api.some_method(data, return_response=True)
    
    # 3. 断言响应
    response_data = self.assert_success_response(response)
    
    # 4. 验证数据
    self.log_data_count(response_data)
```

---

## 🔒 多账号配置

### 配置多个测试账号

```yaml
# config/account_info_config.yaml
accounts:
  default:  # 默认账号
    account_id: "123456"
    org_id: "789012"
    Cookie: "cookie_string_1"
  
  account2:  # 第二个账号
    account_id: "654321"
    org_id: "210987"
    Cookie: "cookie_string_2"
```

### 使用不同账号

```python
# 在测试中使用不同账号
report_api1 = ReportAPI(account_name="default")
report_api2 = ReportAPI(account_name="account2")

# 或者切换账号
from core.base.session_manager import session_manager
session_manager.set_account("account2")
```

---

## 📊 测试报告

### 生成 HTML 报告

```bash
# 生成 HTML 测试报告
pytest tests/ -v --html=reports/report.html --self-contained-html

# 报告会生成在 reports/report.html
```

### 查看日志

- **测试日志**: `logs/api_test.log`
- **详细程度**: 在 `config/config.yaml` 中配置

---

## ❓ 常见问题

### Q1: 如何切换不同的测试环境？

**A:** 修改 `config/config.yaml` 中的 `base_url`：

```yaml
base:
  base_url: "https://test-api.example.com"  # 测试环境
  # base_url: "https://api.example.com"     # 生产环境
```

---

### Q2: 如何处理 Token 认证？

**A:** 框架支持自动 Token 管理：

```python
from core.base.session_manager import session_manager

# 登录后设置 Token
session_manager.set_token(token_from_login)

# 后续请求自动添加 Token
# HTTP 客户端会自动在请求头中添加: Authorization: Bearer {token}
```

---

### Q3: 如何调试失败的测试？

**A:** 
1. 使用 `-s` 参数查看详细输出：`pytest tests/test_xxx.py -v -s`
2. 查看日志文件：`logs/api_test.log`
3. 在代码中添加断点：`import pdb; pdb.set_trace()`

---

### Q4: conftest.py 可以移动到其他目录吗？

**A:** 不可以。`conftest.py` 必须在 `tests/` 目录中，这是 pytest 的规范。详见 [tests/README.md](tests/README.md)。

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 PR 流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

---

## 📚 更多文档

- [测试编写详细指南](tests/README.md)
- [配置文件说明](config/config.yaml)
- [账号配置说明](config/account_info_config.yaml)

---

## 📄 License

MIT License

---

## 👥 作者

- **XCJ** - *Initial work* - [1960675737](https://github.com/1960675737)

---

## 🌟 致谢

- [Pytest](https://docs.pytest.org/) - 优秀的 Python 测试框架
- [Requests](https://requests.readthedocs.io/) - 简洁优雅的 HTTP 库
- [PyYAML](https://pyyaml.org/) - YAML 解析库

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
