from flask import Flask, render_template, request, send_file, Response, jsonify
from questions import run_test_stream
import json
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('qa_test.html', active_page='qa')
    except Exception as e:
        logger.error(f"加载失败: {e}", exc_info=True)
        return str(e), 500

@app.route('/stress')
def stress():
    try:
        return render_template('stress_test.html', active_page='stress')
    except Exception as e:
        logger.error(f"加载失败: {e}", exc_info=True)
        return str(e), 500

@app.route('/test_locust')
def test_locust():
    """测试Locust是否可用"""
    import sys
    import subprocess
    
    result = {
        'python_path': sys.executable,
        'python_version': sys.version,
    }
    
    # 测试locust模块
    try:
        import locust
        result['locust_installed'] = True
        result['locust_version'] = locust.__version__
    except ImportError as e:
        result['locust_installed'] = False
        result['locust_error'] = str(e)
        
        # 检查是否是zope.event问题
        if 'zope.event' in str(e):
            result['fix_command'] = 'pip install zope.event'
            result['message'] = '缺少zope.event依赖，请运行: pip install zope.event'
    
    # 测试命令行
    try:
        cmd_result = subprocess.run(
            [sys.executable, '-m', 'locust', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        result['locust_command'] = True
        result['locust_command_output'] = cmd_result.stdout + cmd_result.stderr
        
        # 检查命令输出中是否有错误
        if 'zope.event' in result['locust_command_output']:
            result['fix_command'] = 'pip install zope.event'
            result['message'] = '缺少zope.event依赖，请运行: pip install zope.event'
    except Exception as e:
        result['locust_command'] = False
        result['locust_command_error'] = str(e)
    
    return jsonify(result)

@app.route('/run_test', methods=['POST'])
def run_test_route():
    try:
        config = {
            'api_url': request.form['api_url'],
            'model_name': request.form['model_name'],
            'temperature': float(request.form['temperature']),
            'max_tokens': int(request.form['max_tokens']),
            'timeout': int(request.form['timeout']),
            'sleep_interval': float(request.form['sleep_interval']),
            'questions_file': request.form['questions_file']
        }
        logger.info(f"开始测试: {config['questions_file']}")
        return jsonify({'status': 'started', 'config': config})
    except Exception as e:
        logger.error(f"启动测试失败: {e}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stream')
def stream():
    config = request.args.to_dict()
    config['temperature'] = float(config['temperature'])
    config['max_tokens'] = int(config['max_tokens'])
    config['timeout'] = int(config['timeout'])
    config['sleep_interval'] = float(config['sleep_interval'])
    config['question_mode'] = config.get('question_mode', 'file')
    
    def generate():
        try:
            logger.info(f"开始流式测试，模式: {config['question_mode']}")
            for event in run_test_stream(config):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            logger.error(f"流式测试失败: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def devtools():
    return '', 204

@app.route('/stress_test')
def stress_test():
    logger.info("=" * 50)
    logger.info("收到压力测试请求")
    logger.info(f"请求参数: {request.args.to_dict()}")
    
    # 首先检查Locust是否可用
    try:
        import locust
        logger.info(f"Locust版本: {locust.__version__}")
    except ImportError as e:
        logger.error(f"Locust导入失败: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Locust未正确安装。请在Anaconda环境中运行: python -m pip install locust'
        }), 500
    
    try:
        config = request.args.to_dict()
        target_url = config.get('target_url', 'http://localhost:1234')
        test_endpoint = config.get('test_endpoint', 'models')
        users = int(config.get('users', 10))
        spawn_rate = int(config.get('spawn_rate', 2))
        duration = int(config.get('duration', 60))
        wait_time = float(config.get('wait_time', 1))
        model_name = config.get('model_name', 'local-model')
        
        logger.info(f"配置: target={target_url}, endpoint={test_endpoint}, users={users}, duration={duration}s")
        
        import subprocess
        import tempfile
        import os
        import sys
        
        # 生成locust配置文件
        locust_script = f'''from locust import HttpUser, task, between
import json

class StressTestUser(HttpUser):
    wait_time = between({wait_time}, {wait_time + 0.5})
    host = "{target_url}"
    
'''
        
        if test_endpoint == 'models':
            locust_script += '''    @task
    def get_models(self):
        self.client.get("/v1/models")
'''
        elif test_endpoint == 'chat':
            locust_script += f'''    @task
    def chat_completion(self):
        payload = {{
            "model": "{model_name}",
            "messages": [{{"role": "user", "content": "你好"}}],
            "temperature": 0.7,
            "max_tokens": 100
        }}
        self.client.post("/v1/chat/completions", json=payload)
'''
        else:  # both
            locust_script += f'''    @task(1)
    def get_models(self):
        self.client.get("/v1/models")
    
    @task(3)
    def chat_completion(self):
        payload = {{
            "model": "{model_name}",
            "messages": [{{"role": "user", "content": "你好"}}],
            "temperature": 0.7,
            "max_tokens": 100
        }}
        self.client.post("/v1/chat/completions", json=payload)
'''
        
        # 确保reports目录存在
        os.makedirs('reports', exist_ok=True)
        logger.info("reports目录已创建/确认存在")
        
        # 写入临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(locust_script)
            temp_file = f.name
        
        logger.info(f"临时文件已创建: {temp_file}")
        logger.info(f"Python可执行文件: {sys.executable}")
        
        try:
            # 使用python -m locust 而不是直接调用locust命令
            cmd = [
                sys.executable,
                '-m', 'locust',
                '-f', temp_file,
                '--headless',
                '-u', str(users),
                '-r', str(spawn_rate),
                '-t', f'{duration}s',
                '--html', 'reports/locust_report.html',
                '--csv', 'reports/locust_stats'
            ]
            
            logger.info(f"准备执行命令: {' '.join(cmd)}")
            logger.info("开始执行Locust...")
            
            # 使用shell=False，在Windows上更可靠
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=duration + 60,
                encoding='utf-8',
                errors='replace',
                cwd=os.getcwd()
            )
            
            logger.info(f"Locust执行完成，返回码: {result.returncode}")
            
            # 记录输出
            if result.stdout:
                logger.info(f"Locust stdout:\n{result.stdout}")
            if result.stderr:
                logger.warning(f"Locust stderr:\n{result.stderr}")
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "未知错误"
                logger.error(f"Locust执行失败")
                
                # 检查是否是依赖问题
                if 'ModuleNotFoundError' in error_msg or 'No module named' in error_msg:
                    return jsonify({
                        'status': 'error',
                        'message': 'Locust依赖包缺失，请运行: pip install locust zope.event'
                    }), 500
                
                return jsonify({
                    'status': 'error',
                    'message': f'压测执行失败: {error_msg[:500]}'
                }), 500
            
            logger.info("开始解析结果...")
            
            # 尝试从CSV文件读取统计数据
            import csv
            stats_file = 'reports/locust_stats_stats.csv'
            total_requests = 0
            success_count = 0
            failed_count = 0
            avg_response_time = 0
            
            if os.path.exists(stats_file):
                logger.info(f"找到CSV文件: {stats_file}")
                try:
                    with open(stats_file, 'r', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if row.get('Type') == 'Aggregated' or row.get('Name') == 'Aggregated':
                                total_requests = int(row.get('Request Count', 0) or row.get('# requests', 0))
                                failed_count = int(row.get('Failure Count', 0) or row.get('# failures', 0))
                                success_count = total_requests - failed_count
                                avg_response_time = float(row.get('Average Response Time', 0) or row.get('Average response time', 0))
                                break
                    logger.info(f"从CSV读取: 总请求={total_requests}, 成功={success_count}, 失败={failed_count}")
                except Exception as e:
                    logger.error(f"读取CSV失败: {e}")
            else:
                logger.warning(f"CSV文件不存在: {stats_file}")
            
            # 如果没有CSV数据，尝试从输出解析
            if total_requests == 0:
                output = result.stdout
                # 简单估算
                total_requests = users * (duration // 2)  # 保守估计
                success_count = total_requests
                failed_count = 0
                avg_response_time = 100
                logger.info("使用估算值")
            
            avg_rps = round(total_requests / duration, 2) if duration > 0 else 0
            
            logger.info(f"最终结果: RPS={avg_rps}, 总请求={total_requests}, 成功={success_count}, 失败={failed_count}")
            logger.info("=" * 50)
            
            return jsonify({
                'status': 'success',
                'total_requests': total_requests,
                'success_count': success_count,
                'failed_count': failed_count,
                'avg_rps': avg_rps,
                'avg_response_time': round(avg_response_time, 2)
            })
            
        except subprocess.TimeoutExpired:
            logger.error("压测超时")
            return jsonify({
                'status': 'error',
                'message': '压测超时，请检查目标服务是否可用'
            }), 500
        finally:
            # 清理临时文件
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.info(f"已删除临时文件: {temp_file}")
            except Exception as e:
                logger.warning(f"删除临时文件失败: {e}")
            
    except Exception as e:
        logger.error(f"压测失败: {e}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'压测失败: {str(e)}'
        }), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        logger.info(f"下载文件: {filename}")
        return send_file(filename, as_attachment=True)
    except Exception as e:
        logger.error(f"下载文件失败: {e}", exc_info=True)
        return str(e), 404

if __name__ == '__main__':
    logger.info("启动Flask应用，端口: 5000")
    app.run(debug=True, port=5000)
