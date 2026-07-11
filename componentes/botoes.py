import flet as ft

@ft.control
class Botao(ft.Button):
    expand: True
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

@ft.control
class Botao3Dias(Botao):
    bgcolor: ft.Colors = ft.Colors.BROWN_50
    icon: ft.Icons = ft.Icons.ARROW_DROP_UP  
    width: int = 140
    height: int = 45
    expand: False

    color: ft.Colors = ft.Colors.BLACK


#Botão de navegação
@ft.control
class BotaoNav(Botao):
    bgcolor: ft.Colors = ft.Colors.GREEN_ACCENT_200
    icon: ft.Icons = ft.Icons.ASSISTANT_NAVIGATION
    width: int = 300
    height: int = 150
    color: ft.Colors = ft.Colors.BLACK



@ft.control
class Checkbox(ft.Checkbox):
    expand: int = 1
    height: int = 50
    border_radius: int = 10
