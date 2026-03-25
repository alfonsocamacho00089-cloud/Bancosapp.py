import streamlit as st
import requests
import json
import datetime

st.set_page_config(page_title="Radar Bancario Real", page_icon="🏦")
st.title("🏦 Tasa de Venta Real (Bancos)")

def obtener_data_viva():
    # Esta URL nos sirve de puente para saltar el bloqueo del BCV
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    # Usamos los headers que me pasaste para parecer un humano en Windows
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        # En este caso usamos GET porque estamos pidiendo información, no enviándola
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            monitores = response.json().get('monitors', {})
            
            # Filtramos exactamente los bancos que viste en tu captura
            bancos_clave = ["Mercantil", "Provincial", "BNC", "Banco de Venezuela", "Banesco"]
            lista_final = []
            
            for clave, info in monitores.items():
                if any(b in info['title'] for b in bancos_clave):
                    lista_final.append({
                        "banco": info['title'],
                        "precio": info['price'],
                        "actualizado": info.get('last_update', 'Hoy')
                    })
            return lista_final
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Sin señal: {e}"

# --- EJECUCIÓN ---
data = obtener_data_viva()

if isinstance(data, list) and len(data) > 0:
    st.success("✅ ¡Data real obtenida con éxito!")
    st.table(data) # Aquí deberían aparecer tus 555, 530, etc.
    
    # Guardamos el JSON para tu App
    with open("bancos.json", "w") as f:
        json.dump(data, f)
else:
    st.error("📡 El BCV sigue bloqueando la IP del servidor.")
    st.info("Pedro, si después de este código sigue saliendo error, es porque el servidor de Streamlit está 'marcado'. En ese caso, la única forma de terminar hoy es dejar los datos de respaldo fijos para que tu App funcione.")

st.write(f"🕒 Sincronizado: {datetime.datetime.now().strftime('%I:%M %p')}")
