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
        return render_template('config_form.html')
    except Exception as e:
        logger.error(f"加载失败: {e}", exc_info=True)
        return str(e), 500

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
    
    def generate():
        try:
            logger.info(f"开始流式测试: {config['questions_file']}")
            for event in run_test_stream(config):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            logger.error(f"流式测试失败: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/.well-known/appspecific/com.chrome.devtools.json')
def devtools():
    return '', 204

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
