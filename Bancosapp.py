import streamlit as st
import requests
import datetime

st.set_page_config(page_title="TuPropina P2P - Alto", page_icon="📡")
st.title("📡 Antena P2P - Señal Limpia")

# --- TUS FUNCIONES ---

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()['data'][0]['adv']['price']
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin señal: {e}"

def obtener_yadio():
    try:
        url = "https://api.yadio.io/json/USDT"
        res = requests.get(url, timeout=10)
        return res.json()['USDT']['price']
    except:
        return "N/A"

def obtener_bit():
    try:
        url = "https://api.bityadio.com/v1/ticker/usdtves"
        res = requests.get(url, timeout=10)
        return res.json()['last_price']
    except:
        return "N/A"

# --- LÓGICA DE PANTALLA ---

precio_alto = obtener_p2p_alto()
p_yadio = obtener_yadio()
p_bit = obtener_bit()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

if "Error" in str(precio_alto) or "Sin" in str(precio_alto):
    st.error(precio_alto)
else:
    st.balloons()
    st.success(f"### 🔥 BINANCE (SELL): {precio_alto} Bs.")
    
    # Mostramos las nuevas tasas en pequeño abajo
    col1, col2 = st.columns(2)
    col1.metric("Yadio", f"{p_yadio} Bs")
    col2.metric("BitYadio", f"{p_bit} Bs")

    # Esto es lo que lee tu otra app (Mantenemos el formato original)
    # Si quieres enviar las 3, puedes usar: f"VALOR_REAL|{precio_alto}|{p_yadio}|{p_bit}|"
    st.code(f"VALOR_REAL|{precio_alto}|")

st.info("Ahora estás viendo la tasa de 'Venta', que siempre es un poco más alta que la de 'Compra'.")

# Guardado en el archivo (Mantenemos tu lógica de tasa.txt)
with open("tasa.txt", "w") as f:
    f.write(f"{precio_alto}|{p_yadio}|{p_bit}")

st.success(f"Tasas sincronizadas: {precio_alto} | {p_yadio} | {p_bit}")
st.write(f"🕒 **Última actualización:** {hora_actual}")
