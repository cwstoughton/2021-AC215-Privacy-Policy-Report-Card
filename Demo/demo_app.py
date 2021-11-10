from fastapi import FastAPI
from demo_inference_backend import model


app = FastAPI()

@app.get("/predict")
async def predict(input_text: str):
    return model.single_prediction(input_text)
