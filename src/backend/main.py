import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import TensorBoard

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

import pickle
import numpy as np
import os
import string

file = open("metamorphosis_clean.txt", "r", encoding = "utf8")
lines = []

for line in file:
    if line and line.strip() and not line.startswith("CHAPTER"):
        lines.append(line)

# Merge every word to one string

print("file_loaded")

data = ""
data = ' '.join(lines)
print(data[:360])

print("file merged!")
data = data.replace('\n', '').replace('\r', '').replace('\ufeff', '').replace(',','').replace('‘','').replace('’','').replace(',','')
print(data[:360])
print("file cleared!")

tokens = word_tokenize(data)
print(tokens[:10])

train_len = 4
text_sequences = []

for i in range(train_len,len(tokens)):
    s = tokens[i-train_len:i]
    text_sequences.append(s)

sequences = {}
count = 1

for i in range(len(tokens)):
    if tokens[i] not in sequences:
        sequences[tokens[i]]=count
        count += 1

print(sequences)
print("text seq:")
print(text_sequences[:10])
tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_sequences)
sequences = tokenizer.texts_to_sequences(text_sequences)

voc_size = len(tokenizer.word_counts) + 1
n_sequences = np.empty([len(sequences),train_len], dtype='int32')

for i in range(len(sequences)):
    n_sequences[i] = sequences[i]

train_inputs = n_sequences[:,:-1]
train_targets = n_sequences[:,-1]
train_targets = to_categorical(train_targets,num_classes=voc_size)
seq_len = train_inputs.shape[1]

print("seq")
print(sequences[:10])
print("seq_len:",seq_len)

pickle.dump(tokenizer, open('tokenizer_seq_of_three.pkl', 'wb'))

model = Sequential()
model.add(Embedding(voc_size, seq_len, input_length=seq_len))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation="relu"))
model.add(Dense(voc_size, activation="softmax"))

print(model.summary())

checkpoint = ModelCheckpoint("nextword_seq_of_three.h5", monitor='loss', verbose=1,
    save_best_only=True, mode='auto')

reduce = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=3, min_lr=0.0001, verbose = 1)

logdir='logsnextword_wep_meta'
tensorboard_Visualization = TensorBoard(log_dir=logdir)


model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.001), metrics=['accuracy'])
model.fit(train_inputs, train_targets, epochs=500, callbacks=[checkpoint, reduce, tensorboard_Visualization])