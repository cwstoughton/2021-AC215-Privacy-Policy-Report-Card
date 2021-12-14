from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
# from inference_backend import model
from Back_End.Fast_Inference_Engine import model
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html>
    <head>
        <title>Privacy Policy Report Card Demo </title>
    </head>
    <body>
        Welcome to the Privacy Policy Report Card App!
        <br><br>
        
        We use cookies!
        
        <a href="http://localhost:3000">Click here to start</a>
    </body>
</html>
"""


class InputData(BaseModel):
    input: str


def convert_prediction(sentences):
    result = {"input_text": "asdfasdf", "identifier_score": 0.3, "identifier_sentences": sentences['IDENTIFIERS'],
              "location_score": 0.5, "location_sentences": sentences['LOCATION'], "third_party_score": 0.8,
              "third_party_sentences": sentences['3RD_PARTY']}
    return result


@app.get("/predict")
async def get_predictions(input):
    data = model.policy_prediction(input)
    return data


@app.post('/analyze')
async def analyze_policy(input: InputData):
    print("Getting predictions for", input.input)
    # print(predictions["input_text"])
    result = dict()
    colors = [["#FFC371", "#FF5F6D"], ["#C3FF71", "#5FFF6D"], ["#86CEFA", "#003396"],["#C371FF", "#5F6DFF"]]
    if input.input == "":
        result = {
            "input_text": "No URL provided",
            "predictions": [
                {
                    "category": "identifiers",
                    "sentences": [],
                    "score": 0.0,
                    "colors": colors[0]
                },
                {
                    "category": "location",
                    "sentences": [],
                    "score": 0.0,
                    "colors": colors[1]
                },
                {
                    "category": "third_party_sharing",
                    "sentences": [],
                    "score": 0.0,
                    "colors": colors[2]
                },
                {
                    "category": "contacts",
                    "sentences": [],
                    "score": 0.0,
                    "colors": colors[3]
                }]}
    elif input.input == "test":
            result = {
                "input_text": "Test success",
                "predictions": [
                    {
                        "category": "identifiers",
                        "sentences": [],
                        "score": 0.0,
                        "colors": colors[0]
                    },
                    {
                        "category": "location",
                        "sentences": [],
                        "score": 0.0,
                        "colors": colors[1]
                    },
                    {
                        "category": "third_party_sharing",
                        "sentences": [],
                        "score": 0.0,
                        "colors": colors[2]
                    },
                    {
                        "category": "contacts",
                        "sentences": [],
                        "score": 0.0,
                        "colors": colors[3]
                    }]}
    else:
        predictions = model.policy_prediction(input.input)["data"]
        for i, pred in enumerate(predictions):
            pred["colors"]=colors[i]

        result["predictions"] = predictions
        result['input_text'] = str(input.input)

    return {"data": result}


@app.post("/predict_new")
async def predict(input_text: str):
    result = dict()
    result["input_text"] = input_text
    result["predictions"] = model.single_prediction(input_text)
    return model.single_prediction(input_text)
