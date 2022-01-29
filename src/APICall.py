import json
import urllib3
import streamlit as st


@st.cache(ttl=86400)
def get_data(url):
    http = urllib3.PoolManager()

    req = http.request("GET", url)
    data = json.loads(req.data.decode("utf-8"))

    return data


@st.cache(ttl=86400)
def get_geojson_data(path):
    with open(path) as data:
        return json.load(data)
