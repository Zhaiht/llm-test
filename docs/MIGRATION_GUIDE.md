# 项目迁移指南

## 迁移状态

✅ **项目已完成迁移**到新的标准Python项目结构。

## 快速开始

直接运行新项目：

```bash
python main.py
```

或者安装后运行：

```bash
pip install -e .
llm-test
```

## 项目结构概览

### 当前结构

```
llm-test/
├── main.py                       # 主启动文件
├── src/                          # 源代码目录
│   └── llm_test/                 # 主包
│       ├── __init__.py          # 包初始化
│       ├── services/            # 业务逻辑
│       │   └── qa_service.py    # 问答测试服务
│       └── utils/               # 工具函数
│           ├── __init__.py
│           └── logger.py        # 日志配置
├── templates/                    # HTML模板
├── data/                         # 数据文件
├── docs/                         # 文档
├── examples/                     # 示例代码
├── scripts/                      # 工具脚本
├── requirements.txt              # Python依赖
└── setup.py                      # 安装配置
```

## 运行方式

### 开发模式

```bash
# 直接运行
python main.py
```

### 生产模式

```bash
# 安装
pip install -e .

# 运行
llm-test
```

## 获取帮助

如有问题，请查看：
- `PROJECT_STRUCTURE.md` - 项目结构详解
- `docs/INSTALL.md` - 安装指南
- `docs/README.md` - 主文档
