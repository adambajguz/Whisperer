from typing import Optional

from fastapi import FastAPI
import predicting as pred
from tensorflow.keras.models import load_model
import numpy as np
import pickle

app = FastAPI()
model = load_model('nextword_en.h5')
tokenizer = pickle.load(open('tokenizer_en.pkl', 'rb'))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/predict")
def predict(sentence: Optional[str] = None):
    text = sentence.split(" ")
    text = text[-1]

    text = ''.join(text)
    result = pred.Predict_Next_Words(model, tokenizer, text)
    return {"predicted_words": result}