from flask import Flask, request, jsonify, render_template_string
import os
app = Flask(__name__)

# HTML 模板
html_template = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>排名</title>
    <style>
        table {
            width: 80%;
            border-collapse: collapse;
            margin: 20px auto;
        }
        th, td {
            border: 1px solid #ccc;
            text-align: center;
            padding: 10px;
        }
        th {
            background-color: #f4f4f4;
        }
        h2 {
            text-align: center;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">排名</h1>

    <!-- 第一個表格 -->
    <h2>數字N(翻牌分數:(1 - 0.9 X (翻牌次數 - N) / N) X 100 X N)</h2>
    <table id="tableＮ1">
        <thead>
            <tr>
                <th>排名</th>
                <th>玩家名稱</th>
                <th>數字N</th>
                <th>翻牌次數</th>
                <th>翻牌時間</th>
				<th>翻牌分數</th>
                <th>時間分數</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>玩家A</td>
                <td>10</td>
                <td>5</td>
                <td>30秒</td>
				<td>50</td>
				<td>20</td>
            </tr>
        </tbody>
    </table>

	<!-- 第二個表格 -->
    <h2>數字N(時間分數:(1 - 0.5 X (翻牌時間 - 2 X N) / 2 X　N) X 100 X N)</h2>
    <table id="tableＮ２">
        <thead>
            <tr>
                <th>排名</th>
                <th>玩家名稱</th>
                <th>數字N</th>
                <th>翻牌次數</th>
                <th>翻牌時間</th>
				<th>翻牌分數</th>
                <th>時間分數</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>玩家A</td>
                <td>10</td>
                <td>5</td>
                <td>30秒</td>
				<td>50</td>
				<td>20</td>
            </tr>
        </tbody>
    </table>

    <!-- 第三個表格 -->
    <h2>撲克牌52</h2>
    <table id="table52">
        <thead>
            <tr>
                <th>排名</th>
                <th>玩家名稱</th>
                <th>翻牌次數</th>
                <th>翻牌時間</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>玩家B</td>
                <td>8</td>
                <td>25秒</td>
            </tr>
        </tbody>
    </table>

    <!-- 第四個表格 -->
    <h2>撲克牌54</h2>
    <table id="table54">
        <thead>
            <tr>
                <th>排名</th>
                <th>玩家名稱</th>
                <th>翻牌次數</th>
                <th>翻牌時間</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>玩家C</td>
                <td>6</td>
                <td>20秒</td>
            </tr>
        </tbody>
    </table>

    <script>
        // 表格為靜態顯示，不提供直接修改功能
        // 可通過爬蟲發送請求來模擬數據修改
        console.log("此頁面只允許通過爬蟲模擬提交數據進行修改。");
    </script>
</body>
</html>
"""

# 路徑: 返回 HTML
@app.route('/data', methods=['GET'])
def get_data():
    return render_template_string(html_template)

# 路徑: 更新數據
@app.route('/data', methods=['POST'])
def update_data():
    # 暫不更新 HTML，僅返回成功訊息
    return jsonify({"message": "數據更新成功"}), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

