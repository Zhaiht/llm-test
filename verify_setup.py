"""验证项目设置是否正确"""
import sys
import os

def check_structure():
    """检查项目结构"""
    print("检查项目结构...")
    required_dirs = ['src/llm_test', 'templates', 'data', 'docs', 'scripts', 'reports']
    required_files = ['main.py', 'README.md', 'requirements.txt', 'setup.py']
    
    missing = []
    for d in required_dirs:
        if not os.path.exists(d):
            missing.append(f"目录: {d}")
    
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f"文件: {f}")
    
    if missing:
        print("❌ 缺少以下文件/目录:")
        for item in missing:
            print(f"  - {item}")
        return False
    
    print("✅ 项目结构完整")
    return True

def check_imports():
    """检查关键模块导入"""
    print("\n检查模块导入...")
    try:
        from src.llm_test.services.qa_service import run_test_stream
        print("✅ qa_service 导入成功")
    except ImportError as e:
        print(f"❌ qa_service 导入失败: {e}")
        return False
    
    try:
        import flask
        print("✅ Flask 已安装")
    except ImportError:
        print("❌ Flask 未安装，请运行: pip install -r requirements.txt")
        return False
    
    return True

def check_templates():
    """检查模板文件"""
    print("\n检查模板文件...")
    templates = ['base.html', 'qa_test.html', 'stress_test.html']
    missing = []
    
    for t in templates:
        path = os.path.join('templates', t)
        if not os.path.exists(path):
            missing.append(t)
    
    if missing:
        print("❌ 缺少模板文件:")
        for t in missing:
            print(f"  - {t}")
        return False
    
    print("✅ 模板文件完整")
    return True

def main():
    print("=" * 60)
    print("LLM 测试工具 - 项目验证")
    print("=" * 60)
    
    checks = [
        check_structure(),
        check_imports(),
        check_templates()
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ 所有检查通过！")
        print("\n启动应用:")
        print("  python main.py")
        print("\n访问地址:")
        print("  http://localhost:5000")
        return 0
    else:
        print("❌ 部分检查失败，请修复后重试")
        return 1

if __name__ == '__main__':
    sys.exit(main())
