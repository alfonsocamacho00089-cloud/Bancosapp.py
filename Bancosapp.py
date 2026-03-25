import streamlit as st
import requests
import json
import datetime

st.set_page_config(page_title="Radar Bancario Real", page_icon="🏦")
st.title("🏦 Precios de Venta: Bancos (Real)")

def obtener_data_viva():
    # Usamos el endpoint que agrupa los bancos de la tabla del BCV
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    try:
        # Nos identificamos como un navegador normal
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            monitores = response.json().get('monitors', {})
            
            # Filtramos exactamente los que viste en tu captura
            bancos_clave = ["Mercantil", "Provincial", "BNC", "Banco de Venezuela", "Banesco"]
            lista_final = []
            
            for clave, info in monitores.items():
                # Si el banco está en nuestra lista, lo guardamos
                if any(b in info['title'] for b in bancos_clave):
                    lista_final.append({
                        "banco": info['title'],
                        "precio": info['price'],
                        "actualizado": info.get('last_update', 'Hoy')
                    })
            return lista_final
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin conexión: {e}"

# --- ACCIÓN ---
data = obtener_data_viva()

if isinstance(data, list) and len(data) > 0:
    st.success("✅ ¡Data real obtenida!")
    st.table(data) # Aquí verás los 555 o el que esté vigente
    
    # Guardamos el JSON automático
    with open("bancos.json", "w") as f:
        json.dump(data, f)
else:
    st.error("📡 El servidor del BCV está rechazando la conexión del robot.")
    st.info("Pedro, si sale este error, es porque el BCV bloqueó la IP. No pierdas tiempo: en ese caso toca usar un 'Scraper' con proxy o esperar a que la API refresque.")

st.write(f"🕒 Sincronizado: {datetime.datetime.now().strftime('%I:%M %p')}")
