# import nltk
from fuzzywuzzy import fuzz

# # text = "I want to know about the blokcage between London and Norwich"
# text = "I want to know the contingency plan when the warther is frost"

# words = nltk.word_tokenize(text)

# acceptable_words = ['blockage', 'weather']

# threshold = 80

# for word in words:
#     for acceptable_word in acceptable_words:
#         similarity_score = fuzz.ratio(word.lower(), acceptable_word.lower())
#         if similarity_score >= threshold:
#             print(f"word: {acceptable_word}")
#             break

from fuzzywuzzy import process, fuzz
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy
import nltk

nlp = spacy.load("en_core_web_md")


def parse_user_input_advise(user_input):
    doc = nlp(user_input)
    words = nltk.word_tokenize(user_input)
    threshold = 60
    
    event_type = None
    weather = None
    bl_location_a = None
    bl_location_b = None
    severity = None

    word_keys = ['blockage', 'weather', 'full', 'partial', 'autumn arrangements and low adhesion', 'flooding', 'frost', 'high temperatures', 'high tides', 'high winds', 'snow']
    event_keys = ['blockage', 'weather']
    severity_keys = ['full', 'partial']

    for word in words:
        for word_key in word_keys:
            similarity_score = fuzz.ratio(word.lower(), word_key.lower())
            if similarity_score >= threshold:
                if word_key in event_keys:
                    event_type = word_key
                elif word_key in severity_keys:
                    severity = word_key

    if extract_weather_phrases(user_input):
        weather = extract_weather_phrases(user_input)
        event_type = 'weather'

    return event_type, weather, bl_location_a, bl_location_b, severity

def extract_weather_phrases(sentence):
    weather_mapping = ['autumn arrangements and low adhesion', 'flooding', 'frost', 'high temperatures', 'high tides',
                       'high winds', 'snow']
    
    best_match = None
    max_score = 0
    
    # Combine all tokens in the sentence into a single string
    combined_tokens = " ".join(word_tokenize(sentence))
    
    # Use fuzzy matching to find the best match for the combined tokens in the weather mapping
    for weather_phrase in weather_mapping:
        score = process.extractOne(combined_tokens.lower(), [weather_phrase.lower()])[1]
        
        # If the fuzzy match score is above a certain threshold and greater than previous matches, consider it as the best match
        if score >= 50 and score > max_score:
            best_match = weather_phrase
            max_score = score
    
    return best_match

user_input = "I'm concerned about flooding and it is very wet."

event_type, weather, bl_location_a, bl_location_b, severity = parse_user_input_advise(user_input)

print(f'type: {event_type}\n weather: {weather}') 