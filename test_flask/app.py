from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# CSV文件路径
CSV_FILE = 'data.csv'

# 如果CSV文件不存在，创建一个空的CSV文件
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['name', 'gender', 'hometown', 'remarks'])
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    # 读取CSV文件数据
    df = pd.read_csv(CSV_FILE)
    records = df.to_dict('records')
    return render_template('index.html', records=records)

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
    data = request.json
    index = int(data['index'])
    df = pd.read_csv(CSV_FILE)
    df.iloc[index] = [data['name'], data['gender'], data['hometown'], data['remarks']]
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"status": "success"})

@app.route('/delete', methods=['POST'])
def delete_record():
    index = int(request.json['index'])
    df = pd.read_csv(CSV_FILE)
    df = df.drop(index)
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)