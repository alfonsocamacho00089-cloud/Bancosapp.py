import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Radar de Bancos", page_icon="🏦")
st.title("🏦 Radar de Tasas Bancarias")

def obtener_tasas_bancos():
    # Limpiamos caché para que siempre sea data fresca
    st.cache_data.clear()
    
    # URL de la API que agrupa los bancos
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bancamiga"
    
    try:
        # Usamos tus mismos headers para que no nos bloqueen
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            return res_json['monitors']
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin señal: {e}"

# Se ejecuta automáticamente al cargar
bancos_data = obtener_tasas_bancos()
hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

if isinstance(bancos_data, str): # Si es un error (string)
    st.error(bancos_data)
else:
    # Mostramos éxito y guardamos el archivo JSON para tu HTML
    st.success(f"### ✅ TASAS SINCRONIZADAS AUTOMÁTICAMENTE")
    st.dataframe(bancos_data)
    
    # Guardamos en GitHub para que tu App HTML lo lea
    with open("bancos.json", "w") as f:
        json.dump(bancos_data, f)
    
    st.info("El archivo 'bancos.json' ha sido actualizado en el repositorio.")

st.write(f"🕒 **Última actualización:** {hora_actual}")
