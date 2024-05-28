import flet as ft

def main(page: ft.Page):

    page.title = "Gestión de Personal"

    def agregar_empleado(e):
        if nombre_field.value and puesto_field.value and salario_field.value and dpi_field.value and edad_field.value:
            nueva_fila = ft.Row(
                controls=[
                    ft.Text(nombre_field.value),
                    ft.Text(puesto_field.value),
                    ft.Text(salario_field.value),
                    ft.Text(dpi_field.value),
                    ft.Text(edad_field.value),
                ]
            )
            lista_empleados.controls.append(nueva_fila)
            page.update()
            # Limpiar campos
            nombre_field.value = ""
            puesto_field.value = ""
            salario_field.value = ""
            dpi_field.value = ""
            edad_field.value = ""
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("⚠️ Todos los campos son obligatorios."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre")
    puesto_field = ft.TextField(label="Puesto")
    salario_field = ft.TextField(label="Salario Q#")
    dpi_field = ft.TextField(label="DPI")
    edad_field = ft.TextField(label="Edad")
    reminder_text = ft.Text("Recuerda que no puedes agregar campos vacíos", color="green")

    # Botones
    aniadir_button = ft.ElevatedButton(text="Añadir", on_click=agregar_empleado)
    guardar_button = ft.ElevatedButton(text="Guardar")

    # Lista de empleados
    lista_empleados = ft.Column()

    page.add(
        nombre_field,
        puesto_field,
        salario_field,
        dpi_field,
        edad_field,
        reminder_text,
        ft.Row([aniadir_button, guardar_button]),
        lista_empleados
    )

ft.app(target=main)