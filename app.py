import os
from openai import OpenAI
import streamlit as st

# Configurar la clave API de OpenAI usando una variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Verificar que la clave API esté configurada
if not api_key:
    st.error("La clave API de OpenAI no está configurada. Por favor, configura la variable de entorno OPENAI_API_KEY.")
    st.stop()

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=api_key)

# Título de la aplicación
st.title("Consultoría para Egresados")

# Inicializar el estado de la aplicación
if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""
if "respuesta" not in st.session_state:
    st.session_state.respuesta = ""

# Función para consultar OpenAI
def consultar_openai(pregunta):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": pregunta}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ocurrió un error al comunicarse con OpenAI: {str(e)}")
        st.stop()

# Entrada de texto para la pregunta
pregunta = st.text_input("Escribe tu pregunta:", value=st.session_state.pregunta)

# Botón para enviar la pregunta
if st.button("Enviar"):
    if pregunta.strip() == "":
        st.warning("Por favor, ingresa una pregunta.")
    else:
        # Guardar la pregunta en el estado de la sesión
        st.session_state.pregunta = pregunta
        # Mostrar un spinner mientras se procesa la respuesta
        with st.spinner("Procesando tu pregunta..."):
            respuesta = consultar_openai(pregunta)
        # Guardar la respuesta en el estado de la sesión
        st.session_state.respuesta = respuesta
        st.success("Respuesta recibida:")
        st.write(respuesta)

# Botón para borrar la pregunta y la respuesta
if st.button("Borrar"):
    st.session_state.pregunta = ""
    st.session_state.respuesta = ""
    st.rerun()  # Reinicia la interfaz

# Mostrar la respuesta almacenada en el estado de la sesión
if st.session_state.respuesta:
    st.success("Respuesta recibida:")
    st.write(st.session_state.respuesta)