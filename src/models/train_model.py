from pprint import pprint

import numpy as np
import pandas as pd
import pickle
import os
import mlflow
from mlflow import MlflowClient

from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
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

    return df_train_x, df_test_x, df_train_y, df_test_y


def train_model(x_train, x_test, y_train, y_test):
    print("--- Starting training model ---")

    x_train = np.array(x_train)
    x_test = np.array(x_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    train_pipe = Pipeline([
        ('imputer', SimpleImputer()),
        ('regressor', RandomForestRegressor())
    ])

    best_params = get_best_params(x_train, y_train)

    with mlflow.start_run(run_name="Train model pipeline") as run:
        train_pipe.set_params(**best_params)

        train_pipe.fit(x_train, y_train)

        predictions = train_pipe.predict(x_test)

        mae = metrics.mean_absolute_error(y_test, predictions)
        mse = metrics.mean_squared_error(y_test, predictions)
        rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))
        mape = np.mean(np.abs((y_test - predictions) / np.abs(predictions)))
        acc = round(100 * (1 - mape), 2)

        mlflow.log_params(best_params)
        mlflow.log_metrics({"mae": mae, "mse": mse, "rmse": rmse, "mape": mape, "acc": acc})
        mlflow.sklearn.log_model(train_pipe, artifact_path="sklearn-model",
                                 registered_model_name="air_pollution_reg_model")

    save_metrics(mae, mse, rmse, mape, acc)

    print('Mean Absolute Error (MAE):', mae)
    print('Mean Squared Error (MSE):', mse)
    print('Root Mean Squared Error (RMSE):', rmse)
    print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
    print('Accuracy:', acc)

    print("     -> Done training model")

    save_model(train_pipe)


def get_best_params(x_train, y_train):
    print("--- Getting best params with GridSearch ---")

    pipe = Pipeline([
        ('imputer', SimpleImputer()),
        ('regressor', RandomForestRegressor())
    ])

    param_grid = {
        'regressor__n_estimators': [50, 100, 200],
        'regressor__max_features': ['sqrt', 'log2'],
        'regressor__max_depth': [3, 5, 10, 20],
        'regressor__min_samples_split': [2, 5, 10, 20],
        'regressor__min_samples_leaf': [1, 2, 4],
    }

    grid_search = GridSearchCV(pipe, param_grid=param_grid, cv=5)
    grid_search.fit(x_train, y_train)

    print("     -> Done searching for params")

    return grid_search.best_params_


def compare_latest_model_with_production():
    print("--- Checking if latest model is better than production model ---")

    client = MlflowClient()
    latest_metrics = {}
    production_metrics = {}
    production_version = -1
    latest_version = -1
    for model in client.search_model_versions("name='air_pollution_reg_model'"):
        pprint(dict(model), indent=4)
        if int(model.version) > latest_version and model.current_stage == "None":
            latest_version = int(model.version)
            latest_metrics = client.get_metric_history(model.run_id, "acc")
        if int(model.version) > production_version and model.current_stage == "Production":
            production_version = int(model.version)
            production_metrics = client.get_metric_history(model.run_id, "acc")

    if production_version == -1 or latest_version == -1:
        return

    print("     -> Latest model accuracy:", latest_metrics[0].value)
    print("     -> Production model accuracy:", production_metrics[0].value)

    if latest_metrics[0].value > production_metrics[0].value:
        client.transition_model_version_stage(
            name="air_pollution_reg_model",
            version=latest_version,
            stage="Production"
        )

        client.transition_model_version_stage(
            name="air_pollution_reg_model",
            version=production_version,
            stage="Archived"
        )

    print("     -> Done checking results")


def save_model(model):
    print("--- Saving model ---")

    pkl_filename = os.path.join(file_location, "../../models/model_air_pollution.pkl")
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

    print("     -> Done saving model")


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
    train_model(x_train, x_test, y_train, y_test)
    compare_latest_model_with_production()


if __name__ == "__main__":
    mlflow.set_tracking_uri("https://dagshub.com/KiwiBrezo/air-pollution-inteligent-system.mlflow")
    mlflow.set_experiment(experiment_name="Train model")
    main()
