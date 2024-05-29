import flet as ft

def main(page: ft.Page):

    page.title = "Gestión de Personal"
    dpis_registrados = set()

    def agregar_empleado(e):
        # Resetear mensajes de error
        edad_field.error_text = None
        dpi_field.error_text = None
        salario_field.error_text = None
        page.update()

        # Verificar campos vacíos
        if not nombre_field.value or not puesto_field.value or not salario_field.value or not dpi_field.value or not edad_field.value:
            recuerdo_text.value = "⚠ No puedes agregar campos vacíos"
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

        if dpi in dpis_registrados:
            dpi_text.value = "🚫 Este DPI ya está registrado"
            dpi_text.color = "red"
            page.update()
            return

        if 18 <= edad <= 35:
            nueva_fila = ft.Row(
                controls=[
                    ft.Text(nombre_field.value),
                    ft.Text(puesto_field.value),
                    ft.Text(f"Q{salario:,.2f}"),
                    ft.Text(dpi_field.value),
                    ft.Text(edad_field.value),
                ]
            )
            lista_empleados.controls.append(nueva_fila)
            dpis_registrados.add(dpi)
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
            page.update()
        else:
            restriccion_edad_text.value = "🚫 No cumple con la edad necesaria para trabajar en esta empresa"
            restriccion_edad_text.color = "red"
            page.update()

    # Campos de entrada
    nombre_field = ft.TextField(label="Nombre")
    puesto_field = ft.TextField(label="Puesto")
    salario_text = ft.Text("Ingresa el salario del empleado, ejem: 5,000", color="blue")
    salario_field = ft.TextField(label="Salario Q#")
    dpi_text = ft.Text("Ingresa DPI del empleado, recuerda que no se pueden repetir", color="blue")
    dpi_field = ft.TextField(label="DPI")
    edad_field = ft.TextField(label="Edad")
    restriccion_edad_text = ft.Text("Solo trabajadores mayores a 18 y menores a 35", color="blue")
    recuerdo_text = ft.Text("Recuerda que no puedes agregar campos vacíos", color="green")

    # Botones
    aniadir_button = ft.ElevatedButton(text="Añadir", on_click=agregar_empleado)
    guardar_button = ft.ElevatedButton(text="Guardar")

    # Lista de empleados
    lista_empleados = ft.Column()

    page.add(
        nombre_field,
        puesto_field,
        salario_text,
        salario_field,
        dpi_text,
        dpi_field,
        restriccion_edad_text,
        edad_field,
        recuerdo_text,
        ft.Row([aniadir_button, guardar_button]),
        lista_empleados
    )

ft.app(target=main)
