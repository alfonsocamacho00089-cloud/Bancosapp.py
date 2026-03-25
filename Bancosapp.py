import streamlit as st
import requests

# Configuración visual
st.set_page_config(page_title="Calculadora TuPropina", page_icon="🇻🇪")

st.title("💰 Calculadora TuPropina")
st.write("Tasas oficiales actualizadas directamente del BCV.")

# --- CARGA DE DATOS ---
# REEMPLAZA ESTE LINK con tu enlace RAW de GitHub
URL_JSON = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/bancos.json"

@st.cache_data(ttl=3600) # Guarda los datos por 1 hora para que sea ultra rápido
def obtener_tasas():
    try:
        response = requests.get(URL_JSON)
        data = response.json()
        return data
    except:
        return None

datos = obtener_tasas()

if datos:
    # 1. Crear la lista para el selector
    # Usamos .encode().decode() para limpiar los acentos raros como \u00e9
    opciones_bancos = {item['banco']: float(item['precio']) for item in datos}
    
    # 2. Interfaz de usuario
    banco_elegido = st.selectbox("Selecciona la tasa del Banco:", list(opciones_bancos.keys()))
    tasa_valor = opciones_bancos[banco_elegido]
    
    st.success(f"Tasa de hoy: **{tasa_valor:,.2f} VES**")
    
    st.write("---")
    
    # 3. Campos de cálculo
    col1, col2 = st.columns(2)
    
    with col1:
        usd = st.number_input("Monto en Dólares ($)", min_value=0.0, value=1.0, step=1.0)
    
    with col2:
        bolivares = usd * tasa_valor
        st.metric("Total en Bolívares", f"{bolivares:,.2f} VES")

    st.info(f"💡 Multiplicando ${usd} x {tasa_valor}")

else:
    st.error("⚠️ Error: No se pudo conectar con la base de datos de GitHub.")
    st.info("Asegúrate de que el enlace RAW sea correcto y que el archivo bancos.json no esté vacío.")

st.write("---")
st.caption("Pedro Peres / El Aprendiz - 2026")
