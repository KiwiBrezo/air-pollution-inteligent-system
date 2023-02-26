import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics


def prepare_data():
    print("--- Starting preparing data ---")
    df = pd.read_csv("../../data/processed/processed_data.csv")

    print("Number of rows: ", len(df.index))

    df = df.dropna()

    print("Number of rows after dropping Nan rows: ", len(df.index))

    df_x = df["pm25"]
    df_y = df["pm10"]

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

    pkl_filename = "../../models/modelAirPollution.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

    print("--- Done model ---")


def save_metrics(mae, mse, rmse, mapa, acc):
    metrics_file = open("../../reports/metrics.txt", "w")

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
