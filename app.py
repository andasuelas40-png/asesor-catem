import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Asesor CATEM",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS VISUALES (ROJO CATEM) ---
st.markdown("""
    <style>
    /* Título Principal Rojo */
    h1 {
        color: #B71C1C !important;
        text-align: center;
        font-weight: 800;
    }
    /* Subtítulo Gris */
    .subtitle {
        text-align: center;
        color: #616161;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    /* Chat con bordes suaves */
    .stChatMessage {
        border-radius: 15px;
        border: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. BARRA LATERAL (HERRAMIENTAS) ---
with st.sidebar:
    st.header("🧰 Herramientas")
    
    # Botón para reiniciar
    if st.button("🗑️ Nueva Consulta", type="primary"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    st.success("✅ **Sistema Operativo**")
    st.info("🤖 **Modelo:** Gemini 1.5 Flash")
    st.warning("⚠️ **Aviso:** Herramienta de orientación. No sustituye asesoría legal profesional.")

# --- 4. CEREBRO IA (CONEXIÓN SEGURA) ---
try:
    # Configuración de la llave
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # DEFINICIÓN DEL MODELO (VERSIÓN ESTÁNDAR)
    # Usamos 'gemini-1.5-flash' sin sufijos raros para máxima compatibilidad
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="""
    Eres el "Asesor Digital CATEM".
    ROL:
    Eres una IA experta en derecho laboral mexicano diseñada para la Confederación Autónoma de Trabajadores y Empleados de México.
    
    TONO:
    - Empático: Entiendes la preocupación del trabajador.
    - Profesional: Basado estrictamente en la Ley Federal del Trabajo (LFT).
    - Firme: Defiendes los derechos laborales sin ser agresivo.
    
    REGLAS DE ORO:
    1. DISCLAIMER: Siempre inicia diciendo que eres una IA de orientación y no un abogado humano.
    2. DESPIDOS: Si te dicen "me despidieron", advierte INMEDIATAMENTE: "No firmes nada si te ofrecen menos de lo justo o una renuncia voluntaria".
    3. CÁLCULOS: Si piden cuánto les toca, explica la diferencia entre Finiquito (renuncia) y Liquidación (despido injustificado - 3 meses + 20 días).
    4. FORMATO: Usa **negritas** para resaltar conceptos clave.
    """)

except Exception as e:
    st.error(f"⚠️ Error de conexión con Google: {e}")

# --- 5. INTERFAZ DE CHAT ---
st.title("⚖️ Asesor Digital CATEM")
st.markdown('<div class="subtitle">Tu aliado en la defensa de tus derechos laborales</div>', unsafe_allow_html=True)

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mensaje de bienvenida automático
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").write("¡Hola compañero! 👷 Soy tu Asesor Virtual CATEM. ¿En qué puedo ayudarte hoy? (Ej. Despido injustificado, dudas de aguinaldo, acoso laboral...)")

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar input del usuario
if prompt := st.chat_input("Escribe tu situación aquí..."):
    # Guardar y mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta IA
    with st.chat_message("assistant"):
        with st.spinner("Consultando la Ley Federal del Trabajo..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")
