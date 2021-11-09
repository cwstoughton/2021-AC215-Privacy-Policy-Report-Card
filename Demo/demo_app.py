from fastapi import FastAPI
from models.inference_backend import model
# from models.gpt2_generator import generate_text

app = FastAPI()

@app.get("/predict")
async def predict(input_text: str):
    return model.single_prediction(input_text)
