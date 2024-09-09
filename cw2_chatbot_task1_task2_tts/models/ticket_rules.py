from experta import *
from models.user_input_parsing import extract_info
from models.web_scraping import find_the_price

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["myChatDatabase"]
book_db = db["booking"]
station_db = db["stations"]

class Book(Fact):
    """Info about the booking ticket."""
    pass

class TrainBot(KnowledgeEngine):
  def __init__(self):
      super().__init__()
      self.action = None
  @Rule(Book(ticket='one way', info=MATCH.info))
  def one_way(self, info):
    for record in info:
      extratced_info = extract_info(record)
    url = f"https://www.nationalrail.co.uk/journey-planner/?type=single&origin={extratced_info['start_station']}&destination={extratced_info['destination_station']}&leavingType=departing&leavingDate={extratced_info['departure_date']}24&leavingHour={extratced_info['departure_hrs']}&leavingMin={extratced_info['departure_mins']}&adults=1&extraTime=0#TD"
    price = find_the_price(url)
    if price == float('inf'):
      self.action == 'No fares available. Please choose another journey.'
    else:
      self.action = f"I found the cheapest ticket for your journey! Here is the link, go an book now: {url}"
      book_db.delete_many({})
    

  @Rule(Book(ticket='round', info=MATCH.info))
  def round_way(self, info):
    for record in info:
      extratced_info = extract_info(record)
    url = f"https://www.nationalrail.co.uk/journey-planner/?type=return&origin={extratced_info['start_station']}&destination={extratced_info['destination_station']}&leavingType=departing&leavingDate={extratced_info['departure_date']}24&leavingHour={extratced_info['departure_hrs']}&leavingMin={extratced_info['departure_mins']}&returnType=departing&returnDate={extratced_info['return_date']}24&returnHour={extratced_info['return_hrs']}&returnMin={extratced_info['return_mins']}&adults=1&extraTime=0#O"
    print(url)
    price = find_the_price(url)
    if price == float('inf'):
      self.action == 'No fares available. Please choose another journey.'
    else:
      self.action = f"I found the cheapest ticket for your journey! Here is the link, go an book now: {url}"


def check_ticket(user_input):
    single_keywords = ['one way', 'single']
    return_keywords = ['return', 'round trip']

    input_lower = user_input.lower()

    for keyword in single_keywords:
        if keyword in input_lower:
            return 'one way'

    for keyword in return_keywords:
        if keyword in input_lower:
            return 'round'

    return None


# def check_travel_plan(user_input):
#     travel_keywords = ['from', 'to']
#     if all(keyword in user_input for keyword in travel_keywords):
#         return user_input
#     return None
# def expert_response(user_input):
    
#     ticket_type = check_ticket(user_input)
#     if ticket_type != None:
#           return 'ask for travel plan', ticket_type
#     elif ticket_type is None:
#         # user_input = input('Would you like to book a one way, round trip or an open return ticket?\n')
#           return 'new prompt'
    
    
 

