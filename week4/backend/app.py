from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)#启动
CORS(app)

@app.route('/参数') #默认是GET
def test_get():
    value = request.args.get("value", "")#从URL查询参数
    return {"结果": "参数是" + value}

@app.route('/参数post', methods = ['POST'])
def test_post():
    body_value = request.json.get("bodyValue", "")#从body的JSON里获取
    if request.json:
        body_value = request.json.get("bodyValue", "")
        param_value = request.args.get("paramValue", "")

    return {"body结果": "body是" + body_value,
            "param结果": "param是" + param_value
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)