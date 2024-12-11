import streamlit as st
import pandas as pd

# Lista de usuarios administradores, en este caso solo uno
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"  # Contraseña simple para propósito de ejemplo
}

def autenticar_admin():
    st.subheader("Autenticación de Administrador")
    
    # Pedir credenciales
    username = st.text_input("Nombre de usuario", type="password")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar sesión"):
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            st.success("Autenticación exitosa!")
            st.session_state.pagina_actual = "descargar_csv"  # Cambiar a la página de descarga
            st.rerun()  # Recargar la página para mostrar la pantalla correcta
        else:
            st.error("Nombre de usuario o contraseña incorrectos")
    
    if st.button("<-", use_container_width=True):
        st.session_state.pagina_actual = 'inicio'
        st.rerun()

def pagina_descarga():
    """Pantalla que permite descargar el archivo respuestas.csv"""
    st.subheader("Descargar CSV")
    
    # Ruta del archivo
    csv_path = "data/respuestas_encuesta.csv"
    
    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            csv_data = file.read()

        st.download_button(
            label="Descargar archivo CSV",
            data=csv_data,
            file_name="respuestas_encuesta.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.error("El archivo respuestas.csv no se encontró. Por favor, verifica su existencia en la carpeta data.")
    
    # Botón para volver al inicio
    if st.button("<-", use_container_width=True):
        st.session_state.pagina_actual = 'inicio'
        st.rerun()