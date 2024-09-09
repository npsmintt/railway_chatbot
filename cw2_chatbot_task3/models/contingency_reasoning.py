import spacy
import re
import json
import nltk
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz, process
from experta import *
import mysql.connector
from models import chat

nlp = spacy.load("en_core_web_md")

# connect to MySQL database
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="234236238",
    database="chatbot_contingency"
)

cursor = db_connection.cursor()

class adviseBot(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        # initialize the variable for contingency plan
        self.all_contingency_info = None
        self.event_type = None
        self.bl_location_a = None
        self.bl_location_b = None
        self.severity = None
        self.bl_location_b_set = False

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="advise")

    @Rule(Fact(action='advise'),
          NOT(Fact(event_type=W())))
    def ask_event_type(self):
        self.response = 'Ok. What contingency are you currently experiencing?'

    @Rule(Fact(action='advise'),
          NOT(Fact(weather=W())),
          Fact(event_type='weather'), # Rule if the event type is about weather
          Fact(event_type=MATCH.event_type))
    def ask_weather(self, event_type):
        self.response = f'You are currently experiencing {event_type}. What is the weather like?'

    @Rule(Fact(action='advise'),
          NOT(Fact(bl_location_a=W())),
          Fact(event_type='blockage'), # Rule if the event type is about blockage
          Fact(event_type=MATCH.event_type))
    def ask_destination(self, event_type):
        self.response = f'You are currently facing {event_type}. Can you specify where is the {event_type} happening?'

    @Rule(Fact(action='advise'),
          NOT(Fact(bl_location_b=W())),
          Fact(event_type='blockage'),
          Fact(event_type=MATCH.event_type),
          Fact(bl_location_a=MATCH.bl_location_a))
    def ask_exp_dep(self, event_type, bl_location_a):
        self.response = f'You are currently facing {event_type} at {bl_location_a}. Can you specify another station that affected by the blockage?'

    @Rule(Fact(action='advise'),
          NOT(Fact(severity=W())),
          Fact(event_type='blockage'),
          Fact(event_type=MATCH.event_type),
          Fact(bl_location_a=MATCH.bl_location_a),
          Fact(bl_location_b=MATCH.bl_location_b))
    def ask_severity(self, event_type, bl_location_a, bl_location_b):
        self.response = f'You are currently facing {event_type} between {bl_location_a} and {bl_location_b}. Is it a full or partial blockage?'

    # When blockage data is completed
    @Rule(Fact(action='advise'),
          Fact(event_type='blockage'),
          Fact(event_type=MATCH.event_type),
          Fact(bl_location_a=MATCH.bl_location_a),
          Fact(bl_location_b=MATCH.bl_location_b),
          Fact(severity=MATCH.severity)) 
    def all_data_complete(self, event_type, bl_location_a, bl_location_b, severity):
        contingency_info = {'event_type': event_type,
                            'bl_location_a': bl_location_a,
                            'bl_location_b': bl_location_b,
                            'severity': severity}
        if None not in contingency_info.values(): 
            cursor.execute("SELECT controller_instructions, resource_required, infrastructure, staff_deployment, alternative_transport ,customer_message ,internal_message, electronic_information FROM blockage_contingency_plan WHERE severity = %s AND location_a = %s AND location_b = %s", (severity, bl_location_a, bl_location_b))
            data_row = cursor.fetchall()
            if data_row:
                data_dict = [{'Controller Instructions': row[0],
                            'Resource Required': row[1],
                            'Infrastructure': row[2],
                            'Staff Deployment': row[3],
                            'Alternative Transport': row[4],
                            'Customer Message': row[5],
                            'Internal Message': row[6],
                            'Electronic Information': row[7]} for row in data_row]
                data_json = json.dumps(data_dict)
                chat.session = 'default'
                chat.response_dict["data_type"] = 'json'
                chat.response_dict["data_content"] = data_json
                self.response = f'Got it! Here is the contingency plan for {severity} line block between {bl_location_a} and {bl_location_b}'
                # reset all variables and rules
                self.reset()
                self.all_contingency_info = None
                self.event_type = None
                self.bl_location_a = None
                self.bl_location_b = None
                self.bl_location_b_set = False
                self.severity = None
            else:
                chat.session = 'default'
                chat.response_dict["data_type"] = ""
                chat.response_dict["data_content"] = ""
                self.response = f'Sorry, I cannot find a contingency plan for {severity} line block between {bl_location_a} and {bl_location_b}'
                self.reset()
                self.all_contingency_info = None
                self.event_type = None
                self.bl_location_a = None
                self.bl_location_b = None
                self.severity = None
                self.bl_location_b_set = False

    # When weather data is completed
    @Rule(Fact(action='advise'),
            Fact(event_type='weather'),
            Fact(event_type=MATCH.event_type),
            Fact(weather=MATCH.weather))
    def all_weather_complete(self, event_type, weather):
        weather_info = {'event_type': event_type,
                            'weather': weather}
        if None not in weather_info.values(): 
            cursor.execute("SELECT plan FROM weather_contingency_plan WHERE weather = %s", ([weather]))
            data_row = cursor.fetchall()
            if data_row:
                weather_plan = data_row[0][0]
                chat.session = 'default'
                chat.response_dict["data_type"] = 'list'
                chat.response_dict["data_content"] = weather_plan
                self.response = f'Got it! Here is the contingency plan for {weather}:'
                self.reset()
                self.all_contingency_info = None
                self.event_type = None
                self.bl_location_a = None
                self.bl_location_b = None
                self.severity = None
                self.bl_location_b_set = False
            else:
                chat.session = 'default'
                chat.response_dict["data_type"] = ""
                chat.response_dict["data_content"] = ""
                self.response = f'Sorry, I cannot find a contingency plan for {weather}'
                self.reset()
                self.all_contingency_info = None
                self.event_type = None
                self.bl_location_a = None
                self.bl_location_b = None
                self.severity = None
                self.bl_location_b_set = False

    # experta rules for getting contingency from acquired knowledge
    @Rule(Fact(action='advise'),
          NOT(Fact(event_type=W())),
          Fact(other_contingency=MATCH.other_contingency))
    def get_other_contingency_plan(self, other_contingency):
        # reconnect database connection to access updated data in the same session
        db_connection1 = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="234236238",
            database="chatbot_contingency"
        )
        cursor1 = db_connection1.cursor()
        cursor1.execute("SELECT plan FROM other_contingency_plan WHERE contingency = %s", ([other_contingency]))
        data_row = cursor1.fetchall()
        if data_row:
            other_plan = data_row[0][0]
            chat.session = 'default'
            self.response = f'Got it! Here is the contingency plan for {other_contingency}:'
            chat.response_dict["data_type"] = 'list'
            chat.response_dict["data_content"] = other_plan
            self.reset()
            self.all_contingency_info = None
            self.event_type = None
            self.bl_location_a = None
            self.bl_location_b = None
            self.severity = None
            self.bl_location_b_set = False
        else:
            chat.session = 'default'
            self.response = f'Sorry, I cannot find a contingency plan for {other_contingency}'
            self.reset()
            self.all_contingency_info = None
            self.event_type = None
            self.bl_location_a = None
            self.bl_location_b = None
            self.severity = None
            self.bl_location_b_set = False
    
bot = adviseBot()
bot.reset()

# parsing input function
def parse_user_input_advise(user_input):
    doc = nlp(user_input)
    words = nltk.word_tokenize(user_input)
    threshold = 85
    
    event_type = None
    weather = None
    bl_location_a = None
    bl_location_b = None
    severity = None
    other_contingency = None

    word_keys = ['blockage', 'weather', 'full', 'partial', 'autumn arrangements and low adhesion', 'flooding', 'frost', 'high temperatures', 'high tides', 'high winds', 'snow']
    event_keys = ['blockage', 'weather']
    severity_keys = ['full', 'partial']
    weather_keys = ['autumn arrangements and low adhesion', 'flooding', 'frost', 'high temperatures', 'high tides', 'high winds', 'snow']

    if 'quit' in user_input or 'bye' in user_input:
        chat.session = 'default'
        bot.reset()
        bot.all_contingency_info = None
        bot.event_type = None
        bot.bl_location_a = None
        bot.bl_location_b = None
        bot.severity = None
        bot.bl_location_b_set = False

    for word in words:
        for word_key in word_keys:
            similarity_score = fuzz.ratio(word.lower(), word_key.lower())
            if similarity_score >= threshold:
                if word_key in event_keys:
                    event_type = word_key
                elif word_key in severity_keys:
                    severity = word_key

    if extract_weather_phrases(user_input) in weather_keys:
        weather = extract_weather_phrases(user_input)
        event_type = 'weather'

    for ent in doc.ents:
        if ent.label_ in ['GPE', 'FAC', 'PERSON', 'ORG']:
            if bl_location_a is None and not bot.bl_location_b_set:
                bl_location_a = ent.text.title()
            elif bl_location_b is None:
                bl_location_b = ent.text.title()

    if event_type is None:
        other_contingency = parse_other_contingency(user_input)

    return event_type, weather, bl_location_a, bl_location_b, severity, other_contingency

def extract_weather_phrases(sentence):
    weather_mapping = ['autumn arrangements and low adhesion', 'flooding', 'frost', 'temperatures', 'tide',
                       'wind', 'snow']
    best_match = None
    # max_score = 0
    combined_tokens = " ".join(word_tokenize(sentence))
    for weather_phrase in weather_mapping:
        score = process.extractOne(combined_tokens.lower(), [weather_phrase.lower()])[1]
        
        # if score >= 50 and score > max_score:
        if score >= 60:
            if weather_phrase == 'temperatures':
                best_match = 'high temperatures'
            elif weather_phrase == 'wind':
                best_match = 'high winds'
            elif weather_phrase == 'tide':
                best_match = 'high tides'
            else:
                best_match = weather_phrase
            # max_score = score
    return best_match

def give_advice(user_input):
    if not bot.all_contingency_info:
        event_type, weather, bl_location_a, bl_location_b, severity, other_contingency = parse_user_input_advise(user_input)

        if event_type is not None:
            bot.declare(Fact(event_type=event_type))
        if weather is not None:
            bot.declare(Fact(weather=weather))
        if bl_location_a is not None and not bot.bl_location_b_set:
            bot.declare(Fact(bl_location_a=bl_location_a))
            bot.bl_location_b_set = True
        if bl_location_b is not None and bot.bl_location_b_set:
            bot.declare(Fact(bl_location_b=bl_location_b))
        if severity is not None:
            bot.declare(Fact(severity=severity))
        elif event_type is None and other_contingency is not None:
            bot.declare(Fact(other_contingency=other_contingency))

        bot.run()
        print(f'bot response = {bot.response}')
        return bot.response
    return bot.all_contingency_info

def parse_other_contingency(user_input):
    # match different patterns in user input for contingency
    match = re.search(r"'([^']+)'", user_input)
    if match:
        return match.group(1)

    match = re.search(r"contingency plan for ([\w\s]+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r"contingency is ([\w\s]+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r"contingency I am facing is ([\w\s]+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1)

    return None