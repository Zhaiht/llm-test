"""测试Locust是否可以正常运行"""
import sys
import subprocess
import tempfile
import os

# 创建简单的locust脚本
locust_script = '''from locust import HttpUser, task, between

class TestUser(HttpUser):
    wait_time = between(1, 1.5)
    host = "http://localhost:1234"
    
    @task
    def get_models(self):
        self.client.get("/v1/models")
'''

# 写入临时文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(locust_script)
    temp_file = f.name

print(f"临时文件: {temp_file}")
print(f"Python: {sys.executable}")

try:
    # 构建命令
    cmd = [
        sys.executable,
        '-m', 'locust',
        '-f', temp_file,
        '--headless',
        '-u', '2',
        '-r', '2',
        '-t', '10s',
        '--html', 'test_report.html'
    ]
    
    print(f"命令: {' '.join(cmd)}")
    print("开始执行...")
    
    # 执行
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=20,
        encoding='utf-8',
        errors='replace'
    )
    
    print(f"\n返回码: {result.returncode}")
    print(f"\nSTDOUT:\n{result.stdout}")
    print(f"\nSTDERR:\n{result.stderr}")
    
    if result.returncode == 0:
        print("\n✅ 测试成功！")
    else:
        print("\n❌ 测试失败！")
        
finally:
    # 清理
    if os.path.exists(temp_file):
        os.unlink(temp_file)
        print(f"\n已删除临时文件: {temp_file}")
