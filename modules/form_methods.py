import csv
import streamlit as st
import datetime
from modules.admin_methods import *

def pagina_inicio():
    st.title("¡Bienvenido al Sistema de Encuesta Personal!")
    st.divider()
    st.write("Seleccione una opción del menú para comenzar a llenar la encuesta.")
    st.image("assets/image.png", caption="Complete su encuesta", use_container_width=True)
    
    if st.button("  Continuar ->  ", use_container_width=True):
        st.session_state.pagina_actual = 'informacion_personal'
        st.rerun()
    
    elif st.button("LogIn"):
        st.session_state.pagina_actual = 'autenticacion'  # Cambiar el estado a 'autenticacion'
        st.rerun()  # Recargar la página para mostrar la pantalla de login

def informacion_personal():
    st.subheader("Información Personal")
    st.divider()

    # Cargar respuestas guardadas si existen
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('informacion_personal', {})

    # Campos de texto
    nombres = st.text_input("Nombres", value=respuestas_guardadas.get("nombres", ""))
    apodo = st.text_input("Apodo", value=respuestas_guardadas.get("apodo", ""))
    apellido = st.text_input("Apellidos", value=respuestas_guardadas.get("apellido", ""))
    edad = st.text_input("Edad", value=respuestas_guardadas.get("edad", ""))

    # Selección de género con opción para escribir directamente
    genero_opciones = ["Masculino", "Femenino"]
    genero = st.radio(
        "Género",
        options=genero_opciones + ["Especificar otro"],
        index=(genero_opciones + ["Especificar otro"]).index(
            respuestas_guardadas.get("genero", "Masculino")
        ) if respuestas_guardadas.get("genero", "Masculino") in genero_opciones
        else len(genero_opciones)  # Índice para "Especificar otro"
    )

    if genero == "Especificar otro":
        genero = st.text_input("Especifica tu género", value=respuestas_guardadas.get("genero", ""))

    # Fecha de nacimiento
    fecha_nacimiento = st.date_input(
        "Fecha de Nacimiento",
        value=respuestas_guardadas.get("fecha_nacimiento", None)
    )

    # Botón para guardar la información
    if st.button("Guardar"):
        if nombres and apodo and apellido and edad and genero and fecha_nacimiento:
            try:
                # Guardar las respuestas en el estado de la sesión
                st.session_state.respuestas_guardadas['informacion_personal'] = {
                    "nombres": nombres,
                    "apodo": apodo,
                    "apellido": apellido,
                    "edad": edad,
                    "genero": genero,
                    "fecha_nacimiento": str(fecha_nacimiento)
                }
                st.success("Información Personal Guardada")

                # Cambiar a la siguiente página
                st.session_state.pagina_actual = 'contacto'
                st.rerun()
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")

def contacto(): 
    st.subheader("Información de Contacto")
    st.divider()
    
    # Obtén los datos guardados del estado de sesión
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('contacto', {})
    
    # Campos de entrada
    telefono = st.text_input("Teléfono", value=respuestas_guardadas.get("telefono", ""))
    correo = st.text_input("Correo Electrónico", value=respuestas_guardadas.get("correo", ""))
    
    # Multiselección para redes sociales
    redes_sociales = st.multiselect(
        "Redes Sociales",
        options=["Facebook", "Twitter", "Instagram", "WhatsApp", "TikTok", "Otras"],  # Opciones posibles
        default=respuestas_guardadas.get("redes_sociales", [])  # Valor predeterminado como lista
    )
    
    direccion = st.text_input("Dirección", value=respuestas_guardadas.get("direccion", ""))
    distrito = st.text_input("Distrito", value=respuestas_guardadas.get("distrito", ""))
    provincia = st.text_input("Provincia", value=respuestas_guardadas.get("provincia", ""))
    departamento = st.text_input("Departamento", value=respuestas_guardadas.get("departamento", ""))
    
    # Botón para guardar los datos
    if st.button("Guardar"):
        # Validación de los campos
        if telefono and correo and redes_sociales and direccion and distrito and provincia and departamento:
            try:
                # Guardar en el estado de sesión
                st.session_state.respuestas_guardadas['contacto'] = {
                    "telefono": telefono,
                    "correo": correo,
                    "redes_sociales": redes_sociales,
                    "direccion": direccion,
                    "distrito": distrito,
                    "provincia": provincia,
                    "departamento": departamento
                }
                st.success("Información de Contacto Guardada")
                
                # Navegar a la siguiente página
                st.session_state.pagina_actual = 'nivel_socioeconomico'
                st.rerun()  # Recargar para mostrar la siguiente página
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")

def nivel_socioeconomico():
    st.subheader("Nivel Socioeconómico")
    st.divider()

    # Recuperar respuestas previas
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('nivel_socioeconomico', {})

    # Pregunta si actualmente estudia
    actualmente_estudia = st.radio(
        "¿Actualmente estudias?",
        ["No", "Sí"],
        index=["Sí", "No"].index(respuestas_guardadas.get("actualmente_estudia", "Sí"))
    )

    # Si responde "Sí", mostrar opciones relacionadas con nivel educativo
    if actualmente_estudia == "Sí":
        nivel_educativo = st.selectbox(
            "Nivel Educativo",
            ["Primaria", "Secundaria", "Técnico", "Universidad", "Otro"],
            index=["Primaria", "Secundaria", "Técnico", "Universidad", "Otro"].index(respuestas_guardadas.get("nivel_educativo", "Primaria"))
        )

        # Si selecciona "Universidad", mostrar campos adicionales
        if nivel_educativo == "Universidad":
            nombre_universidad = st.text_input(
                "Nombre de la Universidad",
                value=respuestas_guardadas.get("nombre_universidad", "")
            )
            escuela_profesional = st.text_input(
                "Escuela Profesional",
                value=respuestas_guardadas.get("escuela_profesional", "")
            )
            semestre_academico = st.text_input(
                "Semestre Académico",
                value=respuestas_guardadas.get("semestre_academico", "")
            )
    else:
        nivel_educativo = None
        nombre_universidad = None
        escuela_profesional = None
        semestre_academico = None

    # Información laboral
    st.subheader("Información Laboral")
    actualmente_empleado = st.radio(
        "¿Actualmente empleado?",
        ["Sí", "No"],
        index=["Sí", "No"].index(respuestas_guardadas.get("actualmente_empleado", "Sí"))
    )

    # Si responde "Sí", mostrar campos relacionados con empleo
    if actualmente_empleado == "Sí":
        tipo_empleo = st.radio(
            "Tipo de empleo",
            ["Tiempo completo", "Tiempo parcial"],
            index=["Tiempo completo", "Tiempo parcial"].index(respuestas_guardadas.get("tipo_empleo", "Tiempo completo"))
        )
        ingreso_mensual = st.text_input(
            "Ingreso Mensual",
            value=respuestas_guardadas.get("ingreso_mensual", "")
        )
    else:
        tipo_empleo = None
        ingreso_mensual = None

    # Botón para guardar datos
    if st.button("Guardar Nivel Socioeconómico y Laboral"):
        # Validación básica
        if (
            actualmente_estudia == "No" or 
            (nivel_educativo and 
            (nivel_educativo != "Universidad" or (nombre_universidad and escuela_profesional and semestre_academico)))
        ) and (
            actualmente_empleado == "No" or (tipo_empleo and ingreso_mensual)
        ):
            # Guardar en session_state
            st.session_state.respuestas_guardadas['nivel_socioeconomico'] = {
                "actualmente_estudia": actualmente_estudia,
                "nivel_educativo": nivel_educativo,
                "nombre_universidad": nombre_universidad,
                "escuela_profesional": escuela_profesional,
                "semestre_academico": semestre_academico,
                "actualmente_empleado": actualmente_empleado,
                "tipo_empleo": tipo_empleo,
                "ingreso_mensual": ingreso_mensual,
            }
            st.success("Nivel Socioeconómico y Laboral Guardado")
            st.session_state.pagina_actual = 'situacion_sentimental'
            st.rerun()
        else:
            st.error("Por favor, complete todos los campos necesarios.")

def situacion_sentimental(): 
    st.subheader("Situación Sentimental")
    st.divider()

    # Recuperar respuestas previas
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('situacion_sentimental', {})

    # Preguntar si tiene pareja
    tiene_pareja = st.radio(
        "¿Tienes pareja?", 
        ["Sí", "No"], 
        index=["Sí", "No"].index(respuestas_guardadas.get("tiene_pareja", "No"))
    )

    # Cambiar a radio para estado civil con las opciones Soltero, Casado, Divorciado
    estado_civil = st.radio(
        "Estado Civil", 
        ["Soltero", "Casado", "Divorciado"], 
        index=["Soltero", "Casado", "Divorciado"].index(respuestas_guardadas.get("estado_civil", "Soltero"))
    )

    # Preguntar si tiene hijos
    tiene_hijos = st.radio(
        "¿Tienes hijos?", 
        ["Sí", "No"], 
        index=["Sí", "No"].index(respuestas_guardadas.get("tiene_hijos", "No"))
    )

    # Botón para guardar la información
    if st.button("Guardar Situación Sentimental"):
        # Validación de que los campos no estén vacíos
        if tiene_pareja and estado_civil and tiene_hijos:
            try:
                # Guardar respuestas en session_state
                st.session_state.respuestas_guardadas['situacion_sentimental'] = {
                    "tiene_pareja": tiene_pareja,
                    "estado_civil": estado_civil,
                    "tiene_hijos": tiene_hijos
                }
                st.success("Situación Sentimental Guardada")
                st.session_state.pagina_actual = 'salud_y_bienestar'
                st.rerun()
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")

def salud_y_bienestar(): 
    st.subheader("Salud y Bienestar")
    st.divider()
    
    # Recuperar respuestas previas
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('salud_y_bienestar', {})

    # Preguntar si padece alguna enfermedad crónica
    padece_enfermedad = st.radio(
        "¿Padeces alguna enfermedad crónica?", 
        ["No", "Sí"], 
        index=["Sí", "No"].index(respuestas_guardadas.get("padece_enfermedad", "No"))
    )

    # Mostrar un campo de texto para la enfermedad si la respuesta es Sí
    if padece_enfermedad == "Sí":
        enfermedad = st.text_input("¿Cuál es la enfermedad?", value=respuestas_guardadas.get("enfermedad", ""))
    else:
        enfermedad = ""

    # Preguntar sobre la actividad física semanal
    actividad_fisica = st.radio(
        "Actividad física semanal", 
        ["0", "1-2", "3-4", "5+"], 
        index=["0", "1-2", "3-4", "5+"].index(respuestas_guardadas.get("actividad_fisica", "0"))
    )

    # Botón para guardar la información
    if st.button("Guardar Salud y Bienestar"):
        # Validación de que los campos no estén vacíos
        if padece_enfermedad and actividad_fisica:
            try:
                # Guardar respuestas en session_state
                st.session_state.respuestas_guardadas['salud_y_bienestar'] = {
                    "padece_enfermedad": padece_enfermedad,
                    "enfermedad": enfermedad,  # Guardar el valor de la enfermedad si se ha escrito
                    "actividad_fisica": actividad_fisica
                }
                st.success("Salud y Bienestar Guardada")

                # Navegar a la siguiente página
                st.session_state.pagina_actual = 'habitos_estilo_de_vida'
                st.rerun() 
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")

def habitos_estilo_de_vida():
    st.subheader("Hábitos y Estilo de Vida")
    st.divider()

    respuestas_guardadas = st.session_state.respuestas_guardadas.get('habitos_estilo_de_vida', {})

    # Pregunta sobre el consumo de tabaco
    fuma = st.radio("¿Fumas?", ["Sí", "No"], index=["Sí", "No"].index(respuestas_guardadas.get("fuma", "No")))

    # Pregunta sobre el consumo de alcohol
    toma_alcohol = st.radio("¿Tomas bebidas alcohólicas?", ["Sí", "No"], index=["Sí", "No"].index(respuestas_guardadas.get("toma_alcohol", "No")))

    # Pregunta sobre actividades recreativas
    actividades_recreativas = st.radio(
        "¿Haces actividades recreativas?", 
        ["No", "Sí"], 
        index=["Sí", "No"].index(respuestas_guardadas.get("actividades_recreativas", "No"))
    )

    # Si la respuesta a actividades recreativas es 'Sí', mostrar un campo de texto
    if actividades_recreativas == "Sí":
        actividades = st.text_input("¿Qué actividades recreativas realizas?", value=respuestas_guardadas.get("actividades", ""))
    
    # Botón para guardar los datos
    if st.button("Guardar Hábitos y Estilo de Vida"):
        # Validación de que todos los campos estén completos
        if fuma and toma_alcohol and actividades_recreativas:
            try:
                # Guardar las respuestas en session_state
                st.session_state.respuestas_guardadas['habitos_estilo_de_vida'] = {
                    "fuma": fuma,
                    "toma_alcohol": toma_alcohol,
                    "actividades_recreativas": actividades_recreativas,
                    "actividades": actividades if actividades_recreativas == "Sí" else ""  # Guardar las actividades si la respuesta fue 'Sí'
                }
                st.success("Hábitos y Estilo de Vida Guardados")

                st.session_state.pagina_actual = 'opiniones_o_interes'
                st.rerun()
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")


def opiniones_o_interes():
    st.subheader("Opiniones e Intereses")
    st.divider()
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('opiniones_o_interes', {})
    
    mayor_logro = st.text_input("¿Cuál considera que es su mayor logro personal?", value=respuestas_guardadas.get("mayor_logro", ""))
    cambios_entorno = st.text_input("¿Qué cambios le gustaría ver en su entorno?", value=respuestas_guardadas.get("cambios_entorno", ""))

    if st.button("Guardar Opiniones e Intereses"):
        if mayor_logro and cambios_entorno:
            try:
                st.session_state.respuestas_guardadas['opiniones_o_interes'] = {
                    "mayor_logro": mayor_logro,
                    "cambios_entorno": cambios_entorno
                }
                st.success("Opiniones e Intereses Guardados")

                st.session_state.pagina_actual = 'consentimientos_y_comentarios'
                st.rerun() 
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")

def consentimientos_y_comentarios():
    st.subheader("Consentimientos y Comentarios")
    st.divider()
    respuestas_guardadas = st.session_state.respuestas_guardadas.get('consentimientos_y_comentarios', {})
    
    consentimiento = st.radio("¿Está de acuerdo en que los datos proporcionados sean utilizados únicamente para fines de este estudio?", ["Sí", "No"], index=["Sí", "No"].index(respuestas_guardadas.get("consentimiento", "Sí")))
    comentario_adicional = st.text_input("¿Desea agregar algún comentario adicional?", value=respuestas_guardadas.get("comentario_adicional", ""))

    if st.button("Guardar Consentimientos y Comentarios"):
        if consentimiento and comentario_adicional:
            try:
                st.session_state.respuestas_guardadas['consentimientos_y_comentarios'] = {
                    "consentimiento": consentimiento,
                    "comentario_adicional": comentario_adicional
                }
                st.success("Consentimientos y Comentarios Guardados")
            except ValueError:
                st.error("Error al guardar los datos.")
        else:
            st.error("Por favor, complete todos los campos.")
    
    if st.button("Enviar Respuestas"):
        st.session_state.pagina_actual = 'enviar_respuestas'
        st.rerun() 

def enviar_respuestas():
    respuestas_guardadas = st.session_state.respuestas_guardadas

    archivo_csv = 'data/respuestas_encuesta.csv'

    with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
        escritor_csv = csv.writer(archivo)
        
        if archivo.tell() == 0:
            escritor_csv.writerow([
                'Nombres', 'Apodo', 'Apellidos', 'Edad', 'Género', 'Fecha de Nacimiento',

                'Teléfono', 'Correo', 'Redes Sociales', 'Dirección', 'Calle y Número', 'Departamento', 'Provincia',

                'Nivel Educativo', 'Máximo Nivel de Estudios', 'Actualmente Estudia', 'Semestre Académico',
                'Escuela Profesional', 'Actualmente Empleado', 'Tipo Empleo', 'Ingresos',

                'Tiene Pareja', 'Estado Civil', 'Tiene Hijos',

                'Padece Enfermedad', 'Actividad Física',

                'Fuma', 'Toma Alcohol', 'Actividades Recreativas',

                'Mayor Logro', 'Cambios Entorno',

                'Consentimiento', 'Comentario Adicional'])

        escritor_csv.writerow([
            #info personal
            respuestas_guardadas.get('informacion_personal', {}).get('nombres', ''),
            respuestas_guardadas.get('informacion_personal', {}).get('apodo', ''),
            respuestas_guardadas.get('informacion_personal', {}).get('apellido', ''),
            respuestas_guardadas.get('informacion_personal', {}).get('edad', ''),
            respuestas_guardadas.get('informacion_personal', {}).get('genero', ''),
            respuestas_guardadas.get('informacion_personal', {}).get('fecha_nacimiento', ''),
            
            #contacto
            respuestas_guardadas.get('contacto', {}).get('telefono', ''),
            respuestas_guardadas.get('contacto', {}).get('correo', ''),
            respuestas_guardadas.get('contacto', {}).get('redes_sociales', ''),
            respuestas_guardadas.get('contacto', {}).get('direccion', ''),
            respuestas_guardadas.get('contacto', {}).get('distrito', ''),
            respuestas_guardadas.get('contacto', {}).get('provincia', ''),
            respuestas_guardadas.get('contacto', {}).get('departamento', ''),

            #nivel_socioeconomico
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('actualmente_estudia', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('nivel_educativo', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('nombre_universidad', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('escuela_profesional', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('semestre_academico', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('actualmente_empleado', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('tipo_empleo', ''),
            respuestas_guardadas.get('nivel_socioeconomico', {}).get('ingresos_mensual', ''),
            
            #situacion_sentimental
            respuestas_guardadas.get('situacion_sentimental', {}).get('tiene_pareja', ''),
            respuestas_guardadas.get('situacion_sentimental', {}).get('estado_civil', ''),
            respuestas_guardadas.get('situacion_sentimental', {}).get('tiene_hijos', ''),

            respuestas_guardadas.get('salud_y_bienestar', {}).get('padece_enfermedad', ''),
            respuestas_guardadas.get('salud_y_bienestar', {}).get('actividad_fisica', ''),
            respuestas_guardadas.get('habitos_estilo_de_vida', {}).get('fuma', ''),
            respuestas_guardadas.get('habitos_estilo_de_vida', {}).get('toma_alcohol', ''),
            respuestas_guardadas.get('habitos_estilo_de_vida', {}).get('actividades_recreativas', ''),

            respuestas_guardadas.get('opiniones_o_interes', {}).get('mayor_logro', ''),
            respuestas_guardadas.get('opiniones_o_interes', {}).get('cambios_entorno', ''),

            respuestas_guardadas.get('consentimientos_y_comentarios', {}).get('consentimiento', ''),
            respuestas_guardadas.get('consentimientos_y_comentarios', {}).get('comentario_adicional', '')
        ])

    st.session_state.encuesta_completada = True

    return archivo_csv
