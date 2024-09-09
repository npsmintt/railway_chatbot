
from difflib import SequenceMatcher
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


class Predictions:
    def __init__(self):
        self.stations = {
            "norwich": "NRCH",
            "diss": "DISS",
            "stowmarket": "STWMRKT",
            "ipswich": "IPSWICH",
            "manningtree": "MANNGTR",
            "colchester": "CLCHSTR",
            "witham": "WITHAME",
            "chelmsford": "CHLMSFD",
            "ingatestone": "INT",
            "shenfield": "SHENFLD",
            "stratford": "STFD",
            "stratford-le-hope": "STFD",
            "london liverpool street": "LIVST",
            "london liverpool st": "LIVST",
            "liverpool street": "LIVST",
            "london": "LIVST"
        }
        # morning: 5 - 10, midday: 10-15, evening: 15 - 20, night: 20 - 5
        self.segment_of_day = None
        self.rush_hour = None  # (06 - 09 and 16:00-:18:00) = 1
        self.day_of_week = datetime.today().weekday()
        print(f'day of week: {self.day_of_week}')  # 0 = Mon and 6 = Sun
        self.weekend = self.is_weekend(
            self.day_of_week)  # Monday - Friday = 1; Saturday and Sunday = 0
        self.departure_station = None
        self.arrival_station = None
        self.exp_dep = None
        self.delay = None



    def station_finder(self, station):
        print("Received station>>62>>", station)
        x = station.lower()
        print(f'x:{x}')
        similar = ''
        if x in self.stations:
            return self.stations[x]
        else:
            for s in self.stations:
                ratio = SequenceMatcher(None, x, s).ratio() * 100
                if ratio >= 60:  # Need to check what value is acceptable
                    similar = s
                    print("The city you've provided has not been found. "
                          "Closest match to " + station + "  is: " + s.upper())
            if similar == '':
                raise Exception("No similar cities to " + station + " have "
                                "been found. Please type again the station")
            print(f"similar: {similar}")
            return similar

    def get_data(self):

        df = pd.read_csv('/Users/thisgirlcan/Desktop/railway_chatBot/cw2_chatbot_task1_task2/data_task_2.csv',
                         dtype={'ptd': str, 'dep_at': str, 'pta': str, 'arr_at': str})

        df['ptd'] = df['ptd'].fillna('00:00')
        df['dep_at'] = df['dep_at'].fillna('00:00')
        df['pta'] = df['pta'].fillna('00:00')
        df['arr_at'] = df['arr_at'].fillna('00:00')

        # Filter DataFrame to include rows where 'tpl' matches departure_station or arrival_station
        departures = df[df['tpl'] == self.departure_station]
        arrivals = df[df['tpl'] == self.arrival_station]

        # Merge departures and arrivals DataFrames on 'rid' to get journey information
        result = pd.merge(departures, arrivals, left_on='rid',
                          right_on='rid', suffixes=('_FROM', '_TO'))

        # Select required columns and order by 'rid_FROM'
        result = result[['rid', 'tpl_FROM', 'ptd_FROM', 'dep_at_FROM',
                        'tpl_TO', 'pta_TO', 'arr_at_TO']].sort_values(by='rid')

        print(f"result length: {len(result)}")
        result_list = result.to_records(index=False).tolist()
        print(f"first result entry: {result_list[0]}")

        return result_list

    @staticmethod
    def convert_time(time):
        """
        Convert given time (in seconds) to hours, minutes, seconds
        """
        tt = []
        hh = int(time[0][0] / 3600)
        tt.append(hh)
        time[0][0] = time[0][0] - (hh * 3600)
        mm = int(time[0][0] / 60)
        tt.append(mm)
        time[0][0] = time[0][0] - (mm * 60)
        ss = int(time[0][0] % 60)
        tt.append(ss)

        return tt

    @staticmethod
    def is_weekend(day):
        weekend = None
        if day <= 4:
            weekend = 0
        elif 4 < day < 7:
            weekend = 1
        return weekend

    @staticmethod
    def check_day_segment(hour_of_day):
        segment_of_day = None
        if 5 <= hour_of_day < 10:
            segment_of_day = 1
        elif 10 <= hour_of_day < 15:
            segment_of_day = 2
        elif 15 <= hour_of_day < 20:
            segment_of_day = 3
        elif (20 <= hour_of_day < 24) or (0 <= hour_of_day < 5):
            segment_of_day = 4
        return segment_of_day

    @staticmethod
    def is_rush_hour(hour, minute):
        rush_hour = []

        if (5 <= hour <= 9) or (16 <= hour <= 18):
            if (hour == 5 and 45 <= minute < 60) or (5 < hour < 9):
                rush_hour = 1
            elif (hour == 5 and minute < 45) or (hour == 9 and 0 < minute):
                rush_hour = 0
            elif 16 <= hour or (hour <= 18 and minute == 0):
                rush_hour = 1
        elif (9 < hour < 16) or (hour == 9 and 0 < minute < 60) or (
                18 < hour < 24) or (0 < hour < 5):
            rush_hour = 0

        return rush_hour

    def prepare_datasets(self):
        result = self.get_data()
        data = []

        for journey in range(len(result)):
            if (result[journey][2] != '' and result[journey][3] != '' and
                    result[journey][5] != '' and result[journey][6] != ''):
                rid = str(result[journey][0])
                day_of_week = datetime(int(rid[:4]), int(
                    rid[4:6]), int(rid[6:8])).weekday()
                hour_of_day = int(result[journey][3].split(":")[0])
                minute_of_day = int(result[journey][3].split(":")[1])
                weekend = self.is_weekend(day_of_week)
                day_segment = self.check_day_segment(hour_of_day)
                rush_hour = self.is_rush_hour(hour_of_day, minute_of_day)
                try:
                    time_dep = (datetime.strptime(
                        result[journey][3], '%H:%M') - datetime(1900, 1, 1)).total_seconds()
                except:
                    print("Unable to get time_dep")
                    continue  # Skip this entry if there is an error
                try:
                    journey_delay = ((datetime.strptime(result[journey][3], '%H:%M') - datetime(1900, 1, 1)).total_seconds() -
                                     (datetime.strptime(result[journey][2], '%H:%M') - datetime(1900, 1, 1)).total_seconds())
                except:
                    print("Unable to get journey_delay")
                    continue  # Skip this entry if there is an error
                try:
                    time_arr = ((datetime.strptime(result[journey][6], '%H:%M') - datetime(1900, 1, 1)).total_seconds() -
                                (datetime.strptime(result[journey][5], '%H:%M') - datetime(1900, 1, 1)).total_seconds())
                except:
                    print("Unable to get time_arrival")
                    continue  # Skip this entry if there is an error

                # Skip entries where the destination is Norwich and there's no departure time from there
                if self.arrival_station == "NRCH" and result[journey][3] == '00:00':
                    continue

                data.append([rid, time_dep, journey_delay, day_of_week,
                            weekend, day_segment, rush_hour, time_arr])
        # Show first 5 entries of prepared data for verification
        print(f"Prepared data: {data[:5]}")
        return data

    def predict(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') -
                      datetime(1900, 1, 1)).total_seconds()
        delay_s = int(self.delay) * 60
        journeys = pd.DataFrame(data, columns=[
                                "rid", "time_dep", "delay", "day_of_week", "weekend", "day_segment", "rush_hour", "arrival_time"])
        journeys['arrival_time'] = journeys['arrival_time'].apply(
            lambda x: max(0, x))
        journeys['delay'] = journeys['delay'].apply(lambda x: max(0, x))
        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)
        journeys.to_csv(
            '/Users/thisgirlcan/Desktop/railway_chatBot/cw2_chatbot_task1_task2/journey2.csv')
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        outliers = iso_forest.fit_predict(journeys[['arrival_time']])
        journeys = journeys[outliers == 1]
        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        # Debug print to check the features
        print(f"Feature DataFrame: {X.head()}")
        # Debug print to check the target values
        print(f"Target Array: {y[:5]}")

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)
    

        clf = RandomForestRegressor(n_estimators=100, random_state=42)
        clf.fit(x_training_data, y_training_data)

        prediction = clf.predict(
            [[dep_time_s, delay_s, self.day_of_week, self.weekend, self.segment_of_day, self.rush_hour]])
        print(f"Raw prediction (seconds): {prediction}")

        prediction = self.convert_time([prediction])
        print(f"Converted prediction (H:M:S): {prediction}")
        total_delay_hours = prediction[0]
        if total_delay_hours > 0:
            total_delay_minutes = prediction[1] + int(self.delay) + 60 * total_delay_hours
            total_delay_seconds = prediction[2]
        elif total_delay_hours == 0:
            total_delay_minutes = prediction[1] + int(self.delay) 
            total_delay_seconds = prediction[2]
        

        print("The delay of the journey will be " + str(total_delay_minutes).zfill(2) +
              " minutes and " + str(total_delay_seconds).zfill(2) + " seconds.")
        return [prediction[0], total_delay_minutes, total_delay_seconds]

    def display_results(self, from_st, to_st, exp_dep, delay):

        self.departure_station = self.station_finder(from_st)
        self.arrival_station = self.station_finder(to_st)
        self.exp_dep = exp_dep
        hour_of_day = int(exp_dep.split(":")[0])
        minute_of_day = int(exp_dep.split(":")[1])
        self.delay = delay
        self.segment_of_day = self.check_day_segment(hour_of_day)
        self.rush_hour = self.is_rush_hour(hour_of_day, minute_of_day)

        data = self.prepare_datasets()
        print(f'data length: {len(data)}')

        prediction = self.predict(data)
       
        return (f"The total delay of the journey will be " + str(
            prediction[0]).zfill(2) + " hour(s) and "+ str(
            prediction[1]).zfill(2) +
            " minutes and " + str(prediction[2]).zfill(2) + " seconds.")


# pr = Predictions()
# pr.display_results('London', 'Norwich', '10:00', '10')
