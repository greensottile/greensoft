import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Función para cargar datos en memoria
@st.cache_data
def cargar_datos():
    return pd.DataFrame(columns=["Fecha", "Evento", "ID Madre", "Cantidad", "Ubicación", "Observaciones"])

# Función para guardar datos en memoria
def guardar_datos(df, nuevo_dato):
    df = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
    return df

# Interfaz de usuario
st.title("Registro de Eventos - Granja de Cerdos")

df = cargar_datos()

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
    df = guardar_datos(df, nuevo_dato)
    st.success("Evento registrado con éxito")

# Mostrar datos registrados
st.subheader("Registros recientes")
st.dataframe(df)

# Botón para descargar el archivo Excel
def convertir_a_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Eventos')
    processed_data = output.getvalue()
    return processed_data

st.download_button(
    label="Descargar registros en Excel",
    data=convertir_a_excel(df),
    file_name="registro_eventos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
