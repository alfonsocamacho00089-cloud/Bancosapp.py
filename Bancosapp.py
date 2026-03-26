import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Antena Bit-Yadio", page_icon="📡")
st.title("📡 Antena: Señal Bit & Yadio")

# --- FUNCIONES DE SEÑAL ---

def obtener_yadio():
    """ Obtiene el precio de Yadio.io (Muy estable) """
    try:
        # Usamos el endpoint específico para USDT
        url = "https://api.yadio.io/json/USDT"
        headers = {"User-Agent": "Mozilla/5.0"} 
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()['USDT']['price']
        return "Error Yadio"
    except:
        return "Sin señal Yadio"

def obtener_bit():
    """ Obtiene el precio de BitYadio """
    try:
        # Endpoint de ticker para el último precio
        url = "https://api.bityadio.com/v1/ticker/usdtves"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            # Asumiendo que la respuesta es un JSON con 'last_price'
            return res.json()['last_price']
        return "Error Bit"
    except:
        return "Sin señal Bit"

# --- EJECUCIÓN Y PANTALLA ---

# Traemos los datos
tasa_yadio = obtener_yadio()
tasa_bit = obtener_bit()

hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

# Diseño de la Antena en Streamlit
col1, col2 = st.columns(2)

with col1:
    st.metric(label="📍 Yadio (USDT)", value=f"{tasa_yadio} Bs")
    
with col2:
    st.metric(label="🪙 BitYadio", value=f"{tasa_bit} Bs")

# --- GUARDADO PARA TU CALCULADORA ---
# Formato compatible: YADIO|BIT
info_txt = f"{tasa_yadio}|{tasa_bit}"

try:
    with open("tasa.txt", "w") as f:
        f.write(info_txt)
    st.success(f"✅ Señal enviada a GitHub: `{info_txt}`")
except Exception as e:
    st.error(f"Fallo al guardar: {e}")

st.write(f"🕒 **Sincronizado a las:** {hora_actual}")
