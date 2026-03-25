import streamlit as st
import requests
import json

# Usamos la API que mejor replica el comportamiento de un humano
def obtener_bancos_estilo_binance():
    # Esta es la ruta que trae la tabla informativa del BCV (la de los 555)
    url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar?page=bcv"
    
    # Los headers de "Nivel Pro" que usaste con Binance
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        # Petición limpia
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            monitores = data.get('monitors', {})
            
            # Filtramos solo los bancos que tú quieres mostrar
            bancos_interes = ["Mercantil", "Provincial", "BNC", "Banco de Venezuela"]
            resultados = []
            
            for clave, info in monitores.items():
                if any(b in info['title'] for b in bancos_interes):
                    resultados.append({
                        "banco": info['title'],
                        "precio": info['price'],
                        "update": info.get('last_update', 'Reciente')
                    })
            return resultados
        return None
    except Exception as e:
        return f"Error de conexión: {e}"

# --- MOSTRAR EN TU APP ---
st.subheader("🏦 Tasas Reales de Venta (Bancos)")
data_bancos = obtener_bancos_estilo_binance()

if isinstance(data_bancos, list) and len(data_bancos) > 0:
    st.success("🔥 ¡Data del BCV quebrada con éxito!")
    st.table(data_bancos)
    # Guardamos el archivo para que tu Calculadora lo use
    with open("bancos.json", "w") as f:
        json.dump(data_bancos, f)
else:
    st.error("El BCV sigue resistiendo. Pero como tú dices: si pudimos con Binance, podemos con esto.")
