# LLM 测试工具 - 安装说明

## 环境要求

- Python 3.7+
- pip

## 安装步骤

### 1. 安装基础依赖

```bash
pip install -r requirements.txt
```

这将安装所有必需的依赖，包括：
- Flask（Web框架）
- requests（HTTP请求）
- pandas（数据处理）
- openpyxl（Excel文件处理）
- locust（压力测试工具）
- zope.event（Locust依赖）

### 2. 验证安装

```bash
# 验证Locust是否正确安装
python -m locust --version
```

如果看到版本号，说明安装成功。

### 3. 如果遇到依赖问题

如果压力测试提示 `ModuleNotFoundError: No module named 'zope.event'`，请运行：

```bash
pip install zope.event
```

或者重新安装Locust：

```bash
pip uninstall locust
pip install locust
```

## 运行应用

```bash
python app.py
```

然后在浏览器访问：http://localhost:5000

## 功能说明

### 问答测试
- 支持从Excel文件读取问题
- 支持手动输入问题
- 实时显示测试进度和结果
- 自动生成测试报告

### 压力测试
- 需要先安装 Locust：`pip install locust`
- 支持测试 /v1/models 接口
- 支持测试 /v1/chat/completions 接口
- 支持混合测试
- 自动生成HTML格式的压测报告

## 常见问题

### Q: 压力测试提示"ModuleNotFoundError: No module named 'zope.event'"
A: 运行以下命令安装缺失的依赖：
```bash
pip install zope.event
```
或者重新安装Locust：
```bash
pip uninstall locust
pip install locust
```

### Q: 压力测试提示"Locust未安装"
A: 运行 `pip install locust` 安装压力测试工具

### Q: 问答测试找不到Excel文件
A: 确保 questions.xlsx 文件在项目根目录，或修改文件路径

### Q: API连接失败
A: 检查LM Studio或其他LLM服务是否已启动，默认地址为 http://localhost:1234

## 目录结构

```
.
├── app.py                  # Flask应用主文件
├── questions.py            # 问答测试逻辑
├── locustfile.py          # Locust压测脚本示例
├── requirements.txt        # Python依赖
├── questions.xlsx         # 问题文件示例
├── templates/             # HTML模板
│   ├── base.html         # 基础模板
│   ├── qa_test.html      # 问答测试页面
│   └── stress_test.html  # 压力测试页面
└── reports/              # 测试报告目录（自动创建）
```

## 技术栈

- 后端：Flask
- 前端：原生JavaScript + CSS
- 压测：Locust
- 数据处理：pandas, openpyxl
