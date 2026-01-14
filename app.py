import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(
    page_title="Asesor CATEM",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. ESTILOS (ROJO CATEM)
st.markdown("""
    <style>
    h1 { color: #B71C1C !important; text-align: center; font-weight: bold; }
    .stChatMessage { border-radius: 15px; border: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.header("🧰 Herramientas")
    if st.button("🗑️ Borrar Historial", type="primary"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("🤖 **Modelo:** Gemini 1.5 Flash")
    st.warning("⚠️ Demo educativa. No es abogacía real.")

# 4. CONEXIÓN (CORREGIDA)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # --- CAMBIO CLAVE: Usamos 'gemini-1.5-flash-latest' ---
    model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction="""
Eres el Asesor Digital CATEM.
ROL: IA experta en derecho laboral mexicano (LFT).
TONO: Empático, firme y profesional.
OBJETIVO: Orientar sobre despidos, salarios y prestaciones.
REGLAS:
- Aclara que NO eres abogado humano.
- Despido: Sugiere NO firmar renuncia y calcular finiquito.
- Usa negritas para resaltar derechos.
""")
except Exception as e:
    st.error(f"Error de conexión: {e}")

# 5. CHAT
st.title("⚖️ Asesor Digital CATEM")
st.markdown("<h3 style='text-align: center; color: #555;'>Tu aliado en la defensa laboral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Bienvenida
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").write("¡Hola compañero! 👷 Soy tu Asesor Virtual. ¿Te despidieron injustificadamente? Cuéntame.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu problema aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
