import streamlit as st
import requests
import json

st.set_page_config(page_title="Radar de Bancos", page_icon="🏦")
st.title("🏦 Radar de Tasas Bancarias")

def obtener_bancos():
    # Esta API es la mejor porque separa los bancos del resto
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bancamiga"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data['monitors']
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# Botón para forzar la actualización y el guardado en GitHub
if st.button('🔄 Sincronizar Tasas de Bancos'):
    with st.spinner('Buscando en las bóvedas...'):
        bancos_data = obtener_bancos()
        
        if bancos_data:
            # MAGIA: Guardamos el archivo que tu HTML va a leer
            with open("bancos.json", "w") as f:
                json.dump(bancos_data, f)
            
            st.success("✅ ¡Lista de Bancos actualizada y guardada!")
            
            # Mostramos la tabla para que verifiques los precios
            st.dataframe(bancos_data)
        else:
            st.error("No se pudo recibir información. Intenta de nuevo.")

st.info("Este radar genera el archivo 'bancos.json'. Tu App principal lo leerá desde ahí.")
