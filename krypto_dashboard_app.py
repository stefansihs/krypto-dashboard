import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="🚀 Krypto Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00f7ff;'>🧠 Dein Krypto Cockpit</h1>", unsafe_allow_html=True)
st.markdown("<style>body {background-color: #0e1117; color: white;} .stMetric {text-align: center;}</style>", unsafe_allow_html=True)

COINS = [
    "neat", "yourai", "gmrx", "supra", "xna", "turbo", "xai", "rio", "strk", "duel", "portal",
    "phb", "pyr", "flux", "chrp", "matic", "slp", "zeta", "skey", "astr", "eth", "storj", "grt",
    "audio", "kas", "imx", "glq", "ftm", "gala", "agix", "rndr", "api3", "near", "filecoin",
    "sei", "fet", "zkj", "sui"
]

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

data = fetch_data()

if not data:
    st.error("❌ Fehler beim Laden der Marktdaten.")
else:
    df = pd.DataFrame(data)
    df = df[["name", "symbol", "current_price", "market_cap", "price_change_percentage_24h"]]
    df.columns = ["Name", "Symbol", "Preis", "Marktkapitalisierung", "24h %"]
    df = df.sort_values("24h %", ascending=False)

    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([2, 2, 6])
        with col1:
            st.markdown(f"### 🪙 {row['Name']} ({row['Symbol'].upper()})")
            st.metric("💵 Preis", f"${row['Preis']:.4f}")
        with col2:
            st.metric("📈 24h %", f"{row['24h %']:.2f} %")
        with col3:
            if row["24h %"] > 15:
                signal = "🔴 Überhitzt – Gewinne sichern?"
            elif row["24h %"] > 5:
                signal = "🟡 Beobachten – mögliche Spitze"
            else:
                signal = "🟢 Ruhig – Halten oder Einstieg"
            st.markdown(f"<div style='padding:10px;background:#1a1d24;border-radius:10px;'>{signal}</div>", unsafe_allow_html=True)
        st.markdown("---")
