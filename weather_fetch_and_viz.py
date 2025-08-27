import argparse
import sys
from pathlib import Path
import requests
import pandas as pd
import matplotlib.pyplot as plt

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def geocode_city(city: str):
    r = requests.get(GEOCODE_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("results"):
        raise ValueError(f"City '{city}' not found.")
    top = data["results"][0]
    return {
        "name": top["name"],
        "country": top.get("country", ""),
        "lat": top["latitude"],
        "lon": top["longitude"],
        "timezone": top.get("timezone", "auto")
    }

def fetch_hourly_forecast(lat, lon, timezone, days: int):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "forecast_days": days,
        "timezone": timezone
    }
    r = requests.get(FORECAST_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def to_dataframe(api_json: dict) -> pd.DataFrame:
    hourly = api_json["hourly"]
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time").sort_index()
    # nicer column names
    df = df.rename(columns={
        "temperature_2m": "temp_C",
        "relative_humidity_2m": "humidity_pct",
        "wind_speed_10m": "wind_kmh"
    })
    return df

def plot_temperature(df: pd.DataFrame, outpath: Path, city: str):
    plt.figure(figsize=(11, 4))
    plt.plot(df.index, df["temp_C"])
    plt.title(f"Hourly Temperature – {city}")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig(outpath / "01_temperature_line.png", dpi=150)
    plt.close()

def plot_daily_avg_temp(df: pd.DataFrame, outpath: Path, city: str):
    daily = df["temp_C"].resample("D").mean()
    plt.figure(figsize=(8, 4))
    plt.bar(daily.index.strftime("%d-%b"), daily.values)
    plt.title(f"Daily Avg Temperature – {city}")
    plt.xlabel("Day")
    plt.ylabel("Avg Temp (°C)")
    plt.tight_layout()
    plt.savefig(outpath / "02_daily_avg_temp.png", dpi=150)
    plt.close()

def plot_precipitation(df: pd.DataFrame, outpath: Path, city: str):
    daily_precip = df["precipitation"].resample("D").sum()
    plt.figure(figsize=(8, 4))
    plt.bar(daily_precip.index.strftime("%d-%b"), daily_precip.values)
    plt.title(f"Daily Precipitation – {city}")
    plt.xlabel("Day")
    plt.ylabel("Total Precipitation (mm)")
    plt.tight_layout()
    plt.savefig(outpath / "03_daily_precipitation.png", dpi=150)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Fetch weather via Open-Meteo and create visualizations.")
    parser.add_argument("--city", required=True, help="City name, e.g., Hyderabad")
    parser.add_argument("--days", type=int, default=7, help="Forecast days (1–16)")
    parser.add_argument("--outdir", default="outputs", help="Output folder")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    data_dir = outdir / "data"
    figs_dir = outdir / "figs"
    data_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    try:
        loc = geocode_city(args.city)
        print(f"→ {loc['name']}, {loc['country']} @ ({loc['lat']}, {loc['lon']}) | tz={loc['timezone']}")
        raw = fetch_hourly_forecast(loc["lat"], loc["lon"], loc["timezone"], args.days)
        df = to_dataframe(raw)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Save CSV
    csv_path = data_dir / f"{loc['name'].replace(' ', '_').lower()}_hourly_{args.days}d.csv"
    df.to_csv(csv_path, index=True)
    print(f"✓ Saved data to {csv_path}")

    # Quick stats
    print("=== Quick Stats ===")
    print(f"Rows: {len(df)} | From {df.index.min()} to {df.index.max()}")
    print(f"Temp °C → min: {df['temp_C'].min():.1f}, mean: {df['temp_C'].mean():.1f}, max: {df['temp_C'].max():.1f}")
    print(f"Humidity % → mean: {df['humidity_pct'].mean():.1f}")
    print(f"Wind km/h → mean: {df['wind_kmh'].mean():.1f}")
    print(f"Total precipitation (mm): {df['precipitation'].sum():.1f}")

    # Charts
    plot_temperature(df, figs_dir, loc["name"])
    plot_daily_avg_temp(df, figs_dir, loc["name"])
    plot_precipitation(df, figs_dir, loc["name"])
    print(f"✓ Charts saved to {figs_dir}")

if __name__ == "__main__":
    main()
