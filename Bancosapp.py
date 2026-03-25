import streamlit as st
import requests
import datetime
import json

st.set_page_config(page_title="Dólar Digital Bancario", page_icon="🏦")
st.title("🏦 Tasa de Venta: Dólar Bancario")

def obtener_dolar_bancario():
    st.cache_data.clear()
    # Esta API nos da el precio al que los bancos VENDEN el dólar
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            monitores = response.json().get('monitors', {})
            # Filtramos para que solo veas los bancos que venden dólares digitales
            bancos_interes = ["Banco de Venezuela", "Banesco", "Mercantil", "BBVA Provincial"]
            
            lista_filtrada = []
            for clave, info in monitores.items():
                if any(banco in info['title'] for banco in bancos_interes):
                    lista_filtrada.append({
                        "banco": info['title'],
                        "precio": info['price'],
                        "actualizado": info['last_update']
                    })
            return lista_filtrada
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin señal: {e}"

# Ejecución automática
data_bancos = obtener_dolar_bancario()
hora_actual = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M %p")

if isinstance(data_bancos, list) and len(data_bancos) > 0:
    st.success(f"✅ Data de Dólar Digital obtenida ({hora_actual})")
    
    # Mostramos la tabla con los precios de venta (tipo 51.50 como dijiste)
    st.table(data_bancos)
    
    # Guardamos el JSON para que tu App lo use
    with open("bancos.json", "w") as f:
        json.dump(data_bancos, f)
else:
    st.error("No se pudo conectar con la tasa bancaria. Reintentando...")

st.info("Esta es la tasa oficial de venta en los portales bancarios para cuentas custodia.")
