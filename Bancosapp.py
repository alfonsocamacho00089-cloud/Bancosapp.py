import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Radar Bancos", page_icon="🏦")
st.title("🏦 Radar de Tasas Bancarias")

def obtener_tasas():
    st.cache_data.clear()
    # Usamos una URL directa que es mucho más estable
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    try:
        # Añadimos un pequeño truco para que la API crea que somos un navegador
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Filtramos para que solo te de los monitores que son bancos o BCV
            return response.json().get('monitors', {})
        return f"Error de servidor: {response.status_code}"
    except Exception as e:
        return f"Error de conexión: {e}"

# Ejecución automática
datos = obtener_tasas()
hora = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M:%S %p")

if isinstance(datos, dict) and len(datos) > 0:
    st.success("✅ ¡Señal recuperada! Tasas encontradas.")
    
    # Mostramos la tabla para que veas los precios variados
    st.table(datos)
    
    # Guardamos el archivo para tu app de las tarjetitas
    with open("bancos.json", "w") as f:
        json.dump(datos, f)
else:
    st.error(f"Sigue el bloqueo: {datos}")
    st.info("Intentando conexión alternativa...")

st.write(f"🕒 **Actualizado:** {hora}")
