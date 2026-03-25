import streamlit as st
import requests
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Calculadora TuPropina", page_icon="💰")

st.title("💰 Calculadora TuPropina")
st.subheader("Tasas Oficiales BCV en tiempo real")

# 2. Tu enlace RAW de GitHub (PEGA EL TUYO AQUÍ)
URL_JSON = "TU_ENLACE_RAW_AQUI"

@st.cache_data(ttl=600) # Esto hace que la app sea veloz y no cargue a cada rato
def cargar_datos():
    try:
        response = requests.get(URL_JSON)
        return response.json()
    except:
        return []

datos = cargar_datos()

if datos:
    # Creamos una lista de nombres de bancos para el selector
    nombres_bancos = [item['banco'] for item in datos]
    
    # Selector de Banco
    banco_seleccionado = st.selectbox("Selecciona el Banco:", nombres_bancos)
    
    # Buscar el precio del banco elegido
    precio_dolar = 0
    for item in datos:
        if item['banco'] == banco_seleccionado:
            precio_dolar = float(item['precio'])
            break

    st.info(f"Tasa seleccionada: **{precio_dolar} VES**")

    # 3. La Calculadora
    col1, col2 = st.columns(2)
    
    with col1:
        monto_usd = st.number_input("Monto en Dólares ($):", min_value=0.0, value=1.0)
    
    with col2:
        resultado = monto_usd * precio_dolar
        st.metric("Total en Bolívares (VES):", f"{resultado:,.2f}")

    st.write("---")
    st.caption("Datos actualizados automáticamente desde el BCV.")

else:
    st.error("No se pudieron cargar los datos. Verifica el enlace de GitHub.")
