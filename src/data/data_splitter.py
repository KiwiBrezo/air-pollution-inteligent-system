import os

import pandas as pd

file_location = os.path.dirname(__file__)


def split_data_to_train_test__set():
    print("--- Started splitting data ---")

    merged_csv_filename = os.path.join(file_location, "../../data/processed/current_processed_data_merged.csv")
    ref_merged_csv_filename = os.path.join(file_location, "../../data/processed/reference_processed_data_merged.csv")
    train_csv_filename = os.path.join(file_location, "../../data/processed/train_data.csv")
    test_csv_filename = os.path.join(file_location, "../../data/processed/test_data.csv")

    df_train = pd.read_csv(merged_csv_filename)
    df_train.to_csv(ref_merged_csv_filename)

    df_train = df_train[df_train["pm25"].apply(lambda x: str(x).isdigit())]
    df_train = df_train.apply(pd.to_numeric, errors='ignore', downcast='integer')
    df_train = df_train[df_train["pm10"].apply(lambda x: str(x).isdigit())]
    df_train = df_train.apply(pd.to_numeric, errors='ignore', downcast='integer')

    n = int(len(df_train) * 0.1)

    df_test = df_train.tail(n)
    df_train = df_train.iloc[:-n]

    print("     -> Thera are", len(df_train), "in train dataset and", len(df_test), "in the test dataset")

    df_train.to_csv(train_csv_filename, index=False, header=True)
    df_test.to_csv(test_csv_filename, index=False, header=True)

    print("     -> Done splitting data")


if __name__ == "__main__":
    split_data_to_train_test__set()
