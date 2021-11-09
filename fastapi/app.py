from fastapi import FastAPI
# from models.inference_backend import create_model
from model import generate

app = FastAPI()

@app.get("/predict")
async def predict(input_text: str):
    return generate(input_text)
