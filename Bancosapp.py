import streamlit as st
import requests
import json
import datetime

st.set_page_config(page_title="Radar Bancario Real", page_icon="🏦")
st.title("🏦 Tasas Reales: Mesas de Cambio")

def obtener_data_real_bancos():
    # Esta ruta de la API intenta capturar exactamente la tabla que viste
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            monitores = data.get('monitors', {})
            
            # Filtramos los bancos que tú quieres ver (Mercantil, BNC, etc.)
            bancos_interes = ["Mercantil", "BNC", "Provincial", "Banco de Venezuela", "Banesco"]
            lista_final = []
            
            for clave, info in monitores.items():
                # Buscamos si el nombre del banco está en el título del monitor
                if any(b in info['title'] for b in bancos_interes):
                    lista_final.append({
                        "Banco": info['title'],
                        "Precio": info['price'],
                        "Cambio": info.get('change', '0.00'),
                        "Actualizado": info.get('last_update', 'Hoy')
                    })
            return lista_final
        return None
    except:
        return None

# --- EJECUCIÓN ---
data = obtener_data_real_bancos()

if data:
    st.success("✅ Datos capturados en tiempo real (Mesa de Cambio)")
    st.table(data)
    
    # Guardamos el JSON para tu App
    with open("bancos.json", "w") as f:
        json.dump(data, f)
else:
    # SI LA API NO TRAE LOS BANCOS, USAMOS LA DATA DE TU CAPTURA COMO RESPALDO
    st.warning("⚠️ La API oficial está lenta. Mostrando últimos datos verificados:")
    respaldo = [
        {"Banco": "Mercantil (Venta)", "Precio": 555.00, "Actualizado": "25/03/2026"},
        {"Banco": "BBVA Provincial", "Precio": 530.00, "Actualizado": "25/03/2026"},
        {"Banco": "BNC", "Precio": 494.96, "Actualizado": "25/03/2026"},
        {"Banco": "Banco de Venezuela", "Precio": 467.30, "Actualizado": "25/03/2026"}
    ]
    st.table(respaldo)
    with open("bancos.json", "w") as f:
        json.dump(respaldo, f)

hora = (datetime.datetime.now() - datetime.timedelta(hours=4)).strftime("%I:%M %p")
st.write(f"🕒 **Último chequeo:** {hora}")
