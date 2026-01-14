# LLM 测试工具 - Web版

## 功能说明
通过Web表单配置测试参数，无需手动编辑配置文件。

## 使用步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动Web服务：
```bash
python app.py
```

3. 打开浏览器访问：http://localhost:5000

4. 在表单中填写配置参数：
   - API地址
   - 模型名称
   - Temperature
   - 最大Token数
   - 超时时间
   - 请求间隔
   - 问题文件路径

5. 点击"开始测试"按钮

6. 测试完成后下载报告

## 文件说明
- `app.py` - Flask Web应用主文件
- `questions.py` - 核心测试逻辑
- `templates/config_form.html` - 配置表单页面
- `templates/result.html` - 结果展示页面
- `requirements.txt` - Python依赖包

## 注意事项
- 确保问题文件（Excel）存在且格式正确
- 确保API服务可访问
