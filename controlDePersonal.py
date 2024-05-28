import flet as ft

def main(page: ft.Page):

    page.title = "Gestión de Personal"

    name_field = ft.TextField(label="Nombre")
    puesto_field = ft.TextField(label="Puesto")
    salario_field = ft.TextField(label="Salario Q#")
    dpi_field = ft.TextField(label="DPI")
    edad_field = ft.TextField(label="Edad")

   
    aniadir_button = ft.ElevatedButton(text="Añadir" )
    guardar_button = ft.ElevatedButton(text="Guardar")


    page.add(
        name_field,
        puesto_field,
        salario_field,
        dpi_field,
        edad_field,
        ft.Row({guardar_button, aniadir_button})
    )

ft.app(target=main)