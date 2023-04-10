from pymongo import MongoClient

database_instance = None


def get_database():
    global database_instance

    if database_instance is None:
        print("--- There is no instance of the database connector... try to connect to the database ---")
        connection_string = "iss_vaje:iss_vaje@cluster0.qitth51.mongodb.net/?retryWrites=true&w=majority"
        database_instance = MongoClient("mongodb+srv://" + connection_string)

        print("     -> Connected successfully")

    return database_instance["prediction_data"]
