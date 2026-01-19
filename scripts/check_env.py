"""检查Python环境和依赖"""
import sys
import os

print("=" * 60)
print("Python 环境信息")
print("=" * 60)
print(f"Python 可执行文件: {sys.executable}")
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.path[0]}")
print()

print("=" * 60)
print("检查依赖包")
print("=" * 60)

# 检查各个包
packages = ['flask', 'requests', 'pandas', 'openpyxl', 'locust', 'zope.event', 'gevent']

for package in packages:
    try:
        mod = __import__(package)
        version = getattr(mod, '__version__', '未知版本')
        location = getattr(mod, '__file__', '未知位置')
        print(f"✓ {package:15} {version:15} {os.path.dirname(location)}")
    except ImportError as e:
        print(f"✗ {package:15} 未安装 - {e}")

print()
print("=" * 60)
print("测试 Locust 导入")
print("=" * 60)

try:
    import locust
    print(f"✓ Locust 导入成功")
    print(f"  版本: {locust.__version__}")
    print(f"  位置: {locust.__file__}")
except Exception as e:
    print(f"✗ Locust 导入失败")
    print(f"  错误: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("建议操作")
print("=" * 60)
print("如果看到依赖缺失，请运行：")
print(f"  {sys.executable} -m pip install <包名>")
print()
print("例如：")
print(f"  {sys.executable} -m pip install zope.event")
print(f"  {sys.executable} -m pip install locust --force-reinstall")
