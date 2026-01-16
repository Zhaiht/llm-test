@echo off
echo ========================================
echo 修复 Anaconda 环境中的 Locust
echo ========================================
echo.

echo 当前Python环境:
python --version
python -c "import sys; print('路径:', sys.executable)"
echo.

echo 步骤1: 卸载用户目录中的包...
python -m pip uninstall locust gevent greenlet zope.event urllib3 -y

echo.
echo 步骤2: 升级pip...
python -m pip install --upgrade pip

echo.
echo 步骤3: 清理缓存并重新安装...
python -m pip cache purge
python -m pip install locust --no-cache-dir --force-reinstall

echo.
echo 步骤4: 验证安装...
python -c "import locust; print('✓ Locust版本:', locust.__version__); print('✓ 安装位置:', locust.__file__)"

echo.
echo 步骤5: 测试命令...
python -m locust --version

echo.
echo ========================================
echo 修复完成！
echo 如果仍有问题，请尝试: conda install -c conda-forge locust
echo ========================================
pause
