import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Diagnóstico", page_icon="🔧")
st.title("🔧 Diagnóstico de Conexión")

try:
    # 1. Configurar Llave
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.write("✅ Llave API detectada.")

    # 2. Listar Modelos Disponibles
    st.write("🔍 Buscando modelos disponibles para tu cuenta...")
    
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"Modelo disponible: {m.name}")
            found_any = True
            
    if not found_any:
        st.error("❌ No se encontraron modelos. Tu API Key podría tener permisos limitados.")

except Exception as e:
    st.error(f"❌ Error Grave: {e}")
    st.info("💡 Pista: Verifica que en 'Advanced Settings' de Streamlit no haya espacios extra en tu clave.")
