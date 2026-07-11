import flet as ft
from componentes.botoes import BotaoNav

def main(page: ft.Page):
    # 1. Configurações da Janela
    page.window.width = 750
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK  # Força o modo escuro
    page.padding = 20                    # Margem interna nas bordas da janela
    page.scroll = "adaptive"             # Cria barra de rolagem se a tela encolher
    page.window.center()

    page.title = "Cadastar notas fiscais para correção"
    titulo = ft.Text("Checa erros das notas fiscais", size=40, weight=ft.FontWeight.BOLD)

    btn_cadastro = BotaoNav(content="Cadastro")

    btn_listar = BotaoNav(content="Listar")

   # CABEÇALHO
# ==========================

    cabecalho = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Checa erros das notas fiscais",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.BLUE_GREY_900,
        padding=20,
        border_radius=10,
    )

   

    corpo = ft.Container(
    content=ft.Column(
        controls=[
          btn_cadastro,
          btn_listar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    ),
    expand=True,
    )



    page.add(
        cabecalho,
        corpo,

    )


if __name__ == "__main__":
    ft.run(main)# ==========================
