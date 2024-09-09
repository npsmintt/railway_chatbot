# import spacy
# import pymongo
# from dateutil.parser import parse

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["myChatDatabase"]
# book_db = db["booking"]
# station_db = db["stations"]

# result = book_db.find({"_id": 1})

# def extract_info(info):
#     updated_info = {}
#     for key, value in info.items():
#         if 'date' in key.lower():
#             print(f'old date: {value}')
#             value = safe_parse_date(value)
#             print(f'updated date: {value}')
#         elif 'time' in key.lower():
#             print(f'old time: {value}')
#             value = safe_parse_time(value)
#             hour = value[:2]
#             minute = value[2:]
#             print(f'updated time: {value}')
#             if key == 'departure_time':  # Extract hour and minute
#                 updated_info['departure_hrs'] = hour
#                 updated_info['departure_mins'] = minute
#             if key == 'return_time':  # Extract hour and minute
#                 updated_info['return_hrs'] = hour
#                 updated_info['return_mins'] = minute
#         updated_info[key] = value
#     update_session_data(updated_info)
#     return updated_info

# def safe_parse_date(date_text):
#     try:
#         parsed_date = parse(date_text, fuzzy=True)
#         return parsed_date.strftime('%d%m')
#     except ValueError:
#         return 'Invalid date format'

# def safe_parse_time(time_text):
#     try:
#         parsed_time = parse(time_text, fuzzy=True)

#         return parsed_time.strftime('%H%M')
#     except ValueError:
#         return 'Invalid time format' 
    
# def update_session_data(session):
#     if any(value is not None for value in session.values()):
#         id = {"_id": 1}
        
#         data_to_update = {
#             "$set": {
#                 key: value
#                 for key, value in session.items() if value is not None
#             }
#         }
#         book_db.update_one(id, data_to_update, upsert=True)

# for record in result:
#     print(f'old data: {record}')
#     extracted_data = extract_info(record)
#     print(f'extracted data: {extracted_data}')
# from datetime import datetime
# current_date = datetime.now()
# current_time = current_date.time()
# departure_date = datetime.strptime('2105'+'24', "%d%m%y").date()
# print(departure_date)
# print(datetime.strptime('1000'+'00','%H%M%S').time() > current_time)

# import ace_tools as tools
# import pandas as pd

# # Load the data
# file_path = '/Users/thisgirlcan/Desktop/railway_chatBot/cw2_chatbot_task1_task2/journey2.csv'
# data = pd.read_csv(file_path)

# # Display basic statistics and a sample of the data
# data_info = data.describe()
# data_sample = data.head()

# tools.display_dataframe_to_user(name="Data Statistics", dataframe=data_info)
# tools.display_dataframe_to_user(name="Data Sample", dataframe=data_sample)
