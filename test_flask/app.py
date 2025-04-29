from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = 'data.csv'

# 如果CSV文件不存在，创建一个空的CSV文件
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['name', 'gender', 'hometown', 'remarks'])
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    try:
        # 读取CSV文件数据
        df = pd.read_csv(CSV_FILE)
        records = df.to_dict('records')
        # 添加checked属性
        for record in records:
            record['checked'] = False
        return render_template('index.html', records=records)
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return render_template('index.html', records=[])

@app.route('/add', methods=['POST'])
def add_record():
    data = request.json
    df = pd.read_csv(CSV_FILE)
    # 修改这里：使用concat替代已弃用的append
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"status": "success"})

@app.route('/update', methods=['POST'])
def update_record():
    try:
        data = request.json
        index = data.pop('index', None)  # 移除并获取index
        if index is None:
            return jsonify({"error": "未提供索引"}), 400
            
        df = pd.read_csv(CSV_FILE)
        if index >= len(df):
            return jsonify({"error": "索引超出范围"}), 400
            
        # 更新记录
        for key, value in data.items():
            df.at[index, key] = value
            
        df.to_csv(CSV_FILE, index=False)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_record():
    index = int(request.json['index'])
    df = pd.read_csv(CSV_FILE)
    df = df.drop(index)
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)