import os
import random
import json
import torch
from datetime import *
from models.predict_intention_model import NeuralNet
from models.bag_of_words import bag_of_words, tokenize
import re
import spacy
from models.contingency_reasoning import give_advice, adviseBot
from models.knowledge_acquisition import addBot, add_contingency_plan

import mysql.connector

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="234236238",
    database="chatbot_contingency"
)

cursor = db_connection.cursor()

nlp = spacy.load("en_core_web_md")

# reasoning engine for contingency advice
advise_bot = adviseBot()
advise_bot.reset()

# reasoning engine for knowledge acquisition
add_bot = addBot()
add_bot.reset()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "intents.json")


with open(file_path) as json_data:
    intents = json.load(json_data)

data_dir = os.path.dirname(__file__)
FILE = os.path.join(data_dir, 'chatdata.pth')
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

contingency_data = {
    'event_type': None,
    'bl_location_a': None,
    'bl_location_b': None,
    'time': None,
    'severity': None
}

session = 'default'
response_dict = {"reply": "", "data_type": "", "data_content": ""}


def get_response(msg):
    global session
    global response_dict
    if session == 'default':
        sentence = tokenize(msg)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        # return the intention tag with the highest probability score
        if prob.item() > 0.75:
            response_dict = {"reply": "", "data_type": "", "data_content": ""}
            if tag == 'advice':
                session = 'advice'
                response_dict["reply"] = give_advice(msg)
                return response_dict
            elif tag == 'add':
                add_bot.reset()
                session = 'add'
                response_dict["reply"] = add_contingency_plan(msg)
                return response_dict
            else:
                response_dict["reply"] = random.choice(next((intent['responses'] for intent in intents['intents'] if intent["tag"] == tag), []))
                return response_dict
        else:
            response_dict["reply"] = "Sorry, I don't understand that. I can help you handle any contingencies if you tell me more information."
            response_dict["data_type"] = ""
            response_dict["data_content"] = ""
            return response_dict
        
    elif session == 'advice':
        response_dict = {"reply": "", "data_type": "", "data_content": ""}
        response_dict["reply"] = give_advice(msg)
        print(f'session: {session}')
        return response_dict

    elif session == 'add':
        response_dict = {"reply": "", "data_type": "", "data_content": ""}
        response_dict["reply"] = add_contingency_plan(msg)
        print(f'session: {session}')
        return response_dict
    


