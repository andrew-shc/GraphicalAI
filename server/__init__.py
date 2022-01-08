from flask import Flask, abort, request
from flask_cors import CORS
import uuid

import copy

from graphical_ai.file_handler import ModelFileHandler


app = Flask(__name__)
CORS(app)

GLOBAL_INC = 0

models = {}
# each models should have following properties:
# - model fpath "path" TODO: somehow make the file handler handle models independently from the project context
# - model name "name"
# - required inputs & outputs "req-inp" and "req-out
# - returned inputs & outputs "ret-inp" and "ret-out"


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
    if model_id not in models:
        abort(404)
    print("retrieved json", request.get_json())
    models[model_id] = request.get_json()
    models[model_id]["%%model"] = ModelFileHandler(models[model_id]["path"], models[model_id]["name"])
    models[model_id]["%%model"].load_model()
    return {}


# returns all the data established in that model's key value
@app.route("/load_model/<model_id>", methods=["GET"])
def load_model(model_id):
    if model_id not in models:
        abort(404)

    # prevents showing the hidden keys used internally
    model_cls = models[model_id]["%%model"]
    del models[model_id]["%%model"]

    mdl_dict = copy.deepcopy(models[model_id])

    models[model_id]["%%model"] = model_cls

    return mdl_dict


# calls the command to predict the model
# the req'd json (input) should contain all the necessary inputs and outputs attribute data
# the returning data should contain all the output information in respect to its output attribute
@app.route("/predict_model/<model_id>", methods=["POST"])
def predict_model(model_id):
    if model_id not in models:
        abort(404)

    req = request.get_json()
    print("predict_model retrieved json:", req)

    output = models[model_id]["%%model"].predict_model({
        "inp": {attr_name : tuple(req["inp"][attr_name]) for attr_name in req["inp"]},
        "out": {attr_name : tuple(req["out"][attr_name]) for attr_name in req["out"]},
        "predicting?": True,
    })

    print("out", output)
    return output


# model key: f4338b9c-d045-415e-9f14-04d3983832d9

if __name__ == "__main__":
    app.run()


    # mhndl = ModelFileHandler("C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II\\Testing-XIII\\models", "LinReg")
    # mhndl.load_model()
    #
    # print(mhndl.required_attrs())

    #   inp: {attr_name:(datatype,data)}
    #   out: {attr_name:(datatype,data)}
    #   predicting?: bool

    # attribute data-type options:
    #   ~ file, str:path
    #   ~ file-content, str:file_data, str:ext

    # output = mhndl.predict_model({
    #     "inp": {"a": ("file", "C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II\\Testing-XIII\\resources\\test.csv")},
    #     "out": {"b": ("file", "C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II\\Testing-XIII\\resources\\out.csv")},
    #     "predicting?": True,
    # })

    # with open("C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II\\Testing-XIII\\resources\\test.csv", "r") as fbo:
    #     fdt = fbo.read()
    #
    # output = mhndl.predict_model({
    #     "inp": {"a": ("file-content", fdt, ".csv")},
    #     "out": {"b": ("file-content", "", ".csv")},
    #     "predicting?": True,
    # })

    # print(output)

