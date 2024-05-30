import flet as ft
import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Configurar la autenticación de Google Sheets
CREDENTIALS_FILE = 'credentials.json'
TOKEN_PICKLE = 'token.pickle'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ID de tu Google Sheet
SPREADSHEET_ID = '1JgCSNi52gF0BXDB_Jie-PVaXpBCIt3Gxv0Kq5PyuGpk'  # Reemplaza con el ID correcto de tu Google Sheet
RANGE_NAME = 'Control de Personal!A2'  # Reemplaza con el nombre correcto de la hoja y el rango

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main(page: ft.Page):
    page.title = "Gestión de Personal"
    page.scroll = "adaptive"  # Agregar barra de desplazamiento vertical

    dpis_registrados = set()
    empleados = []
    editando = False
    index_editando = -1

    def agregar_empleado(e):
        nonlocal editando, index_editando
        # Resetear mensajes de error
        edad_field.error_text = None
        dpi_field.error_text = None
        salario_field.error_text = None
        page.update()

        # Verificar campos vacíos
        if not nombre_field.value or not puesto_field.value or not salario_field.value or not dpi_field.value or not edad_field.value:
            recuerdo_text.value = "⚠️ No puedes agregar campos vacíos"
            recuerdo_text.color = "red"
            page.update()
            return

        try:
            edad = int(edad_field.value)
            dpi = int(dpi_field.value)
            salario = float(salario_field.value.replace(",", ""))
        except ValueError:
            if not edad_field.value.isdigit():
                edad_field.error_text = "Debe ser un número entero"
            if not dpi_field.value.isdigit():
                dpi_field.error_text = "Debe ser un número entero"
            try:
                float(salario_field.value.replace(",", ""))
            except ValueError:
                salario_field.error_text = "Debe ser un número decimal"
            page.update()
            return

        # Validar que el DPI no se repita
        for i, empleado in enumerate(empleados):
            if empleado["dpi"] == str(dpi) and (not editando or (editando and i != index_editando)):
                dpi_text.value = "🚫 Este DPI ya está registrado"
                dpi_text.color = "red"
                page.update()
                return

        if 18 <= edad <= 35:
            nuevo_empleado = {
                "nombre": nombre_field.value,
                "puesto": puesto_field.value,
                "salario": salario,
                "dpi": str(dpi),
                "edad": edad_field.value
            }
            if editando:
                empleados[index_editando] = nuevo_empleado
                aniadir_button.text = "Añadir"
                editando = False
                index_editando = -1
            else:
                empleados.append(nuevo_empleado)
                dpis_registrados.add(dpi)
                agregar_fila_empleado(nuevo_empleado)
            
            guardar_datos(None)  # Guardar los datos en el archivo JSON después de añadir o editar
            guardar_en_google_sheets()  # Guardar los datos en Google Sheets
            page.update()
            # Limpiar campos
            nombre_field.value = ""
            puesto_field.value = ""
            salario_field.value = ""
            dpi_field.value = ""
            edad_field.value = ""
            # Resetear color y mensaje del texto de recordatorio
            recuerdo_text.value = "Recuerda que no puedes agregar campos vacíos"
            recuerdo_text.color = "green"
            restriccion_edad_text.value = "Solo trabajadores mayores a 18 y menores a 35"
            restriccion_edad_text.color = "blue"
            dpi_text.value = "Ingresa DPI del empleado, recuerda que no se pueden repetir"
            dpi_text.color = "blue"
            actualizar_lista_empleados()
        else:
            restriccion_edad_text.value = "🚫 No cumple con la edad necesaria para trabajar en esta empresa"
            restriccion_edad_text.color = "red"
            page.update()

    def guardar_datos(e):
        with open("empleados.json", "w") as f:
            json.dump(empleados, f, indent=4)
        mostrar_datos_json()

    def guardar_en_google_sheets():
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Convertir los datos a formato de lista para Google Sheets
        values = [[emp["nombre"], emp["puesto"], emp["salario"], emp["dpi"], emp["edad"]] for emp in empleados]

        body = {
            'values': values
        }
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="RAW",
            body=body
        ).execute()

    def mostrar_datos_json():
        if os.path.exists("empleados.json"):
            with open("empleados.json", "r") as f:
                datos = json.load(f)
                empleados.clear()
                empleados.extend(datos)
                dpis_registrados.clear()
                for empleado in empleados:
                    dpis_registrados.add(int(empleado["dpi"]))
                actualizar_lista_empleados()

    def editar_empleado(index):
        nonlocal editando, index_editando
        empleado = empleados[index]
        nombre_field.value = empleado["nombre"]
        puesto_field.value = empleado["puesto"]
        salario_field.value = str(empleado["salario"])
        dpi_field.value = empleado["dpi"]
        edad_field.value = empleado["edad"]
        index_editando = index
        editando = True
        aniadir_button.text = "Guardar"
        page.update()

    def borrar_empleado(index):
        empleado = empleados[index]
        del empleados[index]
        dpis_registrados.remove(int(empleado["dpi"]))
        guardar_datos(None)  # Guardar los datos en el archivo JSON después de eliminar
        guardar_en_google_sheets()  # Guardar los datos en Google Sheets
        actualizar_lista_empleados()

    def agregar_fila_empleado(empleado):
        fila = ft.Row(
            controls=[
                ft.Text(empleado["nombre"]),
                ft.Text(empleado["puesto"]),
                ft.Text(f"Q{empleado['salario']:,.2f}"),
                ft.Text(empleado["dpi"]),
                ft.Text(empleado["edad"]),
                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: editar_empleado(empleados.index(empleado))),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: borrar_empleado(empleados.index(empleado)))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        lista_empleados.controls.append(fila)
        page.update()

    def actualizar_lista_empleados():
        lista_empleados.controls.clear()
        for empleado in empleados:
            agregar_fila_empleado(empleado)
        page.update()

    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre", width=450)
    puesto_field = ft.TextField(label="Puesto", width=450)
    salario_text = ft.Text("Ingresa el salario del empleado, ejem: 5000", color="blue")
    salario_field = ft.TextField(label="Salario Q#", width=450)
    dpi_text = ft.Text("Ingresa DPI del empleado, recuerda que no se pueden repetir", color="blue")
    dpi_field = ft.TextField(label="DPI", width=450)
    edad_field = ft.TextField(label="Edad", width=450)
    restriccion_edad_text = ft.Text("Solo trabajadores mayores a 18 y menores a 35", color="blue")
    recuerdo_text = ft.Text("Recuerda que no puedes agregar campos vacíos", color="green")
    datos_text = ft.Text("")

    # Botones
    aniadir_button = ft.ElevatedButton(text="Añadir", on_click=agregar_empleado)

    # Lista de empleados
    lista_empleados = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column(
            controls=[
                nombre_field,
                puesto_field,
                salario_text,
                salario_field,
                dpi_text,
                dpi_field,
                restriccion_edad_text,
                edad_field,
                recuerdo_text,
                aniadir_button,
                ft.Container(height=20),  # Añadir espacio antes de la lista de empleados
                ft.ListView(
                    controls=[lista_empleados],
                    expand=True,  # Permitir que la lista de empleados se expanda
                ),
                datos_text
            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical al inicio
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    mostrar_datos_json()

ft.app(target=main)
