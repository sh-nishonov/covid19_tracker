from APICall import get_data
from CRUD import update_realtime
from data_manipulation import manipulate_realtime_info
import streamlit as st
from pathlib import Path


# @st.cache(hash_funcs={"pymongo.mongo_client.MongoClient": id})
# def get_db_connection(url):
#     client = pymongo.MongoClient(url)
#     return client
st.text("# Global COVID-19 data.")


def main():

    # print(config["API_BASE"])
    data = get_data(st.secrets.API_BASE)
    update_realtime(data)
    # db = get_db_connection(Config.CONNECTION_STRING)
    # collection_realtime_info = db.covid19.realtime_info
    # df = from_collection_to_df(collection_realtime_info)
    # df.to_csv("../data/realtime_info.csv")
    # respond = create(collection_realtime_info, data)
    geojson_path = Path(__file__).parent[1]
    st.write(geojson_path)
    fig = manipulate_realtime_info(
        path_geojson="../data/countries.geojson", db_name="covid19", collection="realtime_info"
    )
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
