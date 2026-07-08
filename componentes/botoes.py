import flet as ft

@ft.control
class Botao(ft.Button):
    expand: int = 1
    height: int = 50
    border_radius: int = 10

class Checkbox(ft.Checkbox):
    expand: int = 1
    height: int = 50
    border_radius: int = 10