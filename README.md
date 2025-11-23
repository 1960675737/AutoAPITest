# 接口自动化测试框架

一个基于Python的接口自动化测试框架，提供完整的API测试解决方案。

## 项目结构

```
api-auto-framework/
├── config/                # 配置文件
│   └── config.yaml
├── data/                  # 测试数据
│   └── login_cases.yaml
├── lib/                   # 核心库
│   ├── core/              # 核心引擎
│   │   ├── http_client.py     # 通用请求封装
│   │   ├── base_api.py        # API基类
│   │   └── session_manager.py # 会话/Token管理
│   ├── apis/              # API封装
│   │   └── auth_api.py        # 认证接口
│   ├── utils/             # 工具函数
│   │   ├── yaml_loader.py
│   │   ├── logger.py
│   │   └── config_loader.py
│   └── assert_helper.py   # 断言逻辑
├── tests/                 # 测试用例
│   └── test_auth.py
├── reports/               # 测试报告
├── logs/                 # 日志文件
└── run.py                # 运行入口
```

## 功能特性

- ✅ 统一的HTTP请求封装
- ✅ 自动Token管理
- ✅ 灵活的配置管理
- ✅ 完善的日志记录
- ✅ 丰富的断言方法
- ✅ YAML测试数据支持
- ✅ 测试报告生成
- ✅ 易于扩展的API封装

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

编辑 `config/config.yaml` 文件来配置框架：

- `base.base_url`: API基础URL
- `base.timeout`: 请求超时时间
- `logging.level`: 日志级别
- `auth.token_storage`: Token存储方式（memory/file）

## 使用示例

### 1. 编写测试数据

在 `data/login_cases.yaml` 中定义测试用例数据：

```yaml
success_login:
  username: "test_user"
  password: "test_password"
  expected:
    status_code: 200
    code: 0
    message: "登录成功"
```

### 2. 编写API封装

在 `lib/apis/` 目录下创建API类，继承 `BaseAPI`：

```python
from lib.core.base_api import BaseAPI

class UserAPI(BaseAPI):
    def get_user_info(self, user_id):
        return self.get(f"/api/users/{user_id}")
```

### 3. 编写测试用例

在 `tests/` 目录下编写测试用例：

```python
from lib.apis.auth_api import AuthAPI
from lib.assert_helper import assert_helper

def test_login():
    auth_api = AuthAPI()
    response = auth_api.client.post(
        "/api/auth/login",
        json={"username": "test", "password": "test"}
    )
    assert_helper.assert_status_code(response, 200)
```

### 4. 运行测试

```bash
# 使用pytest运行
pytest tests/ -v

# 或使用运行脚本
python run.py
```

## 核心模块说明

### HTTP客户端 (http_client.py)

提供统一的HTTP请求方法，自动处理：
- Token自动添加
- 请求/响应日志
- 错误处理

### 会话管理 (session_manager.py)

管理Token的存储和过期：
- 内存存储（默认）
- 文件存储
- 自动过期检查

### 断言助手 (assert_helper.py)

提供丰富的断言方法：
- `assert_status_code()`: 断言HTTP状态码
- `assert_equal()`: 断言相等
- `assert_response_json()`: 断言响应JSON
- 等等...

### 配置加载器 (config_loader.py)

单例模式的配置管理：
```python
from lib.utils.config_loader import config

base_url = config.get('base.base_url')
```

### 日志工具 (logger.py)

统一的日志记录：
```python
from lib.utils.logger import logger

logger.info("这是一条日志")
```

## 扩展指南

### 添加新的API模块

1. 在 `lib/apis/` 目录下创建新的API类
2. 继承 `BaseAPI` 基类
3. 实现具体的接口方法

### 添加新的断言方法

在 `lib/assert_helper.py` 中的 `AssertHelper` 类中添加新方法。

### 自定义配置

在 `config/config.yaml` 中添加新的配置项，通过 `config.get()` 方法访问。

## 注意事项

1. 确保 `config/config.yaml` 文件存在且配置正确
2. 测试数据文件使用UTF-8编码
3. Token存储方式根据需求选择（memory/file）
4. 日志文件会自动创建，无需手动创建logs目录

## License

MIT

