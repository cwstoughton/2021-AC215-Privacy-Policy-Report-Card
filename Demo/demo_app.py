from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from demo_inference_backend import model
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "172.17.0.3",
    "172.17.0.2",
    "172.17.0.2:3000",
    "172.17.0.3:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

CATEGORIES = ["IDENTIFIERS", "LOCATION", "3RD_PARTY"]

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
#
# @app.get("/predict")
# async def predict(input_text: str):
#     # return model.single_prediction(input_text)
#     return { "data": predictions }

#

# @app.get("/predict")
# async def get_predictions():
#     return { "data": predictions }





@app.get('/analyze')
async def analyze_policy(input : str):
    res = dict()
    res['input_text'] = input

    if input == "initiate":
        res['predictions'] = {'IDENTIFIERS': [], "LOCATION":[], "3RD_PARTY":[]}

    else:
        res['predictions'] = model.policy_prediction(input)
    return {"data": res }
    #
    # if input[:4] == "http":
    #     url = str(input)
    #     print(url)
    #
    #     url = url.replace(r'%2F', r'/')
    #     url = url.replace(r'%3A', r':')
    #
    #     try:
    #         preds = model.policy_prediction(url)
    #
    #     except:
    #         preds = []
    #         result
    #         return [{'input_text': input, 'predictions': preds}]
    #
    # else:
    #     return [{'input_text': input, 'predictions': "none"} ]
#
# @app.post("/predict_new")
# async def predict(input_text: str):
#     # print(input_text)
#     result = dict()
#     result["input_text"] = input_text
#     result["predictions"] = model.single_prediction(input_text)
#     # print(predictions)
#     return model.single_prediction(input_text)
#     # result["predictions"] = model.policy_prediction(url)
#     # print(result["predictions"])
#     # predictions = [{'input_text': url, 'predictions': str(}]
#     # prediction =
#     # print(result)


