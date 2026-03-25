import streamlit as st
import pandas as pd
import json
import datetime

st.set_page_config(page_title="Radar Bancario Real", page_icon="📈")
st.title("📈 Tasas Reales de Venta (Bancos)")

def extraer_tabla_bcv():
    url = "https://www.bcv.org.ve/tasas-informativas-sistema-bancario"
    try:
        # Intentamos leer todas las tablas de esa página
        tablas = pd.read_html(url, decimal=',', thousands='.')
        
        # La primera tabla suele ser la de los bancos
        df = tablas[0]
        
        # Limpiamos los nombres de las columnas (Institución, Compra, Venta)
        df.columns = ['Banco', 'Compra', 'Venta', 'Fecha']
        
        # Filtramos solo los que te interesan para que no sea una lista gigante
        bancos_web = ["MERCANTIL", "BANCO NACIONAL DE CRÉDITO", "BBVA PROVINCIAL", "BANCO DE VENEZUELA"]
        df_filtrado = df[df['Banco'].str.contains('|'.join(bancos_web), case=False, na=False)]
        
        return df_filtrado.to_dict(orient='records')
    except Exception as e:
        return f"Error leyendo el BCV: {e}"

# --- PROCESO ---
data_real = extraer_tabla_bcv()

if isinstance(data_real, list):
    st.success("✅ ¡Data capturada directamente del BCV!")
    st.table(data_real)
    
    # Guardamos el JSON para tu botón profesional
    with open("bancos.json", "w") as f:
        json.dump(data_real, f)
else:
    st.error("El BCV bloqueó la conexión automática. Intentando vía API de respaldo...")
    # Aquí podrías poner el código de la API que ya tienes como plan B
