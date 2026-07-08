import flet as ft

@ft.control
class Botao(ft.Button):
    expand: False
    height: int = 50
    border_radius: int = 10

@ft.control
class BotaoSalvar(Botao):
    bgcolor: ft.Colors = ft.Colors.GREEN
    icon: ft.Icons = ft.Icons.SAVE  
    width: int = 140
    height: int = 45
    expand: False

@ft.control
class BotaoLimpar(Botao):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY
    icon: ft.Icons = ft.Icons.CLEAR
    width: int = 140
    height: int = 45
    expand: False

class Checkbox(ft.Checkbox):
    expand: int = 1
    height: int = 50
    border_radius: int = 10

