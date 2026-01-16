from locust import HttpUser, task, between
import json


class LLMAPIUser(HttpUser):
    """LLM API 压力测试用户"""
    
    # 等待时间：每个任务之间等待1-3秒
    wait_time = between(1, 3)
    
    # 设置基础URL
    host = "http://localhost:1234"
    
    @task(1)
    def get_models(self):
        """测试获取模型列表接口"""
        with self.client.get(
            "/v1/models",
            catch_response=True,
            name="GET /v1/models"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "data" in data:
                        response.success()
                    else:
                        response.failure("响应格式错误：缺少data字段")
                except json.JSONDecodeError:
                    response.failure("响应不是有效的JSON")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(3)
    def chat_completion(self):
        """测试聊天补全接口（权重更高）"""
        payload = {
            "model": "local-model",
            "messages": [
                {"role": "user", "content": "你好，请简单介绍一下自己。"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        with self.client.post(
            "/v1/chat/completions",
            json=payload,
            catch_response=True,
            name="POST /v1/chat/completions"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        response.success()
                    else:
                        response.failure("响应格式错误：缺少choices字段")
                except json.JSONDecodeError:
                    response.failure("响应不是有效的JSON")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    def on_start(self):
        """每个用户启动时执行"""
        print(f"用户启动，开始压测 {self.host}")
    
    def on_stop(self):
        """每个用户停止时执行"""
        print("用户停止")


class ModelsOnlyUser(HttpUser):
    """仅测试模型列表接口的用户"""
    
    wait_time = between(0.5, 1.5)
    host = "http://localhost:1234"
    
    @task
    def get_models(self):
        """只测试获取模型列表接口"""
        self.client.get("/v1/models", name="GET /v1/models (only)")
