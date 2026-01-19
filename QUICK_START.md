# 快速开始指南

## 1. 安装

```bash
# 克隆项目
git clone <repository-url>
cd llm-test

# 安装依赖
pip install -r requirements.txt
```

## 2. 启动应用

```bash
python main.py
```

访问：http://localhost:5000

## 3. 问答测试

1. 点击"问答测试"
2. 配置API参数
3. 选择提问方式（文件/手动输入）
4. 点击"开始测试"

## 4. 压力测试

1. 点击"压力测试"
2. 配置压测参数
3. 点击"开始压测"

## 常见问题

### Locust依赖问题

```bash
pip install locust zope.event
```

### 数据文件

示例问题文件：`data/questions.xlsx`

## 更多文档

- [完整文档](docs/README.md)
- [安装说明](docs/INSTALL.md)
- [Locust使用](docs/LOCUST_README.md)
