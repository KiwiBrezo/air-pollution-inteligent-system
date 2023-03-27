import numpy as np
import pandas as pd
import pickle
import os
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

file_location = os.path.dirname(__file__)


def prepare_data():
    print("--- Starting preparing data ---")

    train_csv_filename = os.path.join(file_location, "../../data/processed/train_data.csv")
    test_csv_filename = os.path.join(file_location, "../../data/processed/test_data.csv")
    df_train = pd.read_csv(train_csv_filename)
    df_test = pd.read_csv(test_csv_filename)

    print("     -> Number of rows in train dataset: ", len(df_train.index))
    print("     -> Number of rows in test dataset: ", len(df_test.index))

    df_train = df_train.dropna()
    df_test = df_test.dropna()

    print("     -> Number of rows after dropping Nan rows in train dataset: ", len(df_train.index))
    print("     -> Number of rows after dropping Nan rows in test dataset: ", len(df_test.index))

    df_train_x = df_train[
        ["temperature", "relativehumidity", "dewpoint", "surface_pressure", "cloudcover", "windspeed", "winddirection",
         "pm25"]]

    df_train_y = df_train["pm10"]

    df_test_x = df_test[
        ["temperature", "relativehumidity", "dewpoint", "surface_pressure", "cloudcover", "windspeed", "winddirection",
         "pm25"]]

    df_test_y = df_test["pm10"]

    print("     -> Done preparing data")

    # return train_test_split(df_x, df_y, test_size=0.2)
    return (df_train_x, df_test_x, df_train_y, df_test_y)


def train_model(x_train, x_test, y_train, y_test):
    print("--- Starting training model ---")
    mlflow.sklearn.autolog()

    x_train = np.array(x_train)
    x_test = np.array(x_train)
    y_train = np.array(y_train)
    y_test = np.array(y_train)

    random_forest_model = RandomForestRegressor(max_depth=10, n_estimators=10)

    random_forest_model.fit(x_train, y_train)

    predictions = random_forest_model.predict(x_test)

    mae = metrics.mean_absolute_error(y_test, predictions)
    mse = metrics.mean_squared_error(y_test, predictions)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))
    mape = np.mean(np.abs((y_test - predictions) / np.abs(predictions)))
    acc = round(100 * (1 - mape), 2)

    mlflow.last_active_run()
    save_metrics(mae, mse, rmse, mape, acc)

    print('Mean Absolute Error (MAE):', mae)
    print('Mean Squared Error (MSE):', mse)
    print('Root Mean Squared Error (RMSE):', rmse)
    print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
    print('Accuracy:', acc)

    print("     -> Done training model")

    return random_forest_model


def save_model(model):
    print("--- Saving model ---")

    pkl_filename = os.path.join(file_location, "../../models/model_air_pollution.pkl")
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

    print("     -> Done model")


def save_metrics(mae, mse, rmse, mapa, acc):
    metrics_filename = os.path.join(file_location, "../../reports/metrics.txt")
    metrics_file = open(metrics_filename, "w")

    metrics_file.write("MAE:" + str(mae) + "\n")
    metrics_file.write("MSE:" + str(mse) + "\n")
    metrics_file.write("RMSE:" + str(rmse) + "\n")
    metrics_file.write("MAPA:" + str(mapa) + "\n")
    metrics_file.write("ACCURACY:" + str(acc) + "\n")

    metrics_file.close()


def main():
    (x_train, x_test, y_train, y_test) = prepare_data()
    model = train_model(x_train, x_test, y_train, y_test)
    save_model(model)


if __name__ == "__main__":
    mlflow.set_tracking_uri("https://dagshub.com/KiwiBrezo/air-pollution-inteligent-system.mlflow")
    mlflow.set_experiment(experiment_name="Train model")
    main()
