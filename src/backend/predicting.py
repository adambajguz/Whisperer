from tensorflow.keras.models import load_model
import numpy as np
import pickle

# Load the model and tokenizer

# model = load_model('nextword_en.h5')
# tokenizer = pickle.load(open('tokenizer_en.pkl', 'rb'))

def Predict_Next_Words(model, tokenizer, text):

    sequence = tokenizer.texts_to_sequences([text])[0]
    sequence = np.array(sequence)
        
    preds = np.argsort(model.predict(sequence), axis=-1)[0][-5:][::-1]
    print(preds)
    # predicted_word = ""

    result_dict = {}
        
    for key, value in tokenizer.word_index.items():
        if value in preds:
            # predicted_word = key
            result_dict[value] = key
            #print(value," - ", key)
    # print("final dict: ", result_dict)
    final_list = []
    for item in preds:
        final_list.append(result_dict[item])

    # print("Final list: ", final_list)
    return final_list


# while(True):

#     text = input("Enter your line: ")
    
#     if text == "stop the script":
#         print("Ending The Program.....")
#         break
    
#     else:
#         try:
#             text = text.split(" ")
#             text = text[-1]

#             text = ''.join(text)
#             Predict_Next_Words(model, tokenizer, text)
            
#         except:
#             continue