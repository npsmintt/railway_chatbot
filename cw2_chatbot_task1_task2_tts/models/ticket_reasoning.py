import pymongo
import random
import spacy
from experta import *
from models import chat
from dateutil.parser import parse
import re
from spacy.matcher import PhraseMatcher, Matcher
from models import web_scraping
from datetime import datetime
import math
from models import delay_reasoning
import nltk
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz, process
# Setup NLP and database connection
nlp = spacy.load("en_core_web_md")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["myChatDatabase"]
book_db = db["booking"]
station_db = db["stations"]


class TicketBot(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.all_booking_info = False
        self.all_booking_info_single = False
        self.response = None
        self.departing_station_set = False
        self.departing_time_set = False
        self.departing_date_set = False
        self.confirmed_journey_set = False
        self.confirmed_book_set =False

    def reset_engine(self):
        self.all_booking_info = False
        self.all_booking_info_single = False
        self.departing_station_set = False
        self.departing_time_set = False
        self.departing_date_set = False
        self.confirmed_journey_set = False
        self.confirmed_book_set = False
        print("Engine has been reset and ready for new booking.")

    def update_booking_type(self, ticket_type):
        if ticket_type == 'one way':
            self.all_booking_info_single = True
            self.all_booking_info = False
        elif ticket_type == 'round':
            self.all_booking_info_single = False
            self.all_booking_info = True
    
    def parse_date_back(self, date_text):
        try:
            parsed_date = parse(date_text, fuzzy=True)
            return parsed_date.strftime('%d %B')
        except ValueError:
            return 'Invalid date format'
    def parse_time_back(self, time_text):
        try:
            parsed_time = datetime.strptime(time_text, fuzzy=True).time()
            return parsed_time.strftime('%H:%M')
        except ValueError:
            return 'Invalid time format'

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="book ticket")

    @Rule(Fact(action='book ticket'),
          NOT(Fact(ticket_type=W())))
    def ask_ticket_type(self):
        self.response = 'Would you like to book a one way or return ticket?'

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          NOT(Fact(departing_station=W())))
    def ticket_type_confirmed(self, ticket_type):
        self.response = f'Great, a {ticket_type} ticket. Which station are you departing from?'

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(departing_station=MATCH.departing_station),
          NOT(Fact(confirmed_departing_station=W())))
    def process_departing_station(self, departing_station):
        station_code = self.station_code_matcher(departing_station)
        print(f"station_code:{station_code}")
        if isinstance(station_code, str) and "multiple matched stations" in station_code:
            self.response = station_code
        elif station_code:
            self.declare(Fact(confirmed_departing_station=station_code))
            self.departing_station_set = True
        else:
            self.response = "The station provided is not valid, please enter a valid station."

    def station_code_matcher(self, departing_station):
        if departing_station == 'Oxford':
            matching_stations = ['Oxford']
        elif departing_station == 'Cambridge':
            matching_stations = ['Cambridge']
        elif departing_station == 'Manchester Oxford Road':
            matching_stations = ['Manchester Oxford Road']
        elif departing_station == 'Bedford':
            matching_stations = ['Bedford']
        else:
            matching_stations = chat.find_matching_stations(departing_station)
            print(f"matching_station:{matching_stations}")
        if matching_stations:
            if len(matching_stations) == 1:
                return chat.get_station_code(matching_stations[0])
            else:
                return f"There are multiple matched stations. Could you please specify your station again?\n" + '\n'.join([f"- {station}" for station in matching_stations])
        return None

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(departing_station=MATCH.departing_station),
          NOT(Fact(destination_station=W())))
    def ask_destination_station(self, departing_station):
        self.response = f'You are traveling from {departing_station}. Where are you going to?'
        # self.departing_station_set = True

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(destination_station=MATCH.destination_station),
          NOT(Fact(confirmed_destination_station=W())))
    def process_destination_station(self, destination_station):
        station_code = self.destination_station_code_matcher(
            destination_station)
        print(f'station_code for destination: {station_code}')
        if isinstance(station_code, str) and "multiple matched stations" in station_code:
            self.response = station_code
        elif station_code:
            self.declare(Fact(confirmed_destination_station=station_code))
           
        else:
            self.response = "The station provided is not valid, please enter a valid station."

    def destination_station_code_matcher(self, destination_station):
        if destination_station == 'Oxford':
            matching_stations = ['Oxford']
        elif destination_station == 'Cambridge':
            matching_stations = ['Cambridge']
        elif destination_station == 'Manchester Oxford Road':
            matching_stations = ['Manchester Oxford Road']
        elif destination_station == 'Bedford':
            matching_stations = ['Bedford']
        else:
            matching_stations = chat.find_matching_stations(
                destination_station)

        if matching_stations:
            if len(matching_stations) == 1:
                return chat.get_station_code(matching_stations[0])
            else:
                return f"There are multiple matched stations. Could you please specify your station again?\n" + '\n'.join([f"- {station}" for station in matching_stations])
        return None

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          NOT(Fact(departure_date=W())))
    def ask_date(self, departing_station, destination_station):
        self.response = f'You are traveling from {departing_station} to {destination_station}. What date are you leaving?\nPlease provide a date that is not earlier than the current date.'
      

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          NOT(Fact(departure_time=W())),
          Fact(departure_date=MATCH.departure_date))
    def ask_time(self, departing_station, destination_station, departure_date):
        self.response = f'You are travelling from {departing_station} to {destination_station} on {departure_date[0:2]}/{departure_date[2:]}. What time are you leaving? Please provide a time that is not earlier than the current time.'
        self.departing_date_set = True
    
    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_time=MATCH.departure_time),
          Fact(departure_date=MATCH.departure_date),
          NOT(Fact(confirmed_journey=W())))
    def ask_user_to_confirm(self, departing_station, destination_station, departure_date, departure_time):
        if self.all_booking_info_single:
            self.response = f'You are travelling from {departing_station} to {destination_station} on {departure_date[0:2]}/{departure_date[2:]} at {departure_time[0:2]}:{departure_time[2:]}. Is that correct?'
            self.departing_time_set = True
    
    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_time=MATCH.departure_time),
          Fact(departure_date=MATCH.departure_date),
          Fact(confirmed_journey=MATCH.confirmed_journey),
          NOT(Fact(confirmed_book=W())))
    def ask_user_to_confirm_book(self):
        if self.all_booking_info_single:
                self.response = f'Now we got all the information needed to find the cheapest ticket for your journey and it may take some time. Enter \'OK\' to continue.'
        
           

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_date=MATCH.departure_date),
          Fact(departure_time=MATCH.departure_time),
          Fact(confirmed_journey=MATCH.confirmed_journey),
          Fact(confirmed_book=MATCH.confirmed_book)
          )
    def all_booking_info_complete_single(self, ticket_type, departing_station, destination_station, confirmed_departing_station, confirmed_destination_station, departure_date, departure_time, confirmed_journey, confirmed_book):
        if self.all_booking_info_single:
            booking_info_single = {'ticket_type': ticket_type,
                                   'departing_station': confirmed_departing_station,
                                   'destination_station': confirmed_destination_station,
                                   'departure_date': departure_date,
                                   'departure_time': departure_time,
                                   'confirmed_jouney': confirmed_journey,
                                   'confirmed_book':confirmed_book
                                   }
            print(f"all_booking_info_single in rules:{booking_info_single}")

            if None not in booking_info_single.values():
                now = datetime.now()
                current_date = now.strftime("%d-%b-%Y")
                current_time = now.strftime("%H:%M")
                self.departing_time_set = True
                url = f"https://www.nationalrail.co.uk/journey-planner/?type=single&origin={confirmed_departing_station}&destination={confirmed_destination_station}&leavingType=departing&leavingDate={departure_date}24&leavingHour={departure_time[0:2]}&leavingMin={departure_time[2:]}&adults=1&extraTime=0#TD"
                price = web_scraping.find_the_price(url)
                print(f"price:{price}")
                if not math.isinf(price) and price is not None and price > 0:
                    # ticket_div = f""""""
                    self.response = (
                        f"""🥳 We found the cheapest ticket for your journey! The cheapest price of your journey is £{price}. Click <a href="{url}" target="_blank">Here</a> to book your ticket now! And here is your ticket, enjoy your journey!<div id="ticket">
        <div class="header">

                <div class="image-container">
                    <img
                        src="https://blush.design/api/download?shareUri=PCLyiGLtEO8oJq0R&c=Skin_0%7Effdbb4&w=800&h=800&fm=png"
                        alt="logo">
                    <img
                        src="https://blush.design/api/download?shareUri=QifzoaZsCtS5OmEU&c=Skin_0%7Effdbb4&w=800&h=800&fm=png"
                        alt="logo">
                    <img
                        src="https://blush.design/api/download?shareUri=UmSLTt2J3BfO9Z2k&c=Skin_0%7Effdbb4&w=800&h=800&fm=png"
                        alt="logo">

                </div>
                <div>
                    <p>Developed By Mint, Wen and Shan<p>
                </div>
                </div>
        <div class="content">
            <div class="section">
                <div class="item">
                    <div>Class</div>
                    <div>STD</div>
                </div>
                <div class="item">
                    <div>Ticket type</div>
                    <div>{ticket_type.upper()}</div>
                </div>
                <div class="item">
                    <div>Adult</div>
                    <div>ONE</div>
                </div>
                <div class="item">
                    <div>Child</div>
                    <div>NIL</div>
                </div>
            </div>
            <div class="section">
                <div class="item">
                    <div>Start date</div>
                    <div>{departure_date[0:2]}-{departure_date[2:]}-24</div>
                </div>
                <div class="item">
                    <div>Number</div>
                    <div>{random.randint(10000, 99999)}</div>
                </div>
            </div>
            <div class="section">
                <div class="item">
                    <div>From</div>
                    <div>{departing_station} *</div>
                </div>
                <div class="item">
                    <div>Valid until</div>
                    <div>{departure_date[0:2]}-{departure_date[2:]}-24</div>
                </div>
                <div class="item">
                    <div>Price</div>
                    <div>£{price}</div>
                </div>
            </div>
            <div class="section">
                <div class="item">
                    <div>To</div>
                    <div>{destination_station} *</div>
                </div>
                <div class="item">
                    <div>Time</div>
                    <div>{departure_time}</div>
                </div>
            </div>
        </div>
        <div class="footer">

            <div class="left">Group 3 Railway</div>
            <div class="right">Printed {current_time} on {current_date}</div>
        </div>
    </div>
            """)

                else:
                    # If price is 'inf', 'None', or not greater than zero
                    self.response = '😢 Sorry, currently we have no available tickets for your journey, please go back and choose another one'

                chat.session = 'default'
                self.reset_engine()
                self.reset()
      

            else:
                self.response = 'Some information is missing. Please provide all required details.'

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departure_time=MATCH.departure_time),
          Fact(departure_date=MATCH.departure_date),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          NOT(Fact(returning_date=W())))
    def ask_return_date(self, departure_date, departure_time, departing_station, destination_station):
        if self.all_booking_info:
            self.response = f'You are travelling from {departing_station} to {destination_station} on {departure_date[0:2]}/{departure_date[2:]} at {departure_time[0:2]}:{departure_time[2:]}. What date are you returning?\nPlease provide a date that is not earlier than the current date.'
            self.departing_time_set = True

    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_time=MATCH.departure_time),
          Fact(departure_date=MATCH.departure_date),
          Fact(returning_date=MATCH.returning_date),
          NOT(Fact(returning_time=W())))
    def ask_return_time(self, departing_station, destination_station, departure_date, departure_time, returning_date):
        if self.all_booking_info:
            self.response = f'You are travelling from {departing_station} to {destination_station} on {departure_date} at {departure_time} and returning on {returning_date[0:2]}/{returning_date[2:]}. What time are you returning?\nPlease provide a time that is not earlier than the current time.'
            self.departing_time_set = True
    
    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_time=MATCH.departure_time),
          Fact(departure_date=MATCH.departure_date),
          Fact(returning_date=MATCH.returning_date),
          Fact(returning_time=MATCH.returning_time),
          NOT(Fact(confirmed_journey_return=W())))
    def ask_user_to_confirm_return(self, departing_station, destination_station, departure_date, departure_time, returning_date, returning_time):
        if self.all_booking_info:
            self.response = f'You are travelling from {departing_station} to {destination_station} on {departure_date[0:2]}/{departure_date[2:]} at {departure_time[0:2]}:{departure_time[2:]} and returning on {returning_date[0:2]}/{returning_date[2:]} at {returning_time[0:2]}:{returning_time[2:]}. Is that correct?'
            self.confirmed_journey_set = True
    
    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_time=MATCH.departure_time),
          Fact(departure_date=MATCH.departure_date),
          Fact(returning_date=MATCH.returning_date),
          Fact(returning_time=MATCH.returning_time),
          Fact(confirmed_journey_return=MATCH.confirmed_journey_return),
          NOT(Fact(confirmed_book_return=W())),)
    def ask_user_to_confirm_book_return(self, confirmed_journey_return):
        if self.all_booking_info:
            self.response = f'Now we got all the information needed to find the cheapest ticket for your journey and it may take some time. Enter \'OK\' to continue.'
            self.confirmed_book_set = True


    @Rule(Fact(action='book ticket'),
          Fact(ticket_type=MATCH.ticket_type),
          Fact(confirmed_departing_station=MATCH.confirmed_departing_station),
          Fact(confirmed_destination_station=MATCH.confirmed_destination_station),
          Fact(departing_station=MATCH.departing_station),
          Fact(destination_station=MATCH.destination_station),
          Fact(departure_date=MATCH.departure_date),
          Fact(departure_time=MATCH.departure_time),
          Fact(returning_date=MATCH.returning_date),
          Fact(returning_time=MATCH.returning_time),
          Fact(confirmed_journey_return=MATCH.confirmed_journey_return),
          Fact(confirmed_book_return=MATCH.confirmed_book_return))
    def all_booking_info_complete_return(self, ticket_type, departing_station, destination_station, confirmed_departing_station, confirmed_destination_station, departure_date, departure_time, returning_date, returning_time, confirmed_journey_return, confirmed_book_return):
        if self.all_booking_info:
            booking_info = {'ticket_type': ticket_type,
                            'departing_station': confirmed_departing_station,
                            'destination_station': confirmed_destination_station,
                            'departure_date': departure_date,
                            'departure_time': departure_time,
                            'returning_date': returning_date,
                            'returning_time': returning_time,
                            'confirmed_jouney_return':confirmed_journey_return,
                            'confirmed_book_return': confirmed_book_return
                            }
            print(f"all_booking_info:{booking_info}")

            if None not in booking_info.values():
                now = datetime.now()
                current_date = now.strftime("%d-%b-%Y")
                current_time = now.strftime("%H:%M")
                url = f"https://www.nationalrail.co.uk/journey-planner/?type=return&origin={confirmed_departing_station}&destination={confirmed_destination_station}&leavingType=departing&leavingDate={departure_date}24&leavingHour={departure_time[0:2]}&leavingMin={departure_time[2:]}&returnType=departing&returnDate={returning_date}24&returnHour={returning_time[0:2]}&returnMin={returning_time[2:]}&adults=1&extraTime=0#O"
                price = web_scraping.find_the_price(url)
                print(f"price:{price}")
                if not math.isinf(price) and price is not None and price > 0:
                    self.response = (
                        f"""🥳 We found the cheapest ticket for your journey! The cheapest price of your journey is £{price}. Click <a href="{url}" target="_blank">Here</a> to book your ticket now! And here is your ticket, enjoy your journey! <div id="ticket">
        <div class="header">

                <div class="image-container">
                    <img
                        src="https://blush.design/api/download?shareUri=PCLyiGLtEO8oJq0R&c=Skin_0%7Effdbb4&w=800&h=800&fm=png"
                        alt="logo">
                    <img
                        src="https://blush.design/api/download?shareUri=QifzoaZsCtS5OmEU&c=Skin_0%7Effdbb4&w=800&h=800&fm=png"
                        alt="logo">
                    <img
                        src="https://blush.design/api/download?shareUri=UmSLTt2J3BfO9Z2k&c=Skin_0%7Effdbb4&w=800&h=800&fm=png"
                        alt="logo">

                </div>
                <div>
                    <p>Developed By Mint, Wen and Shan<p>
                </div>
                </div>
        <div class="content">
            <div class="section">
                <div class="item">
                    <div>Class</div>
                    <div>STD</div>
                </div>
                <div class="item">
                    <div>Ticket type</div>
                    <div>{ticket_type.upper()}</div>
                </div>
                <div class="item">
                    <div>Adult</div>
                    <div>ONE</div>
                </div>
                <div class="item">
                    <div>Child</div>
                    <div>NIL</div>
                </div>
            </div>
            <div class="section">
                <div class="item">
                    <div>Start date</div>
                    <div>{departure_date[0:2]}-{departure_date[2:]}-24</div>
                </div>
                <div class="item">
                    <div>Return date</div>
                    <div>{returning_date[0:2]}-{returning_date[2:]}-24</div>
                </div>
                <div class="item">
                    <div>Number</div>
                    <div>{random.randint(10000, 99999)}</div>
                </div>
            </div>
            <div class="section">
                <div class="item">
                    <div>From</div>
                    <div>{departing_station} *</div>
                </div>
                <div class="item">
                    <div>Valid until</div>
                    <div>{returning_date[0:2]}-{returning_date[2:]}-24</div>
                </div>
                <div class="item">
                    <div>Price</div>
                    <div>£{price}</div>
                </div>
            </div>
            <div class="section">
                <div class="item">
                    <div>To</div>
                    <div>{destination_station} *</div>
                </div>
                <div class="item">
                    <div>Start Time</div>
                    <div>{departure_time}</div>
                </div>
                <div class="item">
                    <div>Return Time</div>
                    <div>{returning_time}</div>
                </div>
            </div>
        </div>
        <div class="footer">

            <div class="left">Group 3 Railway</div>
            <div class="right">Printed {current_time} on {current_date}</div>
        </div>
    </div>
            """)

                else:

                    self.response = '😢 Sorry, currently we have no available tickets for your journey, please go back and choose another one'

                chat.session = 'default'
                self.reset_engine()
                self.reset()
              

            else:
                self.response = 'Some information is missing. Please provide all required details.'


bot = TicketBot()
bot.reset()


def parse_user_input_booking(user_input):
    ticket_type = check_ticket(user_input)
    user_input = user_input.title()
    dep_station = None
    arr_station = None
    departure_date = None
    departure_time = None
    returning_date = None
    returning_time = None
    confirmed_journey = None
    confirmed_journey_return = None
    confirmed_book = None
    confirmed_book_return = None

    matcher = Matcher(nlp.vocab)
    matcher_station = PhraseMatcher(nlp.vocab, attr='LOWER')
  


    # Time patterns setup
    # Define pattern
    time_patterns = [
        [{'IS_DIGIT': True}, {'TEXT': ':'}, {'IS_DIGIT': True}, {
            'IS_SPACE': True, 'OP': '?'}, {'LOWER': {'IN': ['am', 'pm']}, 'OP': '?'}],
        [{'IS_DIGIT': True}, {'LOWER': {'IN': ['am', 'pm']}}],
        [{'SHAPE': 'dddd'}],
        [{'LOWER': {'IN': ['half', 'quarter']}}, {'TEXT': 'past'}, {
            'IS_DIGIT': True, 'OP': '?'}, {'IS_ALPHA': True, 'OP': '?'}],
        [{'LOWER': {'IN': ['noon', 'midnight']}}]
    ]
    
    
    

    for pattern in time_patterns:
        matcher.add("TIME", [pattern])
    

    stations = station_db.find({}, {"stationName": 1, "_id": 0})

    station_terms = [station['stationName']
                     for station in stations if 'stationName' in station]
    # print(f"station_terms:{station_terms}")

    patterns = [nlp.make_doc(text) for text in station_terms]
    matcher_station.add("STATION", patterns)

    # Process document
    doc = nlp(user_input)

    # Apply both matchers
    matches_time = matcher(doc)
    # matches_yes_no = matcher(doc)
    
    if user_input.lower() in ['yes','no','nope','yeh','yep','right']:
        if not confirmed_journey and not bot.confirmed_journey_set:
            confirmed_journey = user_input
        elif not confirmed_journey_return:
            confirmed_journey_return = user_input
    elif user_input.lower() == 'ok':
        if not confirmed_book and not bot.confirmed_book_set:
            confirmed_book = user_input
        elif not confirmed_book_return:
            confirmed_book_return = user_input
    elif user_input.lower() == 'bye':
        chat.session = 'default'
        bot.reset_engine()
        bot.reset()
            
    found_stations = find_station_names(user_input, station_terms)
    
    ner_stations = [ent.text for ent in doc.ents if ent.label_ in [
        'GPE', 'FAC', 'PERSON', 'ORG']]

    print(f"ner_stations: {ner_stations}")
    if len(ner_stations) == 2:
        dep_station = ner_stations[0]
        arr_station = ner_stations[1]
    else:
        if found_stations:
            if len(found_stations) == 1:
                print(f'dep_station in found stations before:{dep_station}')
                print(f'arr_station in found stations before:{arr_station}')
                print(f'bot in found stations: {bot.departing_station_set}')
                if not dep_station and not bot.departing_station_set:
                    dep_station = found_stations[0]
                    print(
                        f'dep_station in found stations after:{dep_station}')
                
                elif not arr_station:
                    arr_station = found_stations[0]
                    print(
                        f'arr_station in found stations after:{arr_station}')
            if len(found_stations) > 1:
                if found_stations[0] == 'Manchester Oxford Road' and found_stations[1] == 'Oxford':
                    if not dep_station and not bot.departing_station_set:
                        dep_station = found_stations[0]
                    elif not arr_station:
                        arr_station = found_stations[0]
                else:
                    dep_station = found_stations[0]
                    arr_station = found_stations[1]
                
    


# Final fallback for dep_station and arr_station if neither were found
    if not dep_station and not arr_station:
         for ent in doc.ents:
              if ent.label_ in ['GPE', 'FAC', 'PERSON', 'ORG']:
                  print(f'dep_station in fallback:{dep_station}')
                  if not bot.departing_station_set:
                        dep_station = ent.text
                        print(f"Set dep_station from ent: {dep_station}")
                  else:
                        arr_station = ent.text
                        print(f"Set arr_station from ent: {arr_station}")

    # Process matches for date
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            parsed_date = safe_parse_date(ent.text)
            if not departure_date and not bot.departing_date_set:
                departure_date = parsed_date
                print(f"Set departure_date: {departure_date}")
            elif not returning_date:
                returning_date = parsed_date
                print(f"Set returning_date: {returning_date}")
        if ent.label_ == 'TIME':
            parsed_time = safe_parse_time(ent.text)
            if not departure_time and not bot.departing_time_set:
                departure_time = parsed_time
                print(f"Set departure_time: {departure_time}")
            elif not returning_time:
                returning_time = parsed_time
                print(f"Set returning_time: {returning_time}")
    # Process matches for time
    for match_id, start, end in matches_time:
        span = doc[start:end]
        if not departure_time and not bot.departing_time_set:
            departure_time = safe_parse_time(span.text)
        elif not returning_time:
            returning_time = safe_parse_time(span.text)


    result = [ticket_type, dep_station, arr_station, departure_time,
              departure_date, returning_time, returning_date, confirmed_journey, confirmed_journey_return, confirmed_book, confirmed_book_return]
    print(f"In the parsing function:{result}")

    return ticket_type, dep_station, arr_station, departure_time, departure_date, returning_time, returning_date, confirmed_journey, confirmed_journey_return, confirmed_book, confirmed_book_return


def find_station_names(text, station_list):
    found_stations = []
    for station in station_list:
        if re.search(r'\b' + re.escape(station) + r'\b', text, re.IGNORECASE):
            found_stations.append(station)
    return found_stations


def check_ticket(user_input):
    words = nltk.word_tokenize(user_input)
    threshold = 60
    single_keywords = ['one way', 'single','one-way','one way trip','single trip','single way']
    return_keywords = ['return', 'round','round trip','both ways']

    for word in words:
        for word_key in single_keywords:
            similarity_score = fuzz.ratio(word.lower(), word_key.lower())
            if similarity_score >= threshold:
                if word_key in single_keywords:
                    return 'one way'
        for word_key in return_keywords:
            similarity_score = fuzz.ratio(word.lower(), word_key.lower())
            if similarity_score >= threshold:
                if word_key in return_keywords:
                    return 'round'
            

    return None


def safe_parse_date(date_text):
    try:
        parsed_date = parse(date_text, fuzzy=True)
        return parsed_date.strftime('%d%m')
    except ValueError:
        return 'Invalid date format'


def safe_parse_time(time_text):
    # Normalize and clean up the input
    time_text = time_text.strip().lower()
    print(f"Attempting to parse time from input: '{time_text}'")

    # Define a list of expected time formats
    time_formats = [
        '%I:%M %p',  # '1:00 PM' or '1:00 AM'
        '%I:%M%p',   # '1:00PM' or '1:00AM'
        '%I %p',     # '1 PM' or '1 AM'
        '%I%p',      # '1PM' or '1AM'
        '%H:%M',     # '13:00' for 24-hour format
        '%H%M',      # '1300' for 24-hour without colon
    ]

    for fmt in time_formats:
        try:
            parsed_time = datetime.strptime(time_text, fmt)
            formatted_time = parsed_time.strftime('%H%M')
            print(f"Successfully parsed '{time_text}' as {formatted_time}")
            return formatted_time
        except ValueError:
            continue
    try:
        parsed_time = parse(time_text, fuzzy=True)
        formatted_time = parsed_time.strftime('%H%M')
        print(f"Fuzzy parsed '{time_text}' as {formatted_time}")
        return formatted_time
    except ValueError:
        print(f"Failed to parse time for '{time_text}'")
        return None


def book_ticket(user_input):
    print("User input:", user_input)
    ticket_type, dep_station, arr_station, departure_time, departure_date, returning_time, returning_date, confirmed_journey, confirmed_journey_return, confirmed_book, confirmed_book_return = parse_user_input_booking(
        user_input)
    print("Parsed:", ticket_type, dep_station, arr_station,
          departure_time, departure_date, returning_time, returning_date, confirmed_journey, confirmed_journey_return, confirmed_book, confirmed_book_return)

    # Update ticket type and control flags
    if ticket_type:
        bot.declare(Fact(ticket_type=ticket_type))
        bot.update_booking_type(ticket_type)  # Ensure flags are set correctly
    print(f"all_booking_info_single:{bot.all_booking_info_single}")
    print(f"all_booking_info:{bot.all_booking_info}")
    # Process booking based on type
    if bot.all_booking_info_single:
        handle_one_way_ticket(dep_station, arr_station,
                              departure_time, departure_date, confirmed_journey, confirmed_book)
        bot.all_booking_info_single = True
        bot.all_booking_info = False  # Set flag to true after processing
    elif bot.all_booking_info:
        handle_round_trip_ticket(dep_station, arr_station, departure_time,
                                 departure_date, returning_time, returning_date, confirmed_journey_return, confirmed_book_return)
        bot.all_booking_info = True
        bot.all_booking_info_single = False  # Set flag to true after processing

    bot.run()
    return bot.response


def handle_one_way_ticket(dep_station, arr_station, departure_time, departure_date, confirmed_journey, confirmed_book):
    current_date = datetime.now()
    # Fact declaration for one-way ticket
    if dep_station and not bot.departing_station_set:
        bot.declare(Fact(departing_station=dep_station))
        # bot.departing_station_set = True
    if arr_station:
        bot.declare(Fact(destination_station=arr_station))
    if departure_time and not bot.departing_time_set:
        bot.declare(Fact(departure_time=departure_time))

    if departure_date and not bot.departing_date_set and datetime.strptime(departure_date+'24', "%d%m%y") >= current_date:
        bot.declare(Fact(departure_date=departure_date))
    if confirmed_journey:
        print(f'confirmed_journey: {confirmed_journey}')
        if confirmed_journey.lower() == 'no':
            bot.reset_engine()
            bot.reset()
        else:
            bot.declare(Fact(confirmed_journey=confirmed_journey))
    if confirmed_book:
        bot.declare(Fact(confirmed_book=confirmed_book))


def handle_round_trip_ticket(dep_station, arr_station, departure_time, departure_date, returning_time, returning_date, confirmed_journey_return, confirmed_book_return):
    current_date = datetime.now()
    if dep_station and not bot.departing_station_set:
        bot.declare(Fact(departing_station=dep_station))
        # bot.departing_station_set = True
    if arr_station:
        bot.declare(Fact(destination_station=arr_station))
    if departure_time and not bot.departing_time_set:
        bot.declare(Fact(departure_time=departure_time))
    if returning_time:
        bot.declare(Fact(returning_time=returning_time))
    if departure_date and not bot.departing_date_set and datetime.strptime(departure_date+'24','%d%m%y') >= current_date:
        bot.declare(Fact(departure_date=departure_date))
    
    
    if returning_date and datetime.strptime(returning_date+'24', '%d%m%y') >= current_date:
        bot.declare(Fact(returning_date=returning_date))
    
    if confirmed_journey_return:
        if confirmed_journey_return.lower() == 'no':
            bot.reset_engine()
            bot.reset()
        else:
            bot.declare(Fact(confirmed_journey_return=confirmed_journey_return))
    
    if confirmed_book_return:
        bot.declare(Fact(confirmed_book_return=confirmed_book_return))



