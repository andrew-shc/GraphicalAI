from flask import Flask, abort, request
from flask_cors import CORS
import uuid

import requests

app = Flask(__name__)
CORS(app)

GLOBAL_INC = 0

models = {}
# each models should have following properties:
# - project fpath TODO: somehow make the file handler handle models independently from the project context
# - model name
# - required inputs & outputs


@app.route("/")
def hello_world():
    global GLOBAL_INC
    GLOBAL_INC += 1
    return f"INCREMENT: {GLOBAL_INC}"


# creates a new model with a new model id assigned to it
@app.route("/create_model")
def create_model():
    model_id = str(uuid.uuid4())
    models[model_id] = {}
    return {
        "model-id": model_id,
    }


# saves (any possible) data through the json to the model's key value
@app.route("/save_model/<model_id>", methods=["POST"])
def save_model(model_id):
    print(model_id, type(model_id), models)
    if model_id not in models:
        abort(404)
    print("retrieved json", request.get_json())
    models[model_id] = request.get_json()
    return {}


# returns all the data established in that model's key value
@app.route("/load_model/<model_id>", methods=["GET"])
def load_model(model_id):
    if model_id not in models:
        abort(404)
    return models[model_id]


# calls the command to predict the model
@app.route("/predict_model/<model_id>", methods=["POST"])
def predict_model(model_id):
    if model_id not in models:
        abort(404)
    print("predict_model retrieved json:", request.get_json())
    return {"output-data": ["foo", "bar", "baz"]}


if __name__ == "__main__":
    # app.run()

    from graphical_ai.file_handler import ModelFileHandler

    mhndl = ModelFileHandler("C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II\\Testing-XIII\\models", "LinReg")
    mhndl.load_model()

    print(mhndl.mdl_dt)


