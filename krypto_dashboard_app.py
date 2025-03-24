import streamlit as st
import requests
import pandas as pd

# ------------------ Einstellungen ------------------
st.set_page_config(page_title="🧠 Krypto Cockpit", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #33ffcc;'>🚀 Dein Koinfolio Dashboard</h1>", unsafe_allow_html=True)

# ------------------ Deine Coin-Liste ------------------
COINS = [
    "neat", "yourai", "gmrx", "supra", "xna", "turbo", "xai", "rio", "strk", "duel", "portal",
    "phb", "pyr", "flux", "chrp", "matic", "slp", "zeta", "skey", "astr", "eth", "storj", "grt",
    "audio", "kas", "imx", "glq", "ftm", "gala", "agix", "rndr", "api3", "near", "filecoin",
    "sei", "fet", "zkj", "sui"
]

# ------------------ Daten abrufen ------------------
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

    # ------------------ Darstellung ------------------
    st.markdown("### 📈 Marktübersicht:")

    for index, row in df.iterrows():
        col1, col2, col3 = st.columns([2, 2, 6])
        with col1:
            st.markdown(f"**🪙 {row['name']} ({row['symbol'].upper()})**")
            st.metric("💵 Preis (USD)", f"${row['current_price']:,.4f}")
        with col2:
            st.metric("📉 24h Veränderung", f"{row['price_change_percentage_24h']:.2f} %")
        with col3:
            if row["price_change_percentage_24h"] > 15:
                signal = "🔴 Überhitzt – Gewinne sichern?"
            elif row["price_change_percentage_24h"] > 5:
                signal = "🟡 Beobachten – mögliche Spitze"
            else:
                signal = "🟢 Ruhig – Halten oder Einstieg"
            st.markdown(f"<div style='background-color:#222;padding:10px;border-radius:8px;'>{signal}</div>", unsafe_allow_html=True)

        st.markdown("---")
