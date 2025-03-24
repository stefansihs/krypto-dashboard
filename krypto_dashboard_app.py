
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="📊 Krypto Dashboard", layout="wide")
st.title("💰 Krypto Watchlist & Take-Profit-Signale")

# Projektliste
COINS = [
    "sui", "eth", "near", "gala", "api3", "agix", "rndr", "filecoin", "kas", "grt", "imx",
    "audio", "ftm", "injective", "celestia", "aptos", "sei", "turbo", "xai", "astr", "slp", "zeta"
]

# Daten abrufen
def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'ids': ','.join(COINS),
        'order': 'market_cap_desc',
        'per_page': len(COINS),
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

with st.spinner("📡 Lade aktuelle Marktdaten..."):
    data = fetch_data()

if not data:
    st.error("❌ Fehler beim Laden der Daten.")
else:
    df = pd.DataFrame(data)
    df = df[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]
    df.columns = ["Name", "Symbol", "Preis (USD)", "Marktkapitalisierung", "Volumen (24h)", "24h %"]

    # Take-Profit-Signal
    def signal(row):
        if row["24h %"] > 15:
            return "🔴 Überhitzt – Gewinne sichern?"
        elif row["24h %"] > 5:
            return "🟡 Beobachten – mögliche Spitze"
        else:
            return "🟢 Ruhig – Halten oder Einstieg"

    df["Signal"] = df.apply(signal, axis=1)

    st.subheader("📈 Live Coin-Daten")
    st.dataframe(df.sort_values("24h %", ascending=False), use_container_width=True)
    st.caption("Signal-Logik: 🔴 >15%, 🟡 >5%, 🟢 sonst")
