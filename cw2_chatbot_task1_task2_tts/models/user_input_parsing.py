from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import os

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["myChatDatabase"]
book_db = db["booking"]

print("Current working directory:", os.getcwd())

# Function to safely parse dates
def safe_parse_date(date_text):
    try:
        parsed_date = parse(date_text, fuzzy=True)
        return parsed_date.strftime('%d%m')
    except ValueError:
        return 'Invalid date format'

# Function to safely parse times
def safe_parse_time(time_text):
    try:
        parsed_time = parse(time_text, fuzzy=True)

        return parsed_time.strftime('%H%M')
    except ValueError:
        return 'Invalid time format'

# Function to extract information
def extract_info(info):
    print("Type of info:", type(info))
    updated_info = {}
    for key, value in info.items():
        if 'date' in key.lower():
            value = safe_parse_date(value)
        elif 'time' in key.lower():
            value = safe_parse_time(value)
            hour = value[:2]
            minute = value[2:]
            if key == 'departure_time':  # Extract hour and minute
                updated_info['departure_hrs'] = hour
                updated_info['departure_mins'] = minute
            if key == 'return_time':  # Extract hour and minute
                updated_info['return_hrs'] = hour
                updated_info['return_mins'] = minute
        updated_info[key] = value
    update_session_data(updated_info)
    return updated_info

def update_session_data(session):
    if any(value is not None for value in session.values()):
        id = {"_id": 1}
        
        data_to_update = {
            "$set": {
                key: value
                for key, value in session.items() if value is not None
            }
        }
        book_db.update_one(id, data_to_update, upsert=True)