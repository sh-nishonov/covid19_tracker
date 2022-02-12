import pandas as pd
import streamlit as st


@st.cache(ttl=86400, allow_output_mutation=True)
def from_collection_to_df(data):
    data_raw = pd.DataFrame.from_dict(data, orient="index")
    series_list = [
        pd.DataFrame(
            {
                "country": index,
                "confirmed": row["confirmed"],
                "deaths": row["deaths"],
                "population": row.get("population", None),
            },
            index=[i],
        )
        for i, (index, row) in enumerate(data_raw["All"].items())
    ]
    data = pd.concat(series_list, axis=0)
    return data
