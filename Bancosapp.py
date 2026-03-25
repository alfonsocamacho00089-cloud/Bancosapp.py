import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Radar Bancos Real", page_icon="🏦")
st.title("🏦 Radar de Tasas Bancarias")

def obtener_tasas_reales():
    st.cache_data.clear()
    # Esta URL nos da la lista de TODOS los bancos con precios oficiales
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Aquí vienen los monitores: Banco de Venezuela, Mercantil, BBVA, etc.
            return response.json()['monitors']
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin señal: {e}"

# Se ejecuta solo al abrir
datos_bancos = obtener_tasas_reales()
hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

if isinstance(datos_bancos, list) or isinstance(datos_bancos, dict):
    st.success("✅ ¡Tasas variadas encontradas!")
    
    # Guardamos el JSON para que tu App lo lea y arme las tarjetitas con logos
    with open("bancos.json", "w") as f:
        json.dump(datos_bancos, f)
    
    # Te lo muestro en tabla para que verifiques que los precios NO son iguales
    st.table(datos_bancos)
else:
    st.error(f"Falla de conexión: {datos_bancos}")

st.write(f"🕒 **Última actualización:** {hora_actual}")
