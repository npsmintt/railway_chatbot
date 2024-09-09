import spacy
from experta import *
from datetime import datetime
from models.prediction import Predictions
from models.user_input_parsing import *
from models import chat
from difflib import SequenceMatcher
import re
from dateutil.parser import parse

nlp = spacy.load("en_core_web_md")


class PredictionBot(KnowledgeEngine):
    def __init__(self):
        super().__init__()

        self.all_delay_info = None
        self.response = None
        self.current_station_set = False

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="predict delay")

    @Rule(Fact(action='predict delay'),
          NOT(Fact(current_station=W())))
    def ask_current_station(self):
        image_url = '../static/images/map.jpeg'
        self.response = f'Can you tell me which station you are currently at? (Please note that the current station CANNOT be Norwich because it is the destination of the line.)<br><img src="{image_url}" class="delay_img" alt="Train Stations">'

    @Rule(Fact(action='predict delay'),
          NOT(Fact(destination=W())),
          Fact(current_station=MATCH.current_station))
    def ask_destination(self, current_station):
        image_url = '../static/images/map.jpeg'
        self.response = f'You are currently at {current_station}. Where are you going to? (Please note that the destination station CANNOT be London because it is the departure station of the line.)<br><img src="{image_url}" class="delay_img" alt="Train Stations">'
        self.current_station_set = True

    @Rule(Fact(action='predict delay'),
          NOT(Fact(expected_departure=W())),
          Fact(current_station=MATCH.current_station),
          Fact(destination=MATCH.destination))
    def ask_exp_dep(self, current_station, destination):
        self.response = f'You are traveling from {current_station} to {destination}. When is the train expected to depart?(For example: \'10:20 am\', \'1 pm\')'

    @Rule(Fact(action='predict delay'),
          NOT(Fact(delay=W())),
          Fact(current_station=MATCH.current_station),
          Fact(destination=MATCH.destination),
          Fact(expected_departure=MATCH.expected_departure))
    def ask_delay(self, current_station, destination, expected_departure):
        self.response = f'Your train is expected to depart from {current_station} to {destination} at {expected_departure}. How many minutes has your train been delayed?'
    
    @Rule(Fact(action='predict delay'),
          Fact(delay=MATCH.delay),
          Fact(current_station=MATCH.current_station),
          Fact(destination=MATCH.destination),
          Fact(expected_departure=MATCH.expected_departure),
          NOT(Fact(confirmed_info=W())))
    def confirmed_info(self, current_station, destination, expected_departure, delay):
        self.response = f'Your train is expected to depart from {current_station} to {destination} at {expected_departure}, and it has {delay} minutes delay. Is that correct?'
    
    @Rule(Fact(action='predict delay'),
          Fact(delay=MATCH.delay),
          Fact(current_station=MATCH.current_station),
          Fact(destination=MATCH.destination),
          Fact(expected_departure=MATCH.expected_departure),
          Fact(confirmed_info=MATCH.confirmed_info),
          NOT(Fact(confirmed_prediction=W())))
    def confirmed_prediction(self):
        self.response = f'We got all the information needed for the total delay prediction, and it may take some time to finish the prediction. Enter \'OK\' to continue.'
    @Rule(Fact(action='predict delay'),
          Fact(current_station=MATCH.current_station),
          Fact(destination=MATCH.destination),
          Fact(expected_departure=MATCH.expected_departure),
          Fact(delay=MATCH.delay),
          Fact(confirmed_info=MATCH.confirmed_info),
          Fact(confirmed_prediction=MATCH.confirmed_prediction))
    def all_delay_info_complete(self, current_station, destination, expected_departure, delay):
        delay_info = {'current_station': current_station,
                      'destination': destination,
                      'expected_departure': expected_departure,
                      'delay': delay}
        print(f"all_delay_info: {delay_info}")
        if None not in delay_info.values():
            expected_departure = parse_time(expected_departure)
            pr = Predictions()
            result = pr.display_results(
                current_station, destination, expected_departure, delay)
            self.response = result
            chat.session = 'default'
            self.current_station_set = False
            self.reset()

        else:
            self.response = 'Some information is missing. Please provide all required details.'


station_list = [
    "norwich", "diss", "stowmarket", "ipswich", "manningtree", "colchester",
    "witham", "chelmsford", "ingatestone", "shenfield", "stratford",
    "stratford-le-hope", "london liverpool street", "london liverpool st",
    "liverpool street", "london"
]


def get_closest_station_name(input_text, stations):
    """Returns the closest station name from a list of stations using fuzzy matching."""
    closest_station = None
    highest_ratio = 0
    for station in stations:
        ratio = SequenceMatcher(None, input_text.lower(),
                                station.lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            closest_station = station
    # Threshold for considering a close match
    return closest_station if highest_ratio > 0.6 else None


def find_stations_in_sentence(sentence, station_list):
    """Extract and validate station names from a sentence."""
    words = sentence.split()
    found_stations = []

    for word in words:
        if word.lower() in station_list:
            found_stations.append(word.lower())
        else:
            closest_station = get_closest_station_name(word, station_list)
            if closest_station:
                found_stations.append(closest_station.lower())

    return found_stations


def assign_stations(found_stations):
    """Assign departure and destination stations from found stations."""
    if len(found_stations) >= 2:
        departure = found_stations[0]
        destination = found_stations[1]
        return departure, destination
    elif len(found_stations) == 1:
        return found_stations[0], None
    else:
        return None, None


def parse_user_input_delay(user_input):
    doc = nlp(user_input)
    current_station = None
    destination = None
    expected_departure = None
    delay = None
    confirmed_info = None
    confirmed_prediction = None
    
    if user_input.lower().strip() in ['yeh','yep','ye','yes','yup','yeah','no','nope','nah']:
        confirmed_info = user_input
    elif user_input.lower().strip() == 'ok':
        confirmed_prediction = user_input
    elif user_input.lower().strip() == 'bye':
        chat.session = 'default'
        bot.current_station_set = False
        bot.reset()
        

    found_stations = find_stations_in_sentence(user_input, station_list)
    print(f"Stations found: {found_stations}")
    if len(found_stations) == 2:
        current_station, destination = assign_stations(found_stations)
    elif len(found_stations) == 1:
        if not current_station and not bot.current_station_set:
            current_station = found_stations[0]
        elif not destination:
            destination = found_stations[0]
    elif len(found_stations) > 2:
        current_station = found_stations[0]
        destination = found_stations[1]

    delay = extract_delay(user_input)
    expected_departure = extract_expected_departure(user_input)

    # for ent in doc.ents:
    #     if ent.label_ == 'TIME':
    #         expected_departure = parse_time(ent.text)
    # elif ent.label_ == 'CARDINAL':
    #     match = re.search(r'\d+', ent.text)
    #     if match:
    #         delay = int(match.group())

    result = current_station, destination, expected_departure, delay, confirmed_info, confirmed_prediction
    print(f"In the parsing function: {result}")

    return current_station, destination, expected_departure, delay, confirmed_info, confirmed_prediction


def extract_delay(sentence):
    doc = nlp(sentence)
    delay = None

    for ent in doc.ents:
        if ent.label_ == 'CARDINAL':
            match = re.search(r'\d+', ent.text)
            if match:
                delay = int(match.group())
    return delay


# def is_valid_time_format(time_str):
#     """Check if the given time string is in a valid time format (e.g., 10:00, 14:30)."""
#     # A regex pattern to match times like 10:00, 10:00 AM, 14:30
#     pattern = re.compile(r'^\d{1,2}(?::\d{2})?\s?(AM|PM|am|pm)?$')
#     return bool(pattern.match(time_str))


def extract_expected_departure(sentence):
    doc = nlp(sentence)
    expected_departure = None

    for ent in doc.ents:
        if ent.label_ == 'TIME':
            expected_departure = parse_time(ent.text)
            break

    return expected_departure


bot = PredictionBot()
bot.reset()


def predict_delay(user_input):
    print(user_input)
    print(f"all_delay_info in predict_delay: {bot.all_delay_info}")
    if not bot.all_delay_info:
        current_station, destination, expected_departure, delay, confirmed_info, confirmed_prediction = parse_user_input_delay(
            user_input)
        print(
            f"in predict_delay: {current_station, destination, expected_departure, delay}")
        if current_station and not bot.current_station_set:
            bot.declare(Fact(current_station=current_station))
        if destination:
            bot.declare(Fact(destination=destination))
        if expected_departure:
            bot.declare(Fact(expected_departure=expected_departure))
        if delay:
            bot.declare(Fact(delay=delay))
        if confirmed_info:
            if confirmed_info.lower() in ['no', 'nope', 'nah']:
                bot.all_delay_info = None
                bot.response = None
                bot.current_station_set = False
                bot.reset()
            else:
                bot.declare(Fact(confirmed_info=confirmed_info))
        if confirmed_prediction:
            bot.declare(Fact(confirmed_prediction=confirmed_prediction))

    bot.run()
    return bot.response


def parse_time(time_text):
    time_text = time_text.strip().lower()
    print(f"Attempting to parse time from input: '{time_text}'")

    time_formats = [
        '%I:%M %p', '%I:%M%p', '%I %p', '%I%p', '%H:%M', '%H%M',
    ]

    for fmt in time_formats:
        try:
            parsed_time = datetime.strptime(time_text, fmt)
            formatted_time = parsed_time.strftime('%H:%M')
            print(f"Successfully parsed '{time_text}' as {formatted_time}")
            return formatted_time
        except ValueError:
            continue
    try:
        parsed_time = parse(time_text, fuzzy=True)
        formatted_time = parsed_time.strftime('%H:%M')
        print(f"Fuzzy parsed '{time_text}' as {formatted_time}")
        return formatted_time
    except ValueError:
        print(f"Failed to parse time for '{time_text}'")
        return None
