from flask import Flask
import json

app = Flask(__name__)


@app.route("/")   # 127.0.0.1:5000/
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test")   # 127.0.0.1:5000/test
def hello_test():
    return "<p>Hello, Test!</p>"


# curl -X POST 127.0.0.1:5000/predict
@app.route("/predict", methods=["POST", "PUT"])  # POST, PUT method만 허용
def inference():
    return json.dumps({'hello': 'world'}), 200  # json and http status


if __name__ == "__main__":
    # debug 모드로 실행, 모든 IP 에서 접근 허용, 5000 포트로 사용함
    app.run(debug=True, host='0.0.0.0', port=5000)
