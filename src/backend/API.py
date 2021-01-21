from typing import Optional
from keras.preprocessing.sequence import pad_sequences

from fastapi import FastAPI
import predicting as pred
from tensorflow.keras.models import load_model
import numpy as np
import pickle

app = FastAPI()
model = load_model('nextword_seq_of_three.h5')
tokenizer = pickle.load(open('tokenizer_seq_of_three.pkl', 'rb'))

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/predict")
def predict(sentence: Optional[str] = None, count: Optional[int] = 5):
    text = sentence.strip().lower()
    enc_text = tokenizer.texts_to_sequences([text])[0]
    pad_enc = pad_sequences([enc_text], maxlen=3,truncating='pre')
    print(enc_text,pad_enc)
    result = []
    for i in (model.predict(pad_enc)[0]).argsort()[-count:][::-1]:
        pred_word = tokenizer.index_word[i]
        result.append(pred_word)
        print("Next word suggestion:",pred_word)
        
    return {"predicted_words": result}