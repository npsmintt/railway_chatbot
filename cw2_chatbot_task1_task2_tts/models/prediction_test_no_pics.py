from prediction import Predictions
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, f1_score, accuracy_score, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from scipy import stats
from sklearn.ensemble import IsolationForest


import numpy as np
import warnings


# Filter out the FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)


class TestPredictions(Predictions):

    def __init__(self):
        super().__init__()

    def prepare_datasets(self):
        result = super().get_data()

        data = []

        for journey in range(len(result)):
            if (result[journey][2] != '' and result[journey][3] != '' and
                    result[journey][5] != '' and result[journey][6] != ''):
                rid = str(result[journey][0])
                day_of_week = datetime(int(rid[:4]), int(rid[4:6]),
                                       int(rid[6:8])).weekday()
                hour_of_day = int(result[journey][3].split(":")[0])
                minute_of_day = int(result[journey][3].split(":")[1])
                weekend = super().is_weekend(day_of_week)
                day_segment = super().check_day_segment(hour_of_day)
                rush_hour = super().is_rush_hour(hour_of_day, minute_of_day)
                try:
                    time_dep = (datetime.strptime(result[journey][3], '%H:%M') -
                                datetime(1900, 1, 1)).total_seconds()
                except:
                    print("Unable to get time_dep")
                try:
                    journey_delay = ((datetime.strptime(result[journey][3], '%H:%M') -
                                      datetime(1900, 1, 1)).total_seconds() -
                                     (datetime.strptime(result[journey][2], '%H:%M') -
                                      datetime(1900, 1, 1)).total_seconds())
                except:
                    print("Unable to get journey_delay")
                try:
                    time_arr = ((datetime.strptime(result[journey][6], '%H:%M') -
                                 datetime(1900, 1, 1)).total_seconds() -
                                (datetime.strptime(result[journey][5], '%H:%M') -
                                     datetime(1900, 1, 1)).total_seconds())
                except:
                    print("Unable to get  time_arrival")

                data.append([rid, time_dep, journey_delay, day_of_week,
                             weekend, day_segment, rush_hour,  time_arr])
        return data

    def predict_knn(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') - datetime(
            1900, 1, 1)).total_seconds()
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=["rid", "time_dep",
                                               "delay", "day_of_week", "weekend",
                                               "day_segment", "rush_hour", "arrival_time"])
        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)

        # Remove outliers using Z-score
        z_scores = stats.zscore(journeys['arrival_time'])
        abs_z_scores = np.abs(z_scores)
        filtered_entries = (abs_z_scores < 4)  # Use threshold 3 for Z-score
        journeys = journeys[filtered_entries]

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        clf = KNeighborsRegressor(n_neighbors=3)
        clf.fit(x_training_data, y_training_data)

        y_pred = clf.predict(x_test_data)

        print("KNN RMSE:", np.sqrt(mean_squared_error(y_test_data, y_pred)))
        print("KNN R2:", r2_score(y_test_data, y_pred))
        print("KNN Accuracy:", accuracy_score(
            np.round(y_test_data), np.round(y_pred)))
        print("KNN F1 Score:", f1_score(np.round(y_test_data),
              np.round(y_pred), average="weighted"))


    def predict_rf(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') - datetime(
            1900, 1, 1)).total_seconds()
        print(f"dep_time_s:{dep_time_s}")
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=["rid", "time_dep",
                                               "delay", "day_of_week", "weekend",
                                               "day_segment", "rush_hour", "arrival_time"])
        print(f"journeys:{journeys}")
        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)
        Q1 = journeys['arrival_time'].quantile(0.25)

        Q3 = journeys['arrival_time'].quantile(0.75)
        IQR = Q3 - Q1
        filter = (journeys['arrival_time'] >= Q1 - 1.5 *
                  IQR) & (journeys['arrival_time'] <= Q3 + 1.5 * IQR)
        journeys = journeys.loc[filter]

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(x_training_data)
        X_test = scaler.transform(x_test_data)

        clf = RandomForestClassifier(n_estimators=100)
        clf.fit(X_train, y_training_data)

        y_pred = clf.predict(X_test)
        rf_mse = mean_squared_error(y_test_data, y_pred)

        rf_r2 = r2_score(y_test_data, y_pred)

        print("Linear Regression Test MSE =", rf_mse, "Test R2 =", rf_r2)
        print("RF acc_sc:", accuracy_score(y_test_data, y_pred) * 100)
        print("RF r2:", r2_score(y_test_data, y_pred) * 100)
        print("RF f1_score", f1_score(
            y_test_data, y_pred, average="weighted") * 100)
        print("RF RMSE", np.sqrt(mean_squared_error(y_test_data, y_pred)))

        # print("KNN MSE  is :", ((mse_total / mse_counter) / 60))

    def predict_rf_re(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') -
                      datetime(1900, 1, 1)).total_seconds()
        print(f"dep_time_s: {dep_time_s}")
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=["rid", "time_dep", "delay", "day_of_week", "weekend",
                                               "day_segment", "rush_hour", "arrival_time"])
        print(f"journeys: {journeys}")
        
        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)
        # Q1 = journeys['arrival_time'].quantile(0.25)

        # Q3 = journeys['arrival_time'].quantile(0.75)
        # IQR = Q3 - Q1
        # filter = (journeys['arrival_time'] >= Q1 - 1.5 *
        #           IQR) & (journeys['arrival_time'] <= Q3 + 1.5 * IQR)
        # journeys = journeys.loc[filter]
        
        # Remove outliers using Z-score
        # z_scores = stats.zscore(journeys['arrival_time'])
        # abs_z_scores = np.abs(z_scores)
        # filtered_entries = (abs_z_scores < 4)  # Use threshold 3 for Z-score
        # journeys = journeys[filtered_entries]
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        outliers = iso_forest.fit_predict(journeys[['arrival_time']])
        journeys = journeys[outliers == 1]



        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        X_train, X_test, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # scaler = StandardScaler()
        # X_train = scaler.fit_transform(x_training_data)
        # X_test = scaler.transform(x_test_data)

        regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        regressor.fit(X_train, y_training_data)

        y_pred = regressor.predict(X_test)
        rf_mse = mean_squared_error(y_test_data, y_pred)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)

        print("Random Forest Regression Test MSE =", rf_mse)
        print("Random Forest Regression Test RMSE =", rf_rmse)
        print("Random Forest Regression Test R2 =", rf_r2)

# Usage example
# predictor = YourClass() # Create an instance of your class where this method is defined
# predictor.predict_rf(your_data) # Pass your data to the method

    def predict_naive_bayes(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') - datetime(
            1900, 1, 1)).total_seconds()
        print(f"dep_time_s:{dep_time_s}")
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=["rid", "time_dep",
                                               "delay", "day_of_week", "weekend",
                                               "day_segment", "rush_hour", "arrival_time"])
        print(f"journeys:{journeys}")
        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        outliers = iso_forest.fit_predict(journeys[['arrival_time']])
        journeys = journeys[outliers == 1]

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Use GaussianNB if features are normally distributed
        clf = GaussianNB()
        clf.fit(x_training_data, y_training_data)

        y_pred = clf.predict(x_test_data)

        print("NB acc_sc:", accuracy_score(y_test_data, y_pred) * 100)
        print("NB r2:", metrics.r2_score(y_test_data, y_pred) * 100)
        print("NB f1_score", f1_score(
            y_test_data, y_pred, average="weighted") * 100)
        print("NB RMSE:", np.sqrt(mean_squared_error(y_test_data, y_pred)))

    def predict_dt(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') - datetime(
            1900, 1, 1)).total_seconds()
        print(f"dep_time_s:{dep_time_s}")
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=["rid", "time_dep",
                                               "delay", "day_of_week", "weekend",
                                               "day_segment", "rush_hour", "arrival_time"])
        print(f"journeys:{journeys}")

        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)
        
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        outliers = iso_forest.fit_predict(journeys[['arrival_time']])
        journeys = journeys[outliers == 1]

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(x_training_data)
        X_test = scaler.transform(x_test_data)

        dt = DecisionTreeClassifier().fit(X_train, y_training_data)
        y_lr = dt.predict(X_test)
        dt_mse = mean_squared_error(y_test_data, y_lr)

        dt_r2 = r2_score(y_test_data, y_lr)

        # print("Linear Regression Test MSE =", dt_mse, "Test R2 =", dt_r2)

        print("DT acc_sc:", accuracy_score(y_test_data, y_lr) * 100)
        print("DT r2:", metrics.r2_score(y_test_data, y_lr) * 100)
        print("DT f1_score", f1_score(
            y_test_data, y_lr, average="weighted") * 100)
        print("DT RMSE", np.sqrt(mean_squared_error(y_test_data, y_lr)))

    def predict_lr(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') - datetime(
            1900, 1, 1)).total_seconds()
        print(f"dep_time_s:{dep_time_s}")
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=["rid", "time_dep",
                                               "delay", "day_of_week", "weekend",
                                               "day_segment", "rush_hour", "arrival_time"])
        print(f"journeys:{journeys}")
        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)
        # Q1 = journeys['arrival_time'].quantile(0.25)

        # Q3 = journeys['arrival_time'].quantile(0.75)
        # IQR = Q3 - Q1
        # filter = (journeys['arrival_time'] >= Q1 - 1.5 *
        #           IQR) & (journeys['arrival_time'] <= Q3 + 1.5 * IQR)
        # journeys = journeys.loc[filter]
        # Remove outliers using Z-score
        # z_scores = stats.zscore(journeys['arrival_time'])
        # abs_z_scores = np.abs(z_scores)
        # filtered_entries = (abs_z_scores < 4)  # Use threshold 3 for Z-score
        # journeys = journeys[filtered_entries]
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        outliers = iso_forest.fit_predict(journeys[['arrival_time']])
        journeys = journeys[outliers == 1]
        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=5)

        # scaler = StandardScaler()
        # X_train = scaler.fit_transform(x_training_data)
        # X_test = scaler.transform(x_test_data)

        lr = LinearRegression().fit(x_training_data, y_training_data)
        y_lr = lr.predict(x_test_data)
        lin_mse = mean_squared_error(y_test_data, y_lr)
        lin_rmse = np.sqrt(lin_mse)
        lin_r2 = r2_score(y_test_data, y_lr)
        print("Linear Regression Test MSE =", lin_mse)
        print("Linear Forest Regression Test RMSE =", lin_rmse)
        print("Linear Forest Regression Test R2 =", lin_r2)

        # print("Linear Regression Test MSE =", lin_mse, "Test R2 =", lin_r2)
        # # print("RF acc_sc:", accuracy_score(y_test_data, y_lr) * 100)
        # print("RF r2:", r2_score(y_test_data, y_lr) * 100)
        # print("RF f1_score", f1_score(
        #     y_test_data, y_lr, average="weighted") * 100)
        # print("RF RMSE", np.sqrt(mean_squared_error(y_test_data, y_lr)))

        # y_pred = clf.predict(x_test_data)
        # print("LR acc_sc:", accuracy_score(y_test_data, y_pred))
        # print("LR r2:", metrics.r2_score(y_test_data, y_pred))
        # print("LR f1_score", f1_score(
        #     y_test_data, y_pred, average="weighted"))
        # print("LR RMSE", np.sqrt(mean_squared_error(y_test_data, y_pred)))

    def run_tests(self):
        depart = "09:00"
        FROM = "DISS"
        TO = "Manningtree"
        delay = 12

        print("Departing at:", depart)

        self.departure_station = super().station_finder(FROM)
        self.arrival_station = super().station_finder(TO)
        self.exp_dep = depart
        self.delay = delay
        hour_of_day = int(depart.split(":")[0])
        minute_of_day = int(depart.split(":")[1])
        self.segment_of_day = super().check_day_segment(hour_of_day)
        self.rush_hour = super().is_rush_hour(hour_of_day, minute_of_day)
        data = self.prepare_datasets()

        # self.predict_knn(data)
        # self.predict_rf(data)
        # self.predict_naive_bayes(data)
        # self.predict_dt(data)
        self.predict_lr(data)
        # self.predict_rf_re(data)


test = TestPredictions()
test.run_tests()
