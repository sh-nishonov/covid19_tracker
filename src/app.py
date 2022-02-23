from APICall import get_data
from CRUD import from_collection_to_df, from_collection_to_df_vaccines
from data_manipulation import manipulate_realtime_info, plot_realtime_info
import streamlit as st
from pathlib import Path
import millify


# @st.cache(hash_funcs={"pymongo.mongo_client.MongoClient": id})
# def get_db_connection(url):
#     client = pymongo.MongoClient(url)
#     return client
# st.text("# Global COVID-19 data.")
st.set_page_config(layout="wide")


def main():

    """[summary]"""
    st.title("COVID-19 MINI DASHBOARD")
    confirmed_col, deaths_col, vaccines_col = st.columns(3)
    plot_cases, plot_vacciness = st.columns([1, 1])

    data = get_data(st.secrets.API_BASE, "cases")
    data_vaccines = get_data(st.secrets.API_BASE, "vaccines")

    geojson_path = Path(__file__).parents[1]

    df = from_collection_to_df(data)
    df_vaccines = from_collection_to_df_vaccines(data_vaccines)

    df, countries, df_global = manipulate_realtime_info(
        path_geojson=geojson_path / "data/countries.geojson", df=df
    )
    df_vaccines, countries, df_global_vaccines = manipulate_realtime_info(
        path_geojson=geojson_path / "data/countries.geojson", df=df_vaccines
    )
    fig_cases = plot_realtime_info(df, countries, "cases")
    fig_vaccines = plot_realtime_info(df_vaccines, countries, "vaccines")
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
        st.text(millify.millify(df_global_vaccines.iloc[0, 2], precision=2))

    plot_cases.plotly_chart(fig_cases)

    plot_vacciness.plotly_chart(fig_vaccines)

    st.info("The project is under a heavy development.")


if __name__ == "__main__":
    main()
