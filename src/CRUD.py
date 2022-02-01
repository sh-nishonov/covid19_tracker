import pandas as pd
import numpy as np
from functools import wraps
import pymongo
import streamlit as st


def provide_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = pymongo.MongoClient(st.secrets.CONNECTION_STRING)
        result = func(conn=conn, *args, **kwargs)
        conn.close()
        return result

    return wrapper


@st.cache(ttl=86400)
@provide_db_connection
def update_realtime(data, conn):

    for country, country_stats in data.items():
        for city, city_stats in country_stats.items():
            mapping = {
                "filter": {"country": country + city},
                "update": {
                    "$set": {
                        "confirmed": city_stats["confirmed"],
                        "deaths": city_stats["deaths"],
                    }
                },
            }

            conn.covid19.realtime_info.update_one(**mapping)


@st.cache(ttl=86400)
@provide_db_connection
def from_collection_to_df(conn, db_name, coll_name):
    return pd.DataFrame(list(conn[db_name][coll_name].find({})))


def create(collection, data):
    document = []
    for country, country_stats in data.items():
        for city, city_stats in country_stats.items():
            if city == "All":

                document.append(
                    {
                        "country": country,
                        "city": False,
                        "confirmed": city_stats["confirmed"],
                        "deaths": city_stats["deaths"],
                        "population": city_stats.get("population", 0),
                        "lat": city_stats.get("lat", np.nan),
                        "long": city_stats.get("long", np.nan),
                    }
                )
            else:

                document.append(
                    {
                        "country": country + "_" + city,
                        "confirmed": city_stats["confirmed"],
                        "city": True,
                        "deaths": city_stats["deaths"],
                        "population": city_stats.get("population", 0),
                        "lat": city_stats.get("lat", np.nan),
                        "long": city_stats.get("long", np.nan),
                    }
                )

    respond = collection.insert_many(document)
    return respond
