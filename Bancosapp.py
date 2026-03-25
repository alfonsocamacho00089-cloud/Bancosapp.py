import streamlit as st
import requests
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Calculadora TuPropina", page_icon="💰")

st.title("💰 Calculadora TuPropina")
st.subheader("Tasas Oficiales BCV en tiempo real")

# 2. Tu enlace RAW de GitHub (PEGA EL TUYO AQUÍ)
URL_JSON = "[
    {
        "banco": "Banco Nacional de Cr\u00e9dito BNC",
        "precio": "494.9658"
    },
    {
        "banco": "BBVA Provincial",
        "precio": "530.0000"
    },
    {
        "banco": "Banco Activo",
        "precio": "463.5795"
    },
    {
        "banco": "Banco Mercantil",
        "precio": "555.0000"
    },
    {
        "banco": "Banesco",
        "precio": "469.2704"
    },
    {
        "banco": "Otras Instituciones",
        "precio": "508.9179"
    },
    {
        "banco": "Banco Nacional de Cr\u00e9dito BNC",
        "precio": "498.9911"
    },
    {
        "banco": "Bancamiga",
        "precio": "524.8302"
    },
    {
        "banco": "Banesco",
        "precio": "469.1294"
    },
    {
        "banco": "Banco Venezolano de Cr\u00e9dito",
        "precio": "561.0000"
    },
    {
        "banco": "BBVA Provincial",
        "precio": "516.0646"
    },
    {
        "banco": "Otras Instituciones",
        "precio": "501.9376"
    },
    {
        "banco": "Banco Mercantil",
        "precio": "455.4080"
    },
    {
        "banco": "BBVA Provincial",
        "precio": "548.6447"
    },
    {
        "banco": "Banco Nacional de Cr\u00e9dito BNC",
        "precio": "502.4334"
    },
    {
        "banco": "Banco Exterior",
        "precio": "465.9819"
    },
    {
        "banco": "Banesco",
        "precio": "458.9315"
    },
    {
        "banco": "Otras Instituciones",
        "precio": "524.8509"
    },
    {
        "banco": "BBVA Provincial",
        "precio": "518.6748"
    },
    {
        "banco": "Bancamiga",
        "precio": "506.9812"
    },
    {
        "banco": "Banesco",
        "precio": "539.1861"
    },
    {
        "banco": "Banco Mercantil",
        "precio": "545.0000"
    },
    {
        "banco": "Banco Nacional de Cr\u00e9dito BNC",
        "precio": "483.8723"
    },
    {
        "banco": "Otras Instituciones",
        "precio": "488.6116"
    },
    {
        "banco": "Bancamiga",
        "precio": "513.2278"
    }
]"

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
