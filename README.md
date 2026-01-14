# LLM 测试工具

一个基于 Flask 的 Web 应用，用于批量测试 LLM 模型的响应质量和性能。

## 功能特性

- 🎨 现代化 Web 界面，左右分栏布局
- 📊 实时显示测试进度和统计数据
- 🔄 支持流式输出，实时查看测试日志
- 📈 自动生成 Excel 测试报告
- 🎯 计算模型回答与参考答案的相似度
- 📝 完整的日志记录和错误追踪
- 🚀 支持 LM Studio、Ollama 等本地 LLM 服务

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备问题文件

创建 Excel 文件（如 `questions.xlsx`），包含以下列：
- `问题`：测试问题（必需）
- `答案`：参考答案（可选，用于相似度计算）

### 3. 启动应用

```bash
python app.py
```

### 4. 访问界面

打开浏览器访问：http://localhost:5000

### 5. 配置并测试

在 Web 界面填写配置：
- **API 地址**：LM Studio 默认 `http://localhost:1234/v1/chat/completions`
- **模型名称**：模型标识（LM Studio 可留空）
- **Temperature**：控制输出随机性（0-2）
- **最大 Token 数**：单次回答的最大长度
- **超时时间**：API 请求超时时间（秒）
- **请求间隔**：每次请求之间的等待时间（秒）
- **问题文件路径**：Excel 文件路径

点击"开始测试"，右侧实时显示测试进度和结果。

## 测试报告

测试完成后会生成两个文件：

1. **原问题文件**：添加"回答"和"相似度"列
2. **测试报告**：保存在 `reports/` 目录，包含：
   - 测试结果详情（问题、回答、延迟、状态）
   - 测试汇总（成功率、平均延迟、拒答数等）

## 项目结构

```
llm-test/
├── app.py                      # Flask 应用主文件
├── questions.py                # 测试逻辑和报告生成
├── requirements.txt            # Python 依赖
├── templates/
│   ├── config_form.html       # 主界面（配置表单+实时日志）
│   ├── result.html            # 结果页面
│   └── error.html             # 错误页面
├── reports/                    # 测试报告目录（自动生成）
└── .gitignore                 # Git 忽略配置
```

## 技术栈

- **后端**：Flask + Python 3.x
- **前端**：原生 HTML/CSS/JavaScript
- **数据处理**：pandas、openpyxl
- **实时通信**：Server-Sent Events (SSE)
- **日志**：Python logging 模块

## 兼容性

支持以下 LLM 服务：
- LM Studio（推荐）
- Ollama
- 任何兼容 OpenAI API 格式的服务

## 注意事项

- 确保 LLM 服务已启动并可访问
- Excel 文件必须包含"问题"列
- 测试过程中请勿关闭浏览器
- 大量问题测试时注意 API 限流

## 许可证

MIT License
