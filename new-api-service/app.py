from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/predict")
async def get_predictions():
    return { "data": predictions }

@app.post("/predict_new")
async def predict(input_text: str):
    print(input_text)
    result = dict()
    result["input_text"]=input_text
    result["predictions"]=model.single_prediction(input_text)
    predictions.append(result)
    # print(predictions)
    return model.single_prediction(input_text)



{
    "data": {
        {
            "input_text": "We collect cookies",
            "identifier_score": 0.1,
            "identifier_sentences": ["We collect cookies"],
            "location_score": 0.1,
            "location_sentences": ["We collect cookies"],
            "third_party_score": 0.1,
            "third_party_sentences": ["We collect cookies"],
        }
    }
}

