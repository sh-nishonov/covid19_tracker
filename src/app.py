from APICall import get_data
from CRUD import from_collection_to_df
from data_manipulation import manipulate_realtime_info, plot_realtime_info
import streamlit as st
from pathlib import Path
import millify


# @st.cache(hash_funcs={"pymongo.mongo_client.MongoClient": id})
# def get_db_connection(url):
#     client = pymongo.MongoClient(url)
#     return client
# st.text("# Global COVID-19 data.")


def main():
    """[summary]"""
    st.title("COVID-19 MINI DASHBOARD")
    confirmed_col, deaths_col, vaccines_col = st.columns(3)

    data = get_data(st.secrets.API_BASE)

    geojson_path = Path(__file__).parents[1]

    df = from_collection_to_df(data)

    df, countries, df_global = manipulate_realtime_info(
        path_geojson=geojson_path / "data/countries.geojson", df=df
    )

    with confirmed_col:
        st.subheader("Confirmed Cases")
        st.text(
            millify.millify(df_global.iloc[0, 1], precision=2)
        )  # millify(df_global.iloc[0, 2], precision=2)
    with deaths_col:
        st.subheader("Death Cases")
        st.text(
            millify.millify(df_global.iloc[0, 2], precision=2)
        )  # millify(df_global.iloc[0, 3], precision=2)
    with vaccines_col:
        st.subheader("Vaccines")
        st.text("0")
    fig = plot_realtime_info(df, countries)
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
