from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# 메인 페이지를 렌더링하는 엔드포인트
@app.route('/')
def index():
    return render_template('index.html')  # templates 폴더 안의 index.html을 렌더링

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code')

    try:
        # 코드 실행 (주의: 보안상의 이유로 실제 서비스에서는 sandboxing이 필요합니다)
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return jsonify({'result': result.stdout})
        else:
            return jsonify({'result': f"Error: {result.stderr}"})
    except Exception as e:
        return jsonify({'result': f"Exception: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)