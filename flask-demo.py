import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """アプリの説明を表示"""
    return """
    <h1>Flask デモアプリ</h1>
    <p>このアプリには以下のエンドポイントがあります。</p>
    <ul>
        <li><b>GET /</b> - この説明ページ</li>
        <li><b>POST /calculate</b> - JSON で渡された数値リストの合計と平均を計算</li>
        <li><b>GET /hello</b> - シンプルな 'Hello, World!' を返す</li>
    </ul>
    <p>例えば、/calculate に以下の JSON を POST すると計算結果が返ります。</p>
    <pre>
    {
        "numbers": [1, 2, 3, 4, 5]
    }
    </pre>
    """

@app.route('/calculate', methods=['POST'])
def calculate():
    """JSON で渡された数値リストの合計と平均を計算"""
    data = request.json
    if not data or 'numbers' not in data:
        return jsonify({'error': 'Invalid input. Please provide a list of numbers.'}), 400
    
    try:
        arr = np.array(data['numbers'], dtype=float)
        total = np.sum(arr)
        average = np.mean(arr)

        return jsonify({
            'total': float(total),
            'average': float(average)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/hello', methods=['GET'])
def hello():
    """シンプルな Hello, World! を返す"""
    return "Hello, World!"

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5123) # 外部からアクセス可能になる
    app.run(port=5123, debug=True) # ローカルのみのアクセス
