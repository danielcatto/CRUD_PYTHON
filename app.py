import flet as ft


def main(page: ft.Page):
    # --- Configurações básicas da janela ---
    # título da janela (aparece na barra do navegador/OS)
    page.title = "Analizador de Notas emitidas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16
    page.scroll = "adaptive"

    # --- Cabeçalho (AppBar) ---
    # Usamos AppBar para criar um cabeçalho padrão com título centralizado.
    page.appbar = ft.AppBar(
        title=ft.Text("Analizador de Notas emitidas", size=20, weight=ft.FontWeight.BOLD),
        center_title=True,
    )

    # --- Conteúdo de exemplo ---
    # Mantemos um pequeno texto para que a janela não fique vazia.
    page.add(
        ft.Column([
            ft.Text("Cabeçalho criado com AppBar. Aqui ficará o conteúdo da aplicação."),
        ], alignment="start")
    )


if __name__ == "__main__":
    ft.app(target=main)