import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
# Configurar idioma español para las fechas

import json

# ======== CONFIGURACIÓN PARA STREAMLIT COMMUNITY CLOUD =========

def formato_fecha_español(fecha):
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    fecha_str = fecha.strftime("%d de %B de %Y")
    for eng, esp in meses.items():
        fecha_str = fecha_str.replace(eng, esp)
    return fecha_str
st.set_page_config(page_title="Granja Porcina", page_icon="🐷", layout="centered")

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

gspread_key_dict = json.loads(st.secrets["gspread_key"])
creds = Credentials.from_service_account_info(gspread_key_dict, scopes=SCOPES)
client = gspread.authorize(creds)
SHEET_ID = st.secrets["SHEET_ID"]

def guardar_en_sheets(hoja, datos):
    sheet = client.open_by_key(SHEET_ID).worksheet(hoja)
    sheet.append_row(datos)

st.title("📋 Registro de Eventos - Granja Porcina 🐖")

# Menú principal en un Radio Button
opcion = st.radio("Selecciona una opción:", ["Partos", "Muertes", "Movimientos", "Destete", "Servicio"], index=0)

# Sección PARTOS
if opcion == "Partos":
    st.header("🐷 Registro de Partos")
    madre = st.text_input("Madre")
    fecha = st.date_input("Fecha")
    fecha_str = formato_fecha_español(fecha)
    nacidos_vivos = st.number_input("Nacidos Vivos", min_value=0, step=1)
    natimortos = st.number_input("Natimortos", min_value=0, step=1)
    momificados = st.number_input("Momificados", min_value=0, step=1)
    mnac = st.number_input("MNac", min_value=0, step=1)
    bv = st.number_input("B.V.", min_value=0, step=1)

    if st.button("Guardar Parto"):
        datos = [
            madre,
            fecha.strftime("%d-%m-%Y"),
            nacidos_vivos,
            natimortos,
            momificados,
            mnac,
            bv
        ]
        guardar_en_sheets("Partos", datos)
        st.success("Registro guardado exitosamente en Google Sheets 🚀")
        
        # Mostrar el último registro guardado en pantalla
        columnas_partos = ["Madre", "Fecha", "Nacidos Vivos", "Natimortos", "Momificados", "MNac", "B.V."]
        df_partos = pd.DataFrame([datos], columns=columnas_partos)
        st.subheader("Último registro (Partos)")
        st.table(df_partos)

# Sección MUERTES
elif opcion == "Muertes":
    st.header("⚠️ Registro de Muertes")
    madre_muerte = st.text_input("Madre")
    fecha_muerte = st.date_input("Fecha Muerte")
    fecha_muerte_str = formato_fecha_español(fecha_muerte)
    cantidad_muerte = st.number_input("Cantidad Muertos", min_value=0, step=1)
    causa_muerte = st.text_input("Causa")

    if st.button("Guardar Muertes"):
        datos = [
            madre_muerte,
            fecha_muerte.strftime("%d-%m-%Y"),
            cantidad_muerte,
            causa_muerte
        ]
        guardar_en_sheets("Muertes", datos)
        st.success("Registro guardado exitosamente en Google Sheets 🚀")
        
        # Mostrar el último registro guardado en pantalla
        columnas_muertes = ["Madre", "Fecha Muerte", "Cantidad Muertos", "Causa"]
        df_muertes = pd.DataFrame([datos], columns=columnas_muertes)
        st.subheader("Último registro (Muertes)")
        st.table(df_muertes)

# Sección MOVIMIENTOS
elif opcion == "Movimientos":
    st.header("🚛 Registro de Movimientos (Lechones)")
    donadora = st.text_input("Donadora")
    receptora = st.text_input("Receptora")
    fecha_mov = st.date_input("Fecha Movimiento")
    fecha_mov_str = formato_fecha_español(fecha_mov)
    cantidad_mov = st.number_input("Cantidad de Lechones", min_value=0, step=1)

    if st.button("Guardar Movimiento"):
        datos = [
            donadora,
            receptora,
            fecha_mov.strftime("%d-%m-%Y"),
            cantidad_mov
        ]
        guardar_en_sheets("Movimientos", datos)
        st.success("Registro guardado exitosamente en Google Sheets 🚀")
        
        # Mostrar el último registro guardado en pantalla
        columnas_mov = ["Donadora", "Receptora", "Fecha Movimiento", "Cantidad Lechones"]
        df_mov = pd.DataFrame([datos], columns=columnas_mov)
        st.subheader("Último registro (Movimientos)")
        st.table(df_mov)

# Sección DESTETE
elif opcion == "Destete":
    st.header("🐖 Registro de Destete")
    madre = st.text_input("Madre")
    fecha = st.date_input("Fecha Destete")
    fecha_str = fecha.strftime("%d-%m-%Y")
    destetados = st.number_input("Destetados", min_value=0, step=1)
    lote = st.text_input("Lote")
    observaciones = st.text_area("Observaciones")

    if st.button("Guardar Destete"):
        datos = [
            madre,
            fecha.strftime("%d-%m-%Y"),
            destetados,
            lote,
            observaciones
        ]
        guardar_en_sheets("Destetes", datos)
        st.success("Registro guardado exitosamente en Google Sheets 🚀")
        
        # Mostrar el último registro guardado en pantalla
        columnas_destete = ["Madre", "Fecha Destete", "Destetados", "Lote", "Observaciones"]
        df_destete = pd.DataFrame([datos], columns=columnas_destete)
        st.subheader("Último registro (Destete)")
        st.table(df_destete)

# Sección SERVICIO
elif opcion == "Servicio":
    st.header("💉 Registro de Servicio")
    madre = st.text_input("Madre")
    fecha_servicio = st.date_input("Fecha de Servicio")
    fecha_servicio_str = formato_fecha_español(fecha_servicio)
    padrillo = st.text_input("Padrillo")
    funcionario = st.text_input("Funcionario")
    observaciones_serv = st.text_area("Observaciones")

    if st.button("Guardar Servicio"):
        datos = [
            madre,
            fecha_servicio.strftime("%d-%m-%Y"),
            padrillo,
            funcionario,
            observaciones_serv
        ]
        guardar_en_sheets("Servicios", datos)
        st.success("Registro guardado exitosamente en Google Sheets 🚀")
        
        # Mostrar el último registro guardado en pantalla
        columnas_servicio = ["Madre", "Fecha", "Padrillo", "Funcionario", "Observaciones"]
        df_serv = pd.DataFrame([datos], columns=columnas_servicio)
        st.subheader("Último registro (Servicio)")
        st.table(df_serv)
