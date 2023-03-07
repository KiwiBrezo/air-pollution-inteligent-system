import numpy as np
import pandas as pd
import pickle
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

file_location = os.path.dirname(__file__)


def prepare_data():
    print("--- Starting preparing data ---")
    csv_filename = os.path.join(file_location, "../../data/processed/processed_data.csv")
    df = pd.read_csv(csv_filename)

    print("Number of rows: ", len(df.index))

    df = df.dropna()

    print("Number of rows after dropping Nan rows: ", len(df.index))

    df_x = df["pm25"]
    df_x = df_x[df_x.apply(lambda x: str(x).isdigit())]
    df_x = df_x.apply(pd.to_numeric, errors='ignore', downcast='integer')

    df_y = df["pm10"]
    df_y = df_y[df_y.apply(lambda x: str(x).isdigit())]
    df_y = df_y.apply(pd.to_numeric, errors='ignore', downcast='integer')

    print("--- Done preparing data ---")

    return train_test_split(df_x, df_y, test_size=0.2)


def train_model(x_train, x_test, y_train, y_test):
    print("--- Starting training model ---")

    x_train = np.array(x_train)
    x_test = np.array(x_train)
    y_train = np.array(y_train)
    y_test = np.array(y_train)

    random_forest_model = RandomForestRegressor()

    random_forest_model.fit(x_train.reshape(-1, 1), y_train)

    predictions = random_forest_model.predict(x_test.reshape(-1, 1))

    mae = metrics.mean_absolute_error(y_test, predictions)
    mse = metrics.mean_squared_error(y_test, predictions)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))
    mape = np.mean(np.abs((y_test - predictions) / np.abs(predictions)))
    acc = round(100 * (1 - mape), 2)

    save_metrics(mae, mse, rmse, mape, acc)

    print('Mean Absolute Error (MAE):', mae)
    print('Mean Squared Error (MSE):', mse)
    print('Root Mean Squared Error (RMSE):', rmse)
    print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
    print('Accuracy:', acc)

    print("--- Done training model ---")

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
    main()
