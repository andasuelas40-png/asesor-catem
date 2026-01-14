import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Asesor CATEM", page_icon="⚖️", layout="centered", initial_sidebar_state="expanded")

# --- 2. ESTILOS ---
st.markdown("""
    <style>
    h1 { color: #B71C1C !important; text-align: center; }
    .stChatMessage { border-radius: 15px; border: 1px solid #E0E0E0; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🧰 Herramientas")
    if st.button("🗑️ Nueva Consulta", type="primary"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.success("✅ **Sistema Operativo**")
    st.info("⚡ **Modelo:** Flash (Automático)")
    st.warning("⚠️ Demo educativa.")

# --- 4. CONEXIÓN (USANDO EL COMODÍN DE TU LISTA) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ¡AQUÍ ESTÁ LA CLAVE! Usamos el alias genérico de tu lista
    model = genai.GenerativeModel('gemini-flash-latest', system_instruction="""
    Eres el "Asesor Digital CATEM".
    ROL: IA experta en derecho laboral mexicano (LFT).
    TONO: Empático, profesional y firme.
    REGLAS:
    - Di siempre que NO eres abogado humano.
    - Despidos: Advierte NO firmar renuncia.
    - Usa negritas para resaltar claves.
    """)
except Exception as e:
    st.error(f"Error de conexión: {e}")

# --- 5. CHAT ---
st.title("⚖️ Asesor Digital CATEM")
st.markdown("<h3 style='text-align: center; color: #666;'>Tu aliado en la defensa laboral</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.chat_message("assistant").write("¡Hola compañero! 👷 Soy tu Asesor Virtual. ¿Te despidieron o tienes dudas de tu salario? Cuéntame.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu situación..."):
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
                # Si falla, mostramos el mensaje amigable
                st.error("El sistema está saturado. Por favor espera 30 segundos e intenta de nuevo.")
