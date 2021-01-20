import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import TensorBoard

import pickle
import numpy as np
import os
import string

file = open("8119-0.txt", "r", encoding = "utf8")
lines = []

for line in file:
    if line and line.strip():
        lines.append(line)

# Merge every word to one string

data = ""

for i in lines:
    data = ' '.join(lines)

# map punctuation to space, remove new line marks
data = data.replace('\n', '').replace('\r', '').replace('\ufeff', '')
translator = str.maketrans(string.punctuation, ' '*len(string.punctuation)) 
new_data = data.translate(translator)

# Remove duplicates

z = []

for i in data.split():
    if i not in z:
        z.append(i)
        
data = ' '.join(z)

tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])

pickle.dump(tokenizer, open('tokenizer1.pkl', 'wb'))

sequence_data = tokenizer.texts_to_sequences([data])[0]


print("\n\nFINAL PROGRAM: \n")
print(sequence_data[:10])

vocab_size = len(tokenizer.word_index) + 1
print(vocab_size)



sequences = []

for i in range(1, len(sequence_data)):
    words = sequence_data[i-1:i+1]
    sequences.append(words)
    
print("The Length of sequences are: ", len(sequences))
sequences = np.array(sequences)
print(sequences[:10])

X = []
y = []

for i in sequences:
    X.append(i[0])
    y.append(i[1])
    
X = np.array(X)
y = np.array(y)

print("The Data is: ", X[:5])
print("The responses are: ", y[:5])

y = to_categorical(y, num_classes=vocab_size)
print(y[:5])

model = Sequential()
model.add(Embedding(vocab_size, 10, input_length=1))
model.add(LSTM(1000, return_sequences=True))
model.add(LSTM(1000))
model.add(Dense(1000, activation="relu"))
model.add(Dense(vocab_size, activation="softmax"))

print(model.summary())

checkpoint = ModelCheckpoint("nextword1.h5", monitor='loss', verbose=1,
    save_best_only=True, mode='auto')

reduce = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=3, min_lr=0.0001, verbose = 1)

logdir='logsnextword1'
tensorboard_Visualization = TensorBoard(log_dir=logdir)


model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.001))
model.fit(X, y, epochs=150, batch_size=64, callbacks=[checkpoint, reduce, tensorboard_Visualization])