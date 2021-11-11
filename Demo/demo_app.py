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


predictions = [
    # {"input_text":"We collect cookiesss","predictions":{"IDENTIFIERS":0.04112809896469116,"LOCATION":0.020514369010925293,"3RD_PARTY":0.1350472867488861}}
]



@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html>
    <head>
        <title>🍄 Privacy Policy Report Card Demo </title>
    </head>
    <body>
        🍄 Welcome to the Privacy Policy Report Card App!
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


@app.get("/predict")
async def get_predictions():
    return { "data": predictions }

@app.post("/predict")
async def predict(input_text: str):
    print(input_text)
    result = dict()
    result["input_text"]=input_text
    result["predictions"]=model.single_prediction(input_text)
    predictions.append(result)
    # print(predictions)
    return model.single_prediction(input_text)

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": predictions }
