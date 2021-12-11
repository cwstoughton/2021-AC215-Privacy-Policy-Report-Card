from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from demo_inference_backend import model
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
async def get_predictions():
    # print(predictions)
    data = df.to_json()
    return data


@app.post('/analyze')
async def analyze_policy(input: InputData):
    # print(predictions["input_text"])
    result = dict()

    if input.input == "":
        result={
            "input_text": "No URL provided",
            "identifier_score": 0.0,
            "identifier_sentences": [],
            "location_score": 0.0,
            "location_sentences": [],
            "third_party_score": 0.0,
            "third_party_sentences": [],
        }

    else:
        result = convert_prediction(model.policy_prediction(input.input))
        result['input_text'] = str(input.input)


    return {"data": result}


@app.post("/predict_new")
async def predict(input_text: str):
    result = dict()
    result["input_text"] = input_text
    result["predictions"] = model.single_prediction(input_text)
    return model.single_prediction(input_text)
