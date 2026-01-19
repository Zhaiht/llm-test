# 项目迁移指南

## 快速开始

### 选项1：继续使用当前结构（推荐）

当前项目可以正常运行，无需立即迁移：

```bash
python app.py
```

### 选项2：逐步迁移到新结构

按照以下步骤逐步迁移：

## 迁移步骤

### 第1步：了解新结构

查看文档：
- `PROJECT_STRUCTURE.md` - 完整的项目结构说明
- `RESTRUCTURE.md` - 重构说明
- `README_NEW.md` - 新版README

### 第2步：测试当前功能

确保当前版本正常工作：

```bash
python app.py
# 访问 http://localhost:5000 测试所有功能
```

### 第3步：创建备份

```bash
# Windows
xcopy /E /I . ..\llm-test-backup

# Linux/Mac
cp -r . ../llm-test-backup
```

### 第4步：运行重组脚本

```bash
python scripts/reorganize.py
```

这会将文件复制到新的目录结构，原文件保持不变。

### 第5步：测试新结构

```bash
python run.py
# 访问 http://localhost:5000 测试所有功能
```

### 第6步：清理旧文件（可选）

确认新结构工作正常后，可以删除旧文件：

```bash
# 保留以下文件：
# - src/
# - templates/
# - static/
# - data/
# - docs/
# - scripts/
# - tests/
# - examples/
# - reports/
# - requirements.txt
# - setup.py
# - run.py
# - README_NEW.md
# - .gitignore
# - LICENSE

# 可以删除：
# - app.py (已移至 src/llm_test/app.py)
# - questions.py (已移至 src/llm_test/services/qa_service.py)
# - check_env.py (已移至 scripts/)
# - test_locust.py (已移至 scripts/)
# - *.bat, *.sh (已移至 scripts/)
# - locustfile.py (已移至 examples/)
# - questions.xlsx (已移至 data/)
# - config.yaml (已移至 data/)
# - *.md (已移至 docs/)
```

## 文件对照表

| 旧位置 | 新位置 | 说明 |
|--------|--------|------|
| `app.py` | `src/llm_test/app.py` | Flask应用 |
| `questions.py` | `src/llm_test/services/qa_service.py` | 问答服务 |
| `questions.xlsx` | `data/questions.xlsx` | 数据文件 |
| `config.yaml` | `data/config.yaml` | 配置文件 |
| `README.md` | `docs/README.md` | 文档 |
| `check_env.py` | `scripts/check_env.py` | 脚本 |
| `locustfile.py` | `examples/locustfile.py` | 示例 |

## 代码修改

### 导入路径更新

**旧代码：**
```python
from questions import load_questions, ask_model
```

**新代码：**
```python
from llm_test.services.qa_service import load_questions, ask_model
```

### 配置文件路径

**旧代码：**
```python
df = pd.read_excel('questions.xlsx')
```

**新代码：**
```python
df = pd.read_excel('data/questions.xlsx')
```

## 运行方式

### 开发模式

```bash
# 方法1：使用run.py
python run.py

# 方法2：使用模块
python -m src.llm_test.app
```

### 生产模式

```bash
# 安装
pip install -e .

# 运行
llm-test

# 或使用gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "llm_test.app:create_app()"
```

## 常见问题

### Q: 迁移后导入错误？
A: 确保 `src` 目录在 Python 路径中：
```python
import sys
sys.path.insert(0, 'src')
```

### Q: 找不到模板文件？
A: 检查 Flask 应用的 `template_folder` 配置：
```python
app = Flask(__name__, template_folder='../../templates')
```

### Q: 数据文件路径错误？
A: 使用相对于项目根目录的路径：
```python
os.path.join(os.path.dirname(__file__), '../../data/questions.xlsx')
```

## 回滚

如果遇到问题，可以回滚到旧结构：

```bash
# 恢复备份
xcopy /E /I ..\llm-test-backup\* .

# 或直接使用旧的app.py
python app.py
```

## 下一步

1. ✅ 阅读 `PROJECT_STRUCTURE.md` 了解新结构
2. ✅ 运行 `python scripts/reorganize.py` 重组项目
3. ✅ 测试 `python run.py` 确保功能正常
4. ✅ 更新文档和注释
5. ✅ 提交到版本控制

## 获取帮助

如有问题，请查看：
- `PROJECT_STRUCTURE.md` - 项目结构详解
- `RESTRUCTURE.md` - 重构说明
- `docs/INSTALL.md` - 安装指南
