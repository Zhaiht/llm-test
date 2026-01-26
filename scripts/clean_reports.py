# scripts/clean_reports.py
import os
import time
from datetime import datetime, timedelta

def clean_reports(days_old=1, reports_dir='reports'):
    """清理指定天数之前的报告文件"""
    if not os.path.exists(reports_dir):
        print(f"目录 {reports_dir} 不存在")
        return
    
    now = time.time()
    cutoff_time = now - (days_old * 86400)  # 86400秒/天
    
    deleted = 0
    for filename in os.listdir(reports_dir):
        file_path = os.path.join(reports_dir, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff_time:
                os.remove(file_path)
                deleted += 1
                print(f"已删除过期报告: {filename}")
    
    print(f"清理完成，共删除 {deleted} 个过期报告")

if __name__ == "__main__":
    clean_reports()