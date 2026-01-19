"""
项目重组脚本
将现有文件移动到标准的Python项目结构中
"""
import os
import shutil

# 定义文件移动映射
MOVE_MAP = {
    # 源代码
    'questions.py': 'src/llm_test/services/qa_service.py',
    
    # 数据文件
    'questions.xlsx': 'data/questions.xlsx',
    'config.yaml': 'data/config.yaml',
    
    # 文档
    'README.md': 'docs/README.md',
    'INSTALL.md': 'docs/INSTALL.md',
    'LOCUST_README.md': 'docs/LOCUST_README.md',
    
    # 脚本
    'check_env.py': 'scripts/check_env.py',
    'test_locust.py': 'scripts/test_locust.py',
    'fix_anaconda_env.bat': 'scripts/fix_anaconda_env.bat',
    'fix_locust.bat': 'scripts/fix_locust.bat',
    'fix_locust.sh': 'scripts/fix_locust.sh',
    
    # 示例
    'locustfile.py': 'examples/locustfile.py',
}

# 需要删除的临时文件
DELETE_FILES = [
    'report.html',
    '__pycache__',
]

def reorganize():
    """执行重组"""
    print("=" * 60)
    print("开始重组项目结构...")
    print("=" * 60)
    
    # 移动文件
    for src, dst in MOVE_MAP.items():
        if os.path.exists(src):
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            # 如果是目录，使用copytree
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"✓ 复制目录: {src} -> {dst}")
            else:
                shutil.copy2(src, dst)
                print(f"✓ 复制文件: {src} -> {dst}")
        else:
            print(f"✗ 文件不存在: {src}")
    
    print()
    print("=" * 60)
    print("重组完成！")
    print("=" * 60)
    print()
    print("新的项目结构：")
    print("""
llm-test/
├── src/                    # 源代码
│   └── llm_test/
│       ├── __init__.py
│       ├── app.py         # Flask应用
│       ├── routes/        # 路由
│       ├── services/      # 业务逻辑
│       └── utils/         # 工具函数
├── templates/             # HTML模板
├── static/                # 静态文件
├── data/                  # 数据文件
├── docs/                  # 文档
├── scripts/               # 脚本
├── tests/                 # 测试
├── examples/              # 示例
├── reports/               # 报告输出
├── requirements.txt       # 依赖
├── setup.py              # 安装配置
└── README.md             # 主文档
    """)
    print()
    print("注意：原文件已保留，新文件在对应目录中")
    print("确认无误后，可以手动删除原文件")

if __name__ == '__main__':
    reorganize()
