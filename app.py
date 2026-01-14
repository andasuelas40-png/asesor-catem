import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Asesor CATEM", page_icon="⚖️")

st.title("⚖️ Asesor Digital CATEM")
st.write("Bienvenido compañero. Soy tu asistente virtual para orientación laboral.")

# 2. CONEXIÓN SEGURA (Aquí usará la clave que guardaste, sin mostrarla)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Falta la clave de API. Configúrala en los 'Secrets' de Streamlit.")

# 3. EL CEREBRO (Instrucciones)
sys_instruct = """
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

# 4. CHAT (Memoria)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. INTERACCIÓN
if prompt := st.chat_input("Escribe tu duda aquí..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
