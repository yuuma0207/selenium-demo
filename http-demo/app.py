from flask import Flask, request, jsonify
import numpy as np  # 大規模計算例として
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # CORS (Cross-Origin Resource Sharing) を有効化。これにより異なるドメインからのアクセスを許可。

@app.route('/calculate', methods=['POST'])
def calculate():
    print("通信がありました！")
    data = request.json
    # 例: data に大規模配列が含まれている想定
    arr = np.array(data['numbers'])

    # 何らかの処理 (例: 合計、平均など)
    total = np.sum(arr)
    average = np.mean(arr)

    return jsonify({
        'total': float(total),
        'average': float(average)
    })

if __name__ == '__main__':
    app.run(port=5123, debug=True)
