import json
import pickle
import numpy as np
from flask import Flask, jsonify, request


# curl -X POST -H "Content-Type:application/json" --data '{"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 5.1, "petal_width": 1.8}' http://localhost:5000/predict
model = pickle.load(open('./build/model.pkl', 'rb'))
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def make_predict():
    # POST request
    # '{"sepal_length": 5.9, "sepal_width": 3.0, "petal_length": 5.1, "petal_width": 1.8}'
    request_body = request.get_json(force=True)
    X_test = [request_body['sepal_length'], request_body['sepal_width'],
              request_body['petal_length'], request_body['petal_width']]
    X_test = np.array(X_test)
    X_test = X_test.reshape(1, -1)

    y_test = model.predict(X_test)
    response_body = jsonify(result=y_test.tolist())

    return response_body


if __name__ == "__main__":
    # debug=True => server 에서 debug용 출력 할것이다.
    app.run(port=5000, debug=True)


