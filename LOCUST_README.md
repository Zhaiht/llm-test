# Locust 压测脚本使用说明

## 安装 Locust

```bash
pip install locust
```

## 运行压测

### 1. Web UI 模式（推荐）

启动 Locust Web 界面：

```bash
locust -f locustfile.py
```

然后在浏览器打开 http://localhost:8089，设置：
- **Number of users**: 并发用户数（例如：10）
- **Spawn rate**: 每秒启动用户数（例如：2）
- **Host**: 已在脚本中设置为 http://localhost:1234

点击 "Start swarming" 开始压测。

### 2. 命令行模式（无界面）

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 60s
```

参数说明：
- `-u 10`: 10个并发用户
- `-r 2`: 每秒启动2个用户
- `-t 60s`: 运行60秒后自动停止

### 3. 仅测试 /v1/models 接口

```bash
locust -f locustfile.py --headless -u 50 -r 10 -t 30s ModelsOnlyUser
```

## 压测场景

### LLMAPIUser（默认）
- 测试 GET /v1/models（权重1）
- 测试 POST /v1/chat/completions（权重3）
- 每个任务间隔1-3秒

### ModelsOnlyUser
- 仅测试 GET /v1/models
- 每个任务间隔0.5-1.5秒
- 适合高频压测单一接口

## 查看结果

压测过程中可以看到：
- **RPS**: 每秒请求数
- **响应时间**: 平均、最小、最大、P50、P95、P99
- **失败率**: 请求失败百分比
- **并发用户数**: 当前活跃用户数

## 导出报告

压测结束后生成HTML报告：

```bash
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html report.html
```

## 自定义配置

修改 `locustfile.py` 中的参数：
- `wait_time`: 调整任务间隔时间
- `@task(权重)`: 调整任务执行频率
- `payload`: 修改请求内容
- `host`: 修改目标服务器地址

## 注意事项

1. 确保目标服务 http://localhost:1234 已启动
2. 压测前建议先用小并发测试
3. 注意监控服务器资源使用情况
4. 长时间压测可能影响系统稳定性
