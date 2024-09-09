import os
import random
import json
import torch
from datetime import *
from models.model import NeuralNet
from models.bag_of_words import bag_of_words, tokenize
from models.ticket_rules import TrainBot, Book, check_ticket
import re
import spacy
from models.delay_reasoning import predict_delay, PredictionBot
from models.ticket_reasoning import book_ticket, TicketBot

# from fuzzywuzzy import fuzz

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["myChatDatabase"]
book_db = db["booking"]
station_db = db["stations"]

nlp = spacy.load("en_core_web_md")
prediction_bot = PredictionBot()
booking_bot = TicketBot()
booking_bot.reset()
prediction_bot.reset()


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

# booking = {
#     'ticket_type': None,
#     'start_station': None,
#     'destination_station': None,
#     'departure_date': None,
#     'departure_time': None,
#     'return_date': None,
#     'return_time': None,
#     'expecting': None
# }

session = 'default'

# function for updating data to booking database


def update_booking_data(booking):
    if any(value is not None for value in booking.values()):
        id = {"_id": 1}

        data_to_update = {
            "$set": {
                key: value
                for key, value in booking.items() if value is not None
            }
        }
        book_db.update_one(id, data_to_update, upsert=True)

############


def get_response(msg):
    global session
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

        if prob.item() > 0.75:
            if tag == 'bye':
                # session = 'default'
                # booking_bot.reset()
                # prediction_bot.reset()
                return 'Thank you. Goodbye!'
            elif tag == 'book':
                session = 'book'
                booking_bot.reset()
                return book_ticket(msg)
            elif tag == 'delay':
                session = 'delay'
                prediction_bot.reset()
                return predict_delay(msg)
            else:
                return random.choice(next((intent['responses'] for intent in intents['intents'] if intent["tag"] == tag), []))
        return "Sorry, I don't understand that. I can help you book a ticket, predict train delays, or help you handle any contingencies."

    elif session == 'book':
        # if book_ticket(msg, booking):
        # if booking.get('expecting'):
        return book_ticket(msg)

    elif session == 'delay':
        prediction_bot.reset()
        return predict_delay(msg)


# def handle_direct_response(msg, booking):
#     parsed_details = parse_comprehensive_input(msg)
#     if parsed_details:
#         booking.update(parsed_details)
#         update_booking_data(booking)
#         if all_data_collected(booking):
#             return finalize_booking(booking)
#         else:
#             return ask_for_missing_details(booking)

#     expected = booking.get('expecting')
#     if expected:
#         if expected in ['start_station', 'destination_station']:
#             # Check if the input matches multiple stations
#             if msg not in find_matching_stations(msg):
#                 station_name = extract_station_name(msg)
#                 if station_name:
#                     matching_stations = find_matching_stations(station_name)
#                     if matching_stations:
#                         if len(matching_stations) == 1:
#                             station_code = get_station_code(
#                                 matching_stations[0])
#                             booking[expected] = station_code
#                         else:
#                             return f"There are multiple matched stations. Could you please specify your station again?\n" + '\n'.join([f"- {station}" for station in matching_stations])
#             else:
#                 station_code = get_station_code(msg)
#                 booking[expected] = station_code
#         elif expected == 'ticket_type':
#             msg = msg.lower()
#             if 'one way' in msg or 'return' in msg or 'round trip' in msg:
#                 booking['expecting'] = 'start_station'
#                 booking['ticket_type'] = check_ticket(msg)
#                 update_booking_data(booking)
#                 return ask_for_next('travel_plan')
#         else:
#             booking[expected] = msg
#         booking['expecting'] = next_expected_field(booking, expected)
#         update_booking_data(booking)

#         if booking['expecting']:
#             return ask_for_next(booking['expecting'])
#         if all_data_collected(booking):
#             return finalize_booking(booking)

#     return "Please provide more details to continue with your booking."


def extract_station_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Type: {ent.label_}")
        if ent.label_ in ['GPE', 'FAC', 'PERSON', 'ORG']:
            return ent.text
    return None


def find_matching_stations(station_name):
    matching_stations = list(station_db.find(
        {"stationName": {"$regex": station_name, "$options": "i"}}))
    if matching_stations:
        return [station['stationName'] for station in matching_stations]
    return []


# def parse_comprehensive_input(text):
#     pattern = r"from (?P<start_station>[^ ]+) to (?P<destination_station>[^ ]+) at (?P<departure_time>\d{1,2}(?: ?[ap]m)?) on (?P<departure_date>\w+ \d{1,2})"
#     match = re.search(pattern, text, re.IGNORECASE)
#     if match:
#         return match.groupdict()
#     return {}


# def ask_for_missing_details(booking):
#     for field in ['ticket_type', 'start_station', 'destination_station', 'departure_date', 'departure_time', 'return_date', 'return_time']:
#         if not booking[field]:
#             return ask_for_next(field)
#     return "Please check the details you provided and provide the missing ones."


# def next_expected_field(booking, current_field):
#     if booking['ticket_type'] == 'one way':
#         fields_in_order = ['ticket_type', 'start_station', 'destination_station',
#                            'departure_date', 'departure_time']
#         try:
#             next_index = fields_in_order.index(current_field) + 1
#             return fields_in_order[next_index]
#         except IndexError:
#             return None
#     else:
#         fields_in_order = ['ticket_type', 'start_station', 'destination_station',
#                            'departure_date', 'departure_time', 'return_date', 'return_time']
#         try:
#             next_index = fields_in_order.index(current_field) + 1
#             return fields_in_order[next_index]
#         except IndexError:
#             return None


# def ask_for_next(field):
#     prompts = {
#         'travel_plan': "Ok! Tell me your travel plan!",
#         'ticket_type': "Would you like to book a one way or round trip ticket?",
#         'start_station': "Where is your start station?",
#         'destination_station': "Where is your destination?",
#         'departure_date': "What date are you leaving?",
#         'departure_time': "What time would you like to depart?",
#         'return_date': "What date are you returning?",
#         'return_time': "What time would you like to return?"
#     }
#     return prompts.get(field, "Please provide more details to continue with your booking.")


# def finalize_booking(booking):
#     if not all_data_collected(booking):
#         return "Error: Missing information. Please ensure all required details are provided."

#     info = book_db.find({"_id": 1})
#     info_ticket = book_db.find_one({"_id": 1})
#     ticket_type = info_ticket.get('ticket_type')

#     action = process_booking(ticket_type, info)

#     booking.update({key: None for key in booking.keys()})

#     return action


# def book_ticket(msg, booking):
#     global session
#     msg = msg.lower()
#     if 'one way' in msg or 'return' in msg or 'round trip' in msg:
#         booking['expecting'] = 'start_station'
#         booking['ticket_type'] = check_ticket(msg)
#         booking['test'] = 'hey, test'
#         update_booking_data(booking)
#         return ask_for_next('travel_plan')
#     elif not booking['ticket_type']:
#         session = 'book'
#         booking['expecting'] = 'ticket_type'
#         return "Would you like to book a one way or round trip ticket?"


# def process_booking(ticket_type, travel_info):
#     global session
#     print(f'ticket_type = {ticket_type}')
#     train_bot.reset()
#     train_bot.declare(Book(ticket=ticket_type, info=travel_info))
#     train_bot.run()
#     if train_bot.action:
#         print(f"Action successfully set: {train_bot.action}")
#         session = 'default'
#         return train_bot.action
#     else:
#         print("Action not set; rules might not have fired correctly.")
#         return "Unable to process your request at this time. Please check the details and try again."


# def all_data_collected(booking):
#     if booking['ticket_type'] == 'one way':
#         return all(booking[key] is not None for key in ['ticket_type', 'start_station', 'destination_station', 'departure_date', 'departure_time'])
#     else:
#         return all(booking[key] is not None for key in
#                    ['ticket_type', 'start_station', 'destination_station', 'departure_date', 'departure_time',
#                     'return_date', 'return_time'])


def get_station_code(station_name):
    station = station_db.find_one(
        {"stationName": {"$regex": f'^{station_name}$', "$options": "i"}})
    return station['stationCode']
