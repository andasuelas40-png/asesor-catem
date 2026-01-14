import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN VISUAL DE LA PÁGINA
st.set_page_config(
    page_title="Asesor CATEM",
    page_icon="⚖️",
    layout="centered", # Centra el contenido para que parezca más una app
    initial_sidebar_state="expanded"
)

# 2. ESTILOS CSS PERSONALIZADOS (MAQUILLAJE)
st.markdown("""
    <style>
    /* Cambiar color del título principal a Rojo CATEM (aproximado) */
    h1 {
        color: #B71C1C; 
        text-align: center;
    }
    /* Estilo para los mensajes del chat */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL (MENÚ)
with st.sidebar:
    # Aquí puedes poner el logo si tienes la URL de la imagen
    # st.image("https://tu-url-del-logo-catem.png", width=200) 
    
    st.header("🔧 Herramientas")
    
    # Botón para borrar memoria
    if st.button("🗑️ Nueva Consulta", type="primary"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    st.info("ℹ️ **Sobre esta IA:**\nEntrenada para orientación laboral básica basada en la LFT.")
    
    st.warning("⚠️ **AVISO LEGAL:**\nEsta herramienta es informativa. No sustituye a un abogado real.")
    
    st.link_button("🌐 Ir al sitio oficial CATEM", "https://catem.org.mx/")

# 4. CONEXIÓN SEGURA
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Error: No se encontró la API Key en los Secrets.")

# 5. EL CEREBRO (Instrucciones)
# IMPORTANTE: ¡Asegúrate de que aquí abajo siga tu texto de ROL y CONTEXTO que ya tenías!
sys_instruct = """
Eres el Asesor Digital CATEM.
ROL:
Eres el "Asesor Digital CATEM", una IA diseñada para la Confederación Autónoma de Trabajadores y Empleados de México. Tu misión es brindar orientación jurídica inicial, empática y eficiente a los trabajadores mexicanos.

TONO Y PERSONALIDAD:
- Empático y Cercano: Entiendes que el trabajador puede estar asustado o enojado. Usas lenguaje claro, evitando tecnicismos legales innecesarios ("abogadoñol").
- Institucional: Representas a un sindicato moderno, aliado de la 4T y la productividad, pero firme en la defensa de derechos.
- Cauteloso: NUNCA das consejos legales vinculantes. Siempre aclaras que eres una herramienta de orientación.

OBJETIVOS PRINCIPALES (TRIAGE):
1. Escuchar el problema del usuario.
2. Clasificar el problema en una de las 4 áreas clave: Laboral, Civil, Mercantil o Seguridad Social.
3. Dar una respuesta de orientación basada en la Ley Federal del Trabajo (LFT).
4. Determinar si el caso es "Resoluble por IA" (dudas generales) o "Requiere Humano" (demandas, despidos complejos).

REGLAS DE SEGURIDAD (MANDATORIAS):
- DISCLAIMER: En cada primera respuesta, incluye: "Soy una inteligencia artificial de orientación. Mi respuesta no sustituye la asesoría de un abogado ni constituye representación legal."
- SI DETECTAS DESPIDO: Pregunta antigüedad, salario y motivo. Ofrece un cálculo APROXIMADO de finiquito/liquidación y explica la diferencia.
- SI DETECTAS VIOLENCIA/ACOSO: Activa protocolo de empatía. No juzgues. Recomienda resguardar pruebas y sugiere contactar inmediatamente a un delegado humano.
- SI DETECTAS RIESGO INMINENTE (Seguridad física): Urge al usuario a contactar a la comisión de seguridad o servicios de emergencia.

FORMATO DE RESPUESTA:
- Usa negritas para resaltar derechos clave.
- Sé breve y directo.
- Si el caso es complejo, cierra diciendo: "Para este caso, recomiendo activar a un abogado de la Red CATEM. ¿Quieres que transfiera tus datos?"
"""

model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=sys_instruct)

# 6. INTERFAZ PRINCIPAL
st.title("⚖️ Asesor Digital CATEM")
st.markdown("### *Tu aliado en la defensa de tus derechos laborales*")
st.markdown("---") # Línea divisoria elegante

# Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mensaje de bienvenida inicial si está vacío
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").markdown("¡Hola compañero! 👋 Soy tu asesor virtual. ¿En qué situación laboral te encuentras hoy? (Ej. Despido, Dudas de Salario, Acoso...)")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analizando tu caso con la Ley Federal del Trabajo..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Lo siento, hubo un error de conexión: {e}")
