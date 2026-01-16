@echo off
echo ========================================
echo 修复 Locust 依赖问题
echo ========================================
echo.

echo 正在安装 zope.event...
pip install zope.event

echo.
echo 验证安装...
python -c "import zope.event; print('✓ zope.event 安装成功')"

echo.
echo 测试 Locust...
python -m locust --version

echo.
echo ========================================
echo 修复完成！请重启 Flask 应用
echo ========================================
pause
