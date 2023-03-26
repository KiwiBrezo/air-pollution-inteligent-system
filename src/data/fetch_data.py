from src.data.data_splitter import split_data_to_train_test__set
from src.data.fetch_air_data import get_data_air_pollution
from src.data.fetch_weather_history_data import get_data_weather_history
from src.data.merge_air_weather_data import merge_processed_data
from src.data.process_air_data import pre_preprocess_data_air_pollution
from src.data.process_weather_history_data import pre_preprocess_data_weather_historical


def main():
    get_data_air_pollution()
    pre_preprocess_data_air_pollution()
    get_data_weather_history()
    pre_preprocess_data_weather_historical()
    merge_processed_data()
    split_data_to_train_test__set()


if __name__ == "__main__":
    main()
