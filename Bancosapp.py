import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="TuPropina P2P - Alto", page_icon="📡")
st.title("📡 Antena TuPropina (USDT + Bancos)")

# --- PARTE 1: BINANCE P2P (TU CÓDIGO) ---
def obtener_p2p_alto():
    st.cache_data.clear()
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "SELL", 
        "bank": ["Banesco"],
        "rows": 1,
        "page": 1,
        "publisherType":"merchant"
    }
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['data'][0]['adv']['price']
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin señal: {e}"

precio_alto = obtener_p2p_alto()
hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

if "Error" in str(precio_alto) or "Sin" in str(precio_alto):
    st.error(precio_alto)
else:
    st.success(f"### 🔥 PRECIO USDT: {precio_alto} Bs.")
    st.code(f"VALOR_REAL|{precio_alto}|")
    with open("tasa.txt", "w") as f:
        f.write(str(precio_alto))

st.divider()

# --- PARTE 2: BANCOS (AÑADIDO AUTOMÁTICO) ---
def obtener_bancos():
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bancamiga"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()['monitors']
        return None
    except:
        return None

st.subheader("🏦 Tasas de Bancos")
bancos_data = obtener_bancos()

if bancos_data:
    with open("bancos.json", "w") as f:
        json.dump(bancos_data, f)
    st.success("✅ Tasas de bancos sincronizadas")
    st.dataframe(bancos_data)
else:
    st.warning("⚠️ No se pudo actualizar la lista de bancos (API ocupada)")

st.write(f"🕒 **Última actualización:** {hora_actual}")
