from fastapi import FastAPI
from demo_inference_backend import model
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
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



@app.get("/predict")
async def predict(input_text: str):
    # return model.single_prediction(input_text)
    return { "data": todos }

@app.post("/predict")
async def predict(input_text: str):
    print(input_text)
    result = dict()
    result["input_text"]=input_text
    result["predictions"]=model.single_prediction(input_text)
    predictions.append(result)
    print(predictions)
    return model.single_prediction(input_text)

@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": predictions }
