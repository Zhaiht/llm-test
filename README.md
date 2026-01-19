# LLM 测试工具

一个用于测试大语言模型（LLM）问答能力和性能的综合工具。

## 功能特性

- ✅ **问答测试**：批量测试LLM的问答能力
  - 支持从Excel文件读取问题
  - 支持手动输入问题
  - 实时显示测试进度
  - 自动生成测试报告
  - 计算答案相似度

- ⚡ **压力测试**：测试LLM服务的性能
  - 支持多种接口测试
  - 可配置并发用户数
  - 实时显示RPS和响应时间
  - 生成详细的HTML报告

## 项目结构

```
llm-test/
├── main.py                # 主启动文件
├── src/                   # 源代码
│   └── llm_test/
│       ├── __init__.py
│       ├── services/      # 业务逻辑
│       │   └── qa_service.py     # 问答测试服务
│       └── utils/         # 工具函数
│           ├── __init__.py
│           └── logger.py         # 日志配置
├── templates/             # HTML模板
│   ├── base.html         # 基础模板
│   ├── qa_test.html      # 问答测试页面
│   ├── stress_test.html  # 压力测试页面
│   ├── result.html       # 结果页面
│   └── error.html        # 错误页面
├── data/                  # 数据文件
│   ├── questions.xlsx    # 问题文件示例
│   └── config.yaml       # 配置文件
├── docs/                  # 文档
│   ├── README.md         # 主文档
│   ├── INSTALL.md        # 安装说明
│   └── LOCUST_README.md  # Locust使用说明
├── scripts/               # 脚本
│   ├── check_env.py      # 环境检查
│   ├── test_locust.py    # Locust测试
│   └── fix_*.bat/sh      # 修复脚本
├── tests/                 # 测试用例
├── examples/              # 示例代码
│   └── locustfile.py     # Locust脚本示例
├── reports/               # 测试报告输出目录
├── requirements.txt       # Python依赖
├── setup.py              # 安装配置
├── MANIFEST.in           # 打包配置
├── .gitignore            # Git忽略文件
└── LICENSE               # 许可证
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
# 直接运行（推荐）
python main.py

# 或安装后运行
pip install -e .
llm-test
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

## 使用说明

### 问答测试

1. 选择"问答测试"标签
2. 配置API参数（地址、模型、温度等）
3. 选择提问方式：
   - 从文件读取：使用Excel文件
   - 手动输入：直接输入问题
4. 点击"开始测试"
5. 查看实时结果和下载报告

### 压力测试

1. 选择"压力测试"标签
2. 配置压测参数：
   - 目标API地址
   - 测试接口类型
   - 并发用户数
   - 运行时长
3. 点击"开始压测"
4. 查看实时统计和下载报告

## 开发指南

### 添加新功能

1. 在 `src/llm_test/services/` 添加业务逻辑
2. 在 `main.py` 添加路由
3. 在 `templates/` 添加页面模板

### 运行测试

```bash
pytest tests/
```

### 代码规范

```bash
# 格式化代码
black src/

# 检查代码
flake8 src/
pylint src/
```

## 依赖说明

- **Flask**: Web框架
- **requests**: HTTP请求
- **pandas**: 数据处理
- **openpyxl**: Excel文件处理
- **locust**: 压力测试（可选）

## 常见问题

查看 [docs/INSTALL.md](docs/INSTALL.md) 获取详细的安装和故障排除指南。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
