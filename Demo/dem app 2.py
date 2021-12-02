from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from demo_inference_backend import model
from fastapi.middleware.cors import CORSMiddleware


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

@app.get("/predict")
async def get_predictions():
    return { "data": predictions }

@app.post("/predict_new")
async def predict(input_text: str):
   # print(input_text)
    result = dict()
    result["input_text"]=input_text
    result["predictions"]=model.single_prediction(input_text)
    # print(predictions)
    return model.single_prediction(input_text)

@app.post('/analyze')
async def analyze_policy(url):
    print(url)
    url = url.replace(r'%2F', r'/')
    url = url.replace(r'%3A', r':')
    result = dict()
    result["input_text"] = url

    if url == "nope":
        result["predictions"] = {"IDENTIFIERS": [], "LOCATION": [], "3RD_PARTY": []}
        print('NOPE')
        return {"data":result}

    result["predictions"] = model.policy_prediction(url)
    print(result["predictions"])
    # predictions = [{'input_text': url, 'predictions': str(}]
    # prediction =
    # print(result)
    return {"data": result}
