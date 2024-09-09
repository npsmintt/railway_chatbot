# Importing necessary libraries
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
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


from sklearn.preprocessing import StandardScaler
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

# Filter out the FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the class TestPredictions


class TestPredictions(Predictions):

    def __init__(self):
        super().__init__()
        self.metrics = {
            'Model': [],
            # 'F1 Score': [],
            'R² Score': [],
            'RMSE': [],
            # 'Accuracy': []
        }

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
                    print("Unable to get time_arrival")

                data.append([rid, time_dep, journey_delay, day_of_week,
                             weekend, day_segment, rush_hour, time_arr])
        return data

    def log_metrics(self, model_name, y_true, y_pred):
        # Implement your logging method here
        print(f"Model: {model_name}, Metrics: TBD")

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
        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)
        neighbors = KNeighborsRegressor(n_neighbors=3)
        clf = neighbors
        clf.fit(x_training_data, y_training_data)

        y_pred = clf.predict(x_test_data)
        rf_mse = mean_squared_error(y_test_data, y_pred)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)
        accuracy = accuracy_score(y_test_data, y_pred)

        print("KNN Test MSE =", rf_mse)
        print("KNN Test RMSE =", rf_rmse)
        print("KNN Test R2 =", rf_r2)
        print("KNN accuracy =", accuracy)
       
        self.log_metrics("KNN", y_test_data, y_pred)

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
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)
        accuracy = accuracy_score(y_test_data, y_pred)

        print("RFC Test MSE =", rf_mse)
        print("RFC Test RMSE =", rf_rmse)
        print("RFC Test R2 =", rf_r2)
        print("RFC accuracy =", accuracy)

        self.log_metrics("Random Forest", y_test_data, y_pred)

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

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(x_training_data)
        X_test = scaler.transform(x_test_data)

        regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        regressor.fit(X_train, y_training_data)

        y_pred = regressor.predict(X_test)
        rf_mse = mean_squared_error(y_test_data, y_pred)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)

        print("RFR Test MSE =", rf_mse)
        print("RFR Test RMSE =", rf_rmse)
        print("RFR Test R2 =", rf_r2)
        self.log_metrics("Random Forest Regressor", y_test_data, y_pred)

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

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        clf = GaussianNB()
        clf.fit(x_training_data, y_training_data)

        y_pred = clf.predict(x_test_data)
        rf_mse = mean_squared_error(y_test_data, y_pred)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)
        accuracy = accuracy_score(y_test_data, y_pred)

        print("NB Test MSE =", rf_mse)
        print("NB Test RMSE =", rf_rmse)
        print("NB Test R2 =", rf_r2)
        print("NB accuracy =", accuracy)
        self.log_metrics("Decision Tree", y_test_data, y_pred)
        self.log_metrics("Naive Bayes", y_test_data, y_pred)

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

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(x_training_data)
        X_test = scaler.transform(x_test_data)

        dt = DecisionTreeClassifier().fit(X_train, y_training_data)
        y_pred = dt.predict(X_test)
        rf_mse = mean_squared_error(y_test_data, y_pred)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)
        accuracy = accuracy_score(y_test_data, y_pred)

        print("DT Test MSE =", rf_mse)
        print("DT Test RMSE =", rf_rmse)
        print("DT Test R2 =", rf_r2)
        print("DT accuracy =", accuracy)
        self.log_metrics("Decision Tree", y_test_data, y_pred)

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

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(x_training_data)
        X_test = scaler.transform(x_test_data)

        lr = LinearRegression().fit(X_train, y_training_data)
        y_lr = lr.predict(X_test)
        rf_mse = mean_squared_error(y_test_data, y_lr)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_lr)

        print("LR Test MSE =", rf_mse)
        print("LR Test RMSE =", rf_rmse)
        print("LR Test R2 =", rf_r2)
        self.log_metrics("Linear Regression", y_test_data, y_lr)
    
    def predict_nn(self, data):
        dep_time_s = (datetime.strptime(self.exp_dep, '%H:%M') -
                      datetime(1900, 1, 1)).total_seconds()
        print(f"dep_time_s: {dep_time_s}")
        delay_s = int(self.delay) * 60

        journeys = pd.DataFrame(data, columns=[
                                "rid", "time_dep", "delay", "day_of_week", "weekend", "day_segment", "rush_hour", "arrival_time"])
        print(f"journeys: {journeys}")

        journeys['rush_hour'] = pd.to_numeric(
            journeys['rush_hour'], errors='coerce')
        journeys['rush_hour'].fillna(0, inplace=True)

        X = journeys.drop(['rid', 'arrival_time'], axis=1)
        y = journeys['arrival_time'].values

        x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(
            X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(x_training_data)
        X_test = scaler.transform(x_test_data)

        # Building the neural network
        model = Sequential()
        model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))  # Output layer for regression

        # Compile the model
        model.compile(optimizer=Adam(learning_rate=0.001),
                      loss='mean_squared_error')

        # Train the model
        model.fit(X_train, y_training_data,
                  epochs=50, batch_size=10, verbose=1)

        # Predict using the neural network
        y_pred = model.predict(X_test)
        rf_mse = mean_squared_error(y_test_data, y_pred)
        rf_rmse = np.sqrt(rf_mse)
        rf_r2 = r2_score(y_test_data, y_pred)
        
        print("NN Test MSE =", rf_mse)
        print("NN Test RMSE =", rf_rmse)
        print("NN Test R2 =", rf_r2)
        

        # Log metrics
        self.log_metrics("Neural Network", y_test_data, y_pred)
        

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
        self.rush_hour = super(). is_rush_hour(hour_of_day, minute_of_day)
        data = self.prepare_datasets()

        # self.predict_knn(data)
        # self.predict_rf(data)
        self.predict_rf_re(data)
        # self.predict_naive_bayes(data)
        # self.predict_dt(data)
        self.predict_lr(data)
        # self.predict_nn(data)

        self.visualize_metrics()

    def visualize_metrics(self):
        df_metrics = pd.DataFrame(self.metrics)
        # Colors for different models
        colors = sns.color_palette("hsv", len(df_metrics['Model'].unique()))

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Model Performance Comparison', fontsize=16)

        # sns.barplot(ax=axes[0, 0], x='Model', y='F1 Score',
        #             data=df_metrics, palette=colors)
        # axes[0, 0].set_title('F1 Score by Model')
        # axes[0, 0].set_ylabel('F1 Score')
        # axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=45)

        sns.barplot(ax=axes[0, 1], x='Model', y='R² Score',
                    data=df_metrics, palette=colors)
        axes[0, 1].set_title('R² Score by Model')
        axes[0, 1].set_ylabel('R² Score')
        axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45)

        sns.barplot(ax=axes[1, 0], x='Model', y='RMSE',
                    data=df_metrics, palette=colors)
        axes[1, 0].set_title('RMSE by Model')
        axes[1, 0].set_ylabel('RMSE')
        axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=45)

        # sns.barplot(ax=axes[1, 1], x='Model', y='Accuracy',
        #             data=df_metrics, palette=colors)
        # axes[1, 1].set_title('Accuracy by Model')
        # axes[1, 1].set_ylabel('Accuracy')
        # axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()


# # Create an instance of the class and run tests
test = TestPredictions()
test.run_tests()
