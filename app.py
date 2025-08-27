import time
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

st.set_page_config(page_title="Weather API & Visualization", page_icon="☁️", layout="wide")
st.title("☁️ API Integration & Data Visualization – Open-Meteo")
st.caption("Enter a city, fetch hourly weather, and explore quick charts.")

@st.cache_data(show_spinner=False, ttl=1800)
def geocode_city(city: str):
    r = requests.get(GEOCODE_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        return None
    top = data["results"][0]
    return {
        "name": top["name"],
        "country": top.get("country", ""),
        "lat": top["latitude"],
        "lon": top["longitude"],
        "timezone": top.get("timezone", "auto")
    }

@st.cache_data(show_spinner=False, ttl=600)
def fetch_df(city: str, days: int) -> pd.DataFrame | None:
    loc = geocode_city(city)
    if not loc:
        return None
    params = {
        "latitude": loc["lat"],
        "longitude": loc["lon"],
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "forecast_days": days,
        "timezone": loc["timezone"]
    }
    r = requests.get(FORECAST_URL, params=params, timeout=30)
    r.raise_for_status()
    hourly = r.json()["hourly"]
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time").sort_index()
    df = df.rename(columns={
        "temperature_2m": "temp_C",
        "relative_humidity_2m": "humidity_pct",
        "wind_speed_10m": "wind_kmh"
    })
    df.attrs["loc"] = loc
    return df

with st.sidebar:
    st.header("Controls")
    city = st.text_input("City name", value="Hyderabad")
    days = st.slider("Forecast days", min_value=3, max_value=16, value=7)
    go = st.button("Fetch data")

if go:
    with st.spinner("Contacting API..."):
        df = fetch_df(city, days)

    if df is None or df.empty:
        st.error("City not found or no data.")
        st.stop()

    loc = df.attrs["loc"]
    st.subheader(f"{loc['name']}, {loc['country']}  ({loc['lat']:.2f}, {loc['lon']:.2f})  – tz: {loc['timezone']}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Min Temp (°C)", f"{df['temp_C'].min():.1f}")
    col2.metric("Avg Temp (°C)", f"{df['temp_C'].mean():.1f}")
    col3.metric("Max Temp (°C)", f"{df['temp_C'].max():.1f}")
    col4.metric("Total Rain (mm)", f"{df['precipitation'].sum():.1f}")

    # Show data preview
    st.write("#### Sample data")
    st.dataframe(df.head(24))

    # Plot 1: Hourly temperature
    st.write("#### Hourly Temperature")
    fig1, ax1 = plt.subplots(figsize=(10, 3.5))
    ax1.plot(df.index, df["temp_C"])
    ax1.set_xlabel("Time")
    ax1.set_ylabel("°C")
    ax1.set_title(f"Hourly Temperature – {loc['name']}")
    st.pyplot(fig1)

    # Plot 2: Daily average temperature
    st.write("#### Daily Average Temperature")
    daily = df["temp_C"].resample("D").mean()
    fig2, ax2 = plt.subplots(figsize=(8, 3.2))
    ax2.bar(daily.index.strftime("%d-%b"), daily.values)
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Avg °C")
    ax2.set_title("Daily Avg Temperature")
    st.pyplot(fig2)

    # Plot 3: Daily precipitation
    st.write("#### Daily Precipitation")
    precip = df["precipitation"].resample("D").sum()
    fig3, ax3 = plt.subplots(figsize=(8, 3.2))
    ax3.bar(precip.index.strftime("%d-%b"), precip.values)
    ax3.set_xlabel("Day")
    ax3.set_ylabel("mm")
    ax3.set_title("Daily Precipitation")
    st.pyplot(fig3)

    st.success("Done ✅")
else:
    st.info("Enter a city in the sidebar and click **Fetch data**.")
