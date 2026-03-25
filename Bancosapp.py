import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Radar Bancos P2P", page_icon="🏦")
st.title("🏦 Radar de Bancos (Vía Binance)")

def obtener_tasa_por_banco(nombre_banco):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT", "fiat": "VES", "tradeType": "SELL", 
        "bank": [nombre_banco], "rows": 1, "page": 1, "publisherType": "merchant"
    }
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()['data'][0]['adv']['price']
        return "Error"
    except:
        return "N/A"

# --- LISTA DE BANCOS QUE QUEREMOS ---
bancos_a_buscar = ["Banesco", "Mercantil", "BBVA Provincial", "Banco de Venezuela"]
resultados = {}

st.info("Buscando tasas en tiempo real...")

for b in bancos_a_buscar:
    precio = obtener_tasa_por_banco(b)
    resultados[b] = {"title": b, "price": precio}

# --- GUARDADO AUTOMÁTICO ---
with open("bancos.json", "w") as f:
    json.dump(resultados, f)

st.success("✅ Tasas de Binance sincronizadas")
st.table(resultados) # Para que veas los precios claritos

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")
st.write(f"🕒 **Última actualización:** {hora_actual}")
