import flet as ft

def mensagem(
    page: ft.Page,
    texto: str,
    cor=ft.Colors.GREEN,
):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(texto),
        bgcolor=cor,
        open=True,
    )

    page.update()
