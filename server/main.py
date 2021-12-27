from flask import Flask, abort
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

GLOBAL_INC = 0

models = {}


@app.route("/")
def hello_world():
    global GLOBAL_INC
    GLOBAL_INC += 1
    return f"INCREMENT: {GLOBAL_INC}"


@app.route("/create_model")
def create_model():
    model_id = uuid.uuid4()
    models[model_id] = {}
    return {
        "model-id": model_id,
    }


@app.route("/save_model/<model_id>")
def save_model(model_id):
    if model_id not in models:
        abort(404)
    return {}


@app.route("/load_model/<model_id>")
def load_model(model_id):
    if model_id not in models:
        abort(404)
    return {}

if __name__ == "__main__":
    app.run()
