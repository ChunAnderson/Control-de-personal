import flet as ft

def main(page: ft.Page):
    data = []


    page.title = "Gestión de Personal"

    name_field = ft.TextField(label="Nombre")
    puesto_field = ft.TextField(label="Puesto")

    save_button = ft.ElevatedButton(text="Guardar", visible=False)
    message_text = ft.Text("", color="green")

    employee_list = ft.ListView(expand=1, spacing=10, padding=20)

    page.add(
        name_field,
        puesto_field,
        message_text,
        ft.Row([save_button]),
        employee_list
    )


ft.app(target=main)
