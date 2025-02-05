import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Archivo XLSX para almacenar los datos
XLSX_FILE = "registro_eventos.xlsx"

# Verificar si el archivo existe, si no, crearlo con encabezados
if not os.path.exists(XLSX_FILE):
    df = pd.DataFrame(columns=["Fecha", "Evento", "ID Madre", "Cantidad", "Ubicación", "Observaciones"])
    with pd.ExcelWriter(XLSX_FILE, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Eventos')

# Función para cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_excel(XLSX_FILE, sheet_name='Eventos')

# Función para guardar datos
def guardar_datos(nuevo_dato):
    df = cargar_datos()
    df = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
    with pd.ExcelWriter(XLSX_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, sheet_name='Eventos')

# Interfaz de usuario
st.title("Registro de Eventos - Granja de Cerdos")

# Selección de evento
evento = st.selectbox("Seleccione un evento", ["Nacimiento", "Destete", "Baja", "Tratamiento", "Inseminación", "Movimiento", "Pasaje de lechones", "Fallecido"])

# Entrada de datos
id_madre = st.text_input("ID de la madre (opcional)")
cantidad = st.number_input("Cantidad", min_value=1, step=1)
ubicacion = st.text_input("Ubicación (sala, corral, etc.)")
observaciones = st.text_area("Observaciones (opcional)")
fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Botón para guardar
guardar = st.button("Registrar Evento")
if guardar:
    nuevo_dato = {
        "Fecha": fecha,
        "Evento": evento,
        "ID Madre": id_madre,
        "Cantidad": cantidad,
        "Ubicación": ubicacion,
        "Observaciones": observaciones,
    }
    guardar_datos(nuevo_dato)
    st.success("Evento registrado con éxito")

# Mostrar datos registrados
st.subheader("Registros recientes")
df = cargar_datos()
st.dataframe(df)
