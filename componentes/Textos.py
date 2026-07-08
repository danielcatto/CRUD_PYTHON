import flet as ft

@ft.control
class Textos(ft.TextField):
    expand: int = 1
    height: int = 50
    border_radius: int = 10

    # Aparência
    filled: bool = True
    bgcolor = ft.Colors.BLACK
    color = ft.Colors.WHITE

    # Borda
    border_color: ft.Colors = ft.Colors.BLACK_12
    focused_border_color: ft.Colors = ft.Colors.BLUE


@ft.control
class Titulo(ft.Text):
    size: int = 28
    weight: ft.FontWeight = ft.FontWeight.BOLD
    color: str = "#6c9db8"