from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import json
from questions import run_test

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('config_form.html')

@app.route('/run_test', methods=['POST'])
def run_test_route():
    config = {
        'api_url': request.form['api_url'],
        'model_name': request.form['model_name'],
        'temperature': float(request.form['temperature']),
        'max_tokens': int(request.form['max_tokens']),
        'timeout': int(request.form['timeout']),
        'sleep_interval': float(request.form['sleep_interval']),
        'questions_file': request.form['questions_file']
    }
    
    report_path = run_test(config)
    
    if not report_path:
        return render_template('error.html', error='未找到有效的测试问题或测试失败')
    
    return render_template('result.html', report_path=report_path)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
