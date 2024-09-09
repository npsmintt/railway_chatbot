from experta import *
import mysql.connector
import re
from models import chat

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="234236238",
    database="chatbot_contingency"
)

cursor = db_connection.cursor()

# class addBot(KnowledgeEngine):
#     def __init__(self):
#         super().__init__()
#         self.contingency = None
#         self.plan = None
#         self.contingency_set = False
#         self.contingency_asked = False
#
#     @DefFacts()
#     def _initial_action(self):
#         yield Fact(action="add")
#
#     @Rule(Fact(action='add'),
#           NOT(Fact(contingency=W())))
#     def ask_contingency(self):
#         self.response = 'Sure! What contingency is the plan for?'
#
#     @Rule(Fact(action='add'),
#           NOT(Fact(plan=W())),
#           Fact(contingency=MATCH.contingency))
#     def ask_plan(self, contingency):
#         # self.response = f'Ok. Can you tell me the contingency plan for {contingency}?'
#         # self.contingency_asked = True
#         # first, check the database to see if there is already a plan for the contingency
#         cursor.execute("SELECT plan FROM other_contingency_plan WHERE contingency = %s", (contingency,))
#         result = cursor.fetchone()
#         if result:
#             self.response = f"A contingency plan for '{contingency}' already exists. Would you like to update it?"
#         else:
#             self.response = f"Ok. Can you tell me the contingency plan for '{contingency}'?"
#         self.contingency_asked = True
#
#     @Rule(Fact(action='add'),
#           Fact(contingency=MATCH.contingency),
#           Fact(plan=MATCH.plan))
#     def all_info_gathered(self, contingency, plan):
#         print(f"all info has been gathered. contingency is {contingency}, plan is {plan}")
#         try:
#             cursor.execute("INSERT INTO other_contingency_plan (contingency, plan) VALUES (%s, %s)",
#                            (contingency, plan))
#             db_connection.commit()
#             self.response = f"Thank you! The contingency plan for {contingency} has been successfully added to the database."
#             self.reset()
#         except mysql.connector.Error as err:
#             self.response = f" There was an error adding the plan to the database: {err}"
#             db_connection.rollback()
#             self.reset()
#
# add_bot = addBot()
# add_bot.reset()
#
# def parse_contingency(user_input):
#     # different patterns for contingency plan in user input
#     match = re.search(r"'([^']+)'", user_input)
#     if match:
#         return match.group(1)
#
#     match = re.search(r"contingency plan for ([\w\s]+)", user_input, re.IGNORECASE)
#     if match:
#         return match.group(1)
#
#     match = re.search(r"contingency is ([\w\s]+)", user_input, re.IGNORECASE)
#     if match:
#         return match.group(1)
#
#     return None
#
# def add_contingency_plan(msg):
#     contingency = parse_contingency(msg)
#     print(contingency)
#     if contingency is not None:
#         add_bot.declare(Fact(contingency=contingency))
#         add_bot.contingency_set = True
#     elif contingency is None and add_bot.contingency_set is False and add_bot.contingency_asked is True:
#         add_bot.declare(Fact(contingency=msg))
#         add_bot.contingency_set = True
#
#     elif add_bot.contingency_set is True:
#         print("The contingency")
#         add_bot.declare(Fact(plan=msg))
#
#     add_bot.run()
#     print(f'bot response: {add_bot.response}')
#     return add_bot.response
#

class addBot(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.contingency = None
        self.plan = None
        self.contingency_set = False
        self.contingency_asked = False
        self.update_asked = False
        self.update_confirmed = False

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="add")

    @Rule(Fact(action='add'),
          NOT(Fact(contingency=W())))
    def ask_contingency(self):
        self.response = 'Sure! What contingency is the plan for?'
        self.contingency_asked = True

    @Rule(Fact(action='add'),
          NOT(Fact(plan=W())),
          Fact(contingency=MATCH.contingency))
    def ask_plan(self, contingency):
        cursor.execute("SELECT plan FROM other_contingency_plan WHERE contingency = %s", (contingency,))
        result = cursor.fetchone()
        if result:
            self.response = f"A contingency plan for '{contingency}' already exists. Would you like to update it?"
            self.update_asked = True
        else:
            self.response = f"Ok. Can you tell me the contingency plan for '{contingency}'?"
            self.contingency_asked = True

    @Rule(Fact(action='add'),
          Fact(contingency=MATCH.contingency),
          Fact(plan=MATCH.plan))
    # only execute this if update plan is false
    def all_info_gathered(self, contingency, plan):
        print(f"all info has been gathered. contingency is {contingency}, plan is {plan}")
        try:
            cursor.execute("INSERT INTO other_contingency_plan (contingency, plan) VALUES (%s, %s)",
                           (contingency, plan))
            db_connection.commit()
            self.response = f"Thank you! The contingency plan for {contingency} has been successfully added to the database."
            self.contingency = None
            self.plan = None
            self.contingency_set = False
            self.contingency_asked = False
            self.update_asked = False
            self.update_confirmed = False
            chat.session = 'default'
            self.reset()
        except mysql.connector.Error as err:
            self.response = f" There was an error adding the plan to the database: {err}"
            db_connection.rollback()
            self.contingency = None
            self.plan = None
            self.contingency_set = False
            self.contingency_asked = False
            self.update_asked = False
            self.update_confirmed = False
            chat.session = 'default'
            self.reset()

    @Rule(Fact(action='add'),
          Fact(contingency=MATCH.contingency),
          Fact(update_confirmed='yes'),
          NOT(Fact(plan_to_update=W())))
    def update_plan(self, contingency):
        self.response = f"Great! What is the updated contingency plan for '{contingency}'?"
        self.update_confirmed = True
        self.contingency_asked = True

    @Rule(Fact(action='add'),
          Fact(contingency=MATCH.contingency),
          Fact(update_confirmed='no'))
    def no_update(self, contingency):
        self.response = f"Ok, the existing plan for '{contingency}' will not be updated."
        self.contingency = None
        self.plan = None
        self.contingency_set = False
        self.contingency_asked = False
        self.update_asked = False
        self.update_confirmed = False
        chat.session = 'default'
        self.reset()

    @Rule(Fact(action='add'),
          Fact(contingency=MATCH.contingency),
          Fact(update_confirmed='yes'),
          Fact(plan_to_update=MATCH.plan_to_update))
    def update_existing_plan(self, contingency, plan_to_update):
        print(f"Updating existing plan for {contingency} with new plan: {plan_to_update}")
        try:
            cursor.execute("UPDATE other_contingency_plan SET plan = %s WHERE contingency = %s", (plan_to_update, contingency))
            db_connection.commit()
            self.response = f"The contingency plan for '{contingency}' has been successfully updated."
            self.contingency = None
            self.plan = None
            self.contingency_set = False
            self.contingency_asked = False
            self.update_asked = False
            self.update_confirmed = False
            chat.session = 'default'
            self.reset()
        except mysql.connector.Error as err:
            self.response = f" There was an error updating the plan in the database: {err}"
            db_connection.rollback()
            self.contingency = None
            self.plan = None
            self.contingency_set = False
            self.contingency_asked = False
            self.update_asked = False
            self.update_confirmed = False
            chat.session = 'default'
            self.reset()

add_bot = addBot()
add_bot.reset()

def parse_contingency(user_input):
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

    return None

def add_contingency_plan(msg):

    if 'quit' in msg or 'bye' in msg:
        chat.session = 'default'
        add_bot.reset()
        add_bot.contingency = None
        add_bot.plan = None
        add_bot.contingency_set = False
        add_bot.contingency_asked = False
        add_bot.update_asked = False
        add_bot.update_confirmed = False


    contingency = parse_contingency(msg)
    print(contingency)
    if contingency is not None:
        add_bot.declare(Fact(contingency=contingency))
        add_bot.contingency_set = True
    elif contingency is None and add_bot.contingency_set is False and add_bot.contingency_asked is True:
        add_bot.declare(Fact(contingency=msg))
        add_bot.contingency_set = True
    elif add_bot.contingency_set is True and not add_bot.update_asked:
        add_bot.declare(Fact(plan=msg))
    elif add_bot.update_asked:
        if 'yes' in msg.lower():
            add_bot.declare(Fact(update_confirmed='yes'))
        elif 'no' in msg.lower():
            add_bot.declare(Fact(update_confirmed='no'))
    if add_bot.update_confirmed is True:
        add_bot.declare(Fact(plan_to_update=msg))
    add_bot.run()

    print(f'bot response: {add_bot.response}')
    print(f'contingency set: {add_bot.contingency_set},'
          f'contingency asked: {add_bot.contingency_asked},'
          f'update asked: {add_bot.update_asked}'
          f'update confirmed: {add_bot.update_confirmed}')
    return add_bot.response
