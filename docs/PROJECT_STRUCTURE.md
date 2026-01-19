# 项目结构说明

## 标准Python项目结构

```
llm-test/
│
├── src/                          # 源代码目录
│   └── llm_test/                # 主包
│       ├── __init__.py          # 包初始化，定义版本号
│       ├── app.py               # Flask应用主文件
│       │
│       ├── routes/              # 路由模块（MVC中的Controller）
│       │   ├── __init__.py
│       │   ├── qa_routes.py     # 问答测试路由
│       │   └── stress_routes.py # 压力测试路由
│       │
│       ├── services/            # 业务逻辑层（MVC中的Model）
│       │   ├── __init__.py
│       │   ├── qa_service.py    # 问答测试服务
│       │   └── stress_service.py# 压力测试服务
│       │
│       └── utils/               # 工具函数
│           ├── __init__.py
│           └── logger.py        # 日志配置
│
├── templates/                    # HTML模板（MVC中的View）
│   ├── base.html                # 基础模板
│   ├── qa_test.html             # 问答测试页面
│   └── stress_test.html         # 压力测试页面
│
├── static/                       # 静态资源
│   ├── css/                     # 样式文件
│   ├── js/                      # JavaScript文件
│   └── images/                  # 图片资源
│
├── data/                         # 数据文件
│   ├── questions.xlsx           # 问题文件示例
│   └── config.yaml              # 配置文件
│
├── docs/                         # 文档
│   ├── README.md                # 主文档
│   ├── INSTALL.md               # 安装说明
│   ├── API.md                   # API文档
│   └── LOCUST_README.md         # Locust使用说明
│
├── scripts/                      # 工具脚本
│   ├── check_env.py             # 环境检查
│   ├── test_locust.py           # Locust测试
│   ├── reorganize.py            # 项目重组
│   ├── fix_anaconda_env.bat     # 环境修复（Windows）
│   └── fix_locust.sh            # 环境修复（Linux/Mac）
│
├── tests/                        # 测试用例
│   ├── __init__.py
│   ├── test_qa_service.py       # 问答服务测试
│   ├── test_stress_service.py   # 压力测试服务测试
│   └── test_routes.py           # 路由测试
│
├── examples/                     # 示例代码
│   ├── locustfile.py            # Locust脚本示例
│   └── sample_questions.xlsx    # 示例问题文件
│
├── reports/                      # 测试报告输出
│   └── .gitkeep                 # 保持目录
│
├── .git/                         # Git版本控制
├── .gitignore                    # Git忽略文件
├── .vscode/                      # VSCode配置
│
├── requirements.txt              # Python依赖列表
├── setup.py                      # 安装配置
├── MANIFEST.in                   # 打包配置
├── pytest.ini                    # pytest配置
├── .flake8                       # flake8配置
│
├── README.md                     # 项目说明
├── LICENSE                       # 许可证
├── CHANGELOG.md                  # 更新日志
│
├── app.py                        # 旧版启动文件（兼容）
└── run.py                        # 新版启动文件

```

## 目录职责

### src/llm_test/
主要源代码包，包含所有业务逻辑。

- **app.py**: Flask应用工厂，创建和配置应用
- **routes/**: 处理HTTP请求，调用服务层
- **services/**: 核心业务逻辑，与外部API交互
- **utils/**: 通用工具函数，如日志、配置等

### templates/
Jinja2模板文件，负责页面渲染。

### static/
静态资源文件，如CSS、JavaScript、图片等。

### data/
数据文件和配置文件。

### docs/
项目文档，包括安装、使用、API说明等。

### scripts/
辅助脚本，用于开发、测试、部署等。

### tests/
单元测试和集成测试。

### examples/
示例代码和配置文件。

### reports/
测试报告输出目录。

## 设计模式

### MVC架构
- **Model**: services/ - 业务逻辑和数据处理
- **View**: templates/ - 页面展示
- **Controller**: routes/ - 请求处理和路由

### 分层架构
```
Presentation Layer (templates/)
        ↓
Controller Layer (routes/)
        ↓
Service Layer (services/)
        ↓
Utility Layer (utils/)
```

## 命名规范

### 文件命名
- Python文件：小写+下划线，如 `qa_service.py`
- 模板文件：小写+下划线，如 `qa_test.html`
- 配置文件：大写，如 `README.md`

### 代码命名
- 类名：大驼峰，如 `QAService`
- 函数名：小写+下划线，如 `load_questions`
- 常量：大写+下划线，如 `MAX_RETRIES`
- 变量：小写+下划线，如 `question_list`

## 导入规范

```python
# 标准库
import os
import sys

# 第三方库
from flask import Flask
import pandas as pd

# 本地模块
from llm_test.services import qa_service
from llm_test.utils import logger
```

## 配置管理

### 开发环境
```python
DEBUG = True
TESTING = False
```

### 生产环境
```python
DEBUG = False
TESTING = False
```

## 版本控制

使用语义化版本号：`MAJOR.MINOR.PATCH`

- MAJOR: 不兼容的API修改
- MINOR: 向后兼容的功能新增
- PATCH: 向后兼容的问题修正

当前版本：`1.0.0`
