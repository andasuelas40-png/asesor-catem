import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL DE LA PÁGINA
st.set_page_config(
    page_title="Asesor CATEM",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MAQUILLAJE (CSS FORZADO)
st.markdown("""
    <style>
    /* Forzar el color rojo en el título */
    h1 {
        color: #B71C1C !important;
        text-align: center;
        font-weight: bold;
    }
    /* Fondo suave para el chat */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Estilo para los mensajes */
    .stChatMessage {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL (LOGO Y HERRAMIENTAS)
with st.sidebar:
    # Si tienes un logo, descomenta la linea de abajo y pon el link
    # st.image("https://catem.org.mx/wp-content/uploads/2023/10/logo-catem.png", width=200)
    
    st.header("🧰 Herramientas")
    
    if st.button("🗑️ Borrar Historial", type="primary"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.success("✅ **Sistema en Línea**")
    st.info("🤖 **Modelo:** Gemini 1.5 Flash\n(Optimizado para velocidad)")
    st.warning("⚠️ **Nota:** Esta es una demo educativa. No es asesoría legal vinculante.")

# 4. CONEXIÓN (CORREGIDA PARA EVITAR ERROR 404)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # CAMBIO IMPORTANTE: Usamos 'gemini-1.5-flash' que es más compatible y rápido
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="""
Eres el Asesor Digital CATEM.
ROL:
Eres una IA experta en derecho laboral mexicano diseñada para la CATEM.
TONO: Empático, profesional y firme en la defensa de derechos.
OBJETIVO: Orientar sobre despidos, salarios y prestaciones según la LFT.
REGLAS:
- Siempre inicia aclarando que NO eres abogado humano.
- Si detectas despido injustificado, sugiere NO firmar renuncia.
- Si detectas violencia, recomienda acudir al sindicato.
- Usa negritas para resaltar conceptos clave.
""")
except Exception as e:
    st.error(f"⚠️ Error de configuración: {e}")

# 5. INTERFAZ DE CHAT
st.title("⚖️ Asesor Digital CATEM")
st.markdown("<h3 style='text-align: center; color: #666;'>Tu aliado en la defensa laboral</h3>", unsafe_allow_html=True)
st.divider()

# Inicializar memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mensaje de bienvenida
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").write("¡Hola compañero! 👷 Soy tu Asesor Virtual CATEM. ¿Te despidieron, tienes dudas de tu aguinaldo o sufres acoso? Cuéntame para ayudarte.")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar input
if prompt := st.chat_input("Escribe aquí tu situación..."):
    # Usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta IA
    with st.chat_message("assistant"):
        with st.spinner("Consultando la Ley Federal del Trabajo..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Error de conexión: {e}")
