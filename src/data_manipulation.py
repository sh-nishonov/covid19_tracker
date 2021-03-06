from APICall import get_geojson_data
import pandas as pd
import plotly.express as px
import plotly
import numpy as np
import streamlit as st


@st.cache(ttl=86400)
def update_df(df):
    df.replace(
        {
            "country": {
                "Korea, South": "South Korea",
                "US": "United States of America",
                "Czechia": "Czech Republic",
                "Bahamas": "The Bahamas",
                "Taiwan*": "Taiwan",
                "Congo (Kinshasa)": "Democratic Republic of the Congo",
                "Congo (Brazzaville)": "Republic of Congo",
                "Cabo Verde": "Cape Verde",
                "Serbia": "Republic of Serbia",
                "Burma": "Myanmar",
                "Cote d'Ivoire": "Ivory Coast",
                "Tanzania": "United Republic of Tanzania",
                "North Macedonia": "Macedonia",
            }
        },
        inplace=True,
    )
    return df


@st.cache(ttl=86400)
def manipulate_realtime_info(path_geojson, df):
    countries = get_geojson_data(path_geojson)

    new_countries = pd.DataFrame(
        [name["properties"]["ADMIN"] for name in countries["features"]],
        columns=["country"],
    )
    df = update_df(df)

    df_global = df.loc[df["country"] == "Global", :]
    df_new = df.merge(new_countries, how="inner", on=["country"])
    df_new["log_count"] = np.log10(df_new.iloc[:, 2])
    return (df_new, countries, df_global)


@st.cache(ttl=86400)
def plot_realtime_info(
    dataframe: pd.DataFrame, countries, fig_info_type
) -> plotly.graph_objects.Figure:
    if fig_info_type == "cases":
        fig = px.choropleth_mapbox(
            dataframe[["country", "confirmed", "log_count"]],
            geojson=countries,
            locations="country",
            featureidkey="properties.ADMIN",
            color="log_count",
            hover_name="country",
            hover_data=["confirmed"],
            color_continuous_scale="Reds",
            mapbox_style="carto-positron",
            zoom=0,
            labels={"log_count": "Count"},
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    elif fig_info_type == "vaccines":
        fig = px.choropleth_mapbox(
            dataframe[["country", "people_vaccinated", "log_count"]],
            geojson=countries,
            locations="country",
            featureidkey="properties.ADMIN",
            color="log_count",
            hover_name="country",
            hover_data=["people_vaccinated"],
            color_continuous_scale="Blues",
            mapbox_style="carto-positron",
            zoom=0,
            labels={"log_count": "Count"},
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
