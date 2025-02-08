import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# ======== CONFIGURACIÓN PARA STREAMLIT COMMUNITY CLOUD =========
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
    fecha = st.date_input("Fecha", format="%d-%m-%Y")
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

# Sección MUERTES
elif opcion == "Muertes":
    st.header("⚠️ Registro de Muertes")
    madre_muerte = st.text_input("Madre")
    fecha_muerte = st.date_input("Fecha Muerte", format="%d-%m-%Y")
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

# Sección MOVIMIENTOS
elif opcion == "Movimientos":
    st.header("🚛 Registro de Movimientos (Lechones)")
    donadora = st.text_input("Donadora")
    receptora = st.text_input("Receptora")
    fecha_mov = st.date_input("Fecha Movimiento", format="%d-%m-%Y")
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

# Sección DESTETE
elif opcion == "Destete":
    st.header("🐖 Registro de Destete")
    madre = st.text_input("Madre")
    fecha = st.date_input("Fecha Destete", format="%d-%m-%Y")
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

# Sección SERVICIO
elif opcion == "Servicio":
    st.header("💉 Registro de Servicio")
    madre = st.text_input("Madre")
    fecha_servicio = st.date_input("Fecha de Servicio", format="%d-%m-%Y")
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
