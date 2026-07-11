import flet as ft
import datetime
# IMPORTANTE: Aqui trazemos as funções que criamos no outro arquivo
from banco import inicializar_banco, db_criar_pedido, db_listar_pedidos
from componentes.botoes import Botao, Botao3Dias,  Checkbox
from componentes.Textos import Textos, Titulo
from componentes.mensagens import mensagem


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


    #Inicialização do Banco de Dados
    try:
        inicializar_banco()
    except Exception as e:
        snack = ft.SnackBar(
                content=ft.Text(f"Erro na conexão do banco!", color=ft.Colors.WHITE,),
                bgcolor="red", 
            )
    
        page.overlay.append(snack)
        snack.open = True
        page.update()
        return


    #Montando o cabeçaçho   
    header = ft.Row(
        [titulo],
        alignment=ft.MainAxisAlignment.CENTER
    )
    # 6. Criando a Estrutura da Tabela de Dados
    tabela_pedidos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("IVA")),
            ft.DataColumn(ft.Text("Valor")),
            ft.DataColumn(ft.Text("Flag")),
            ft.DataColumn(ft.Text("Data da Avaliação")),
        ],
        rows=[]
    )


    # --- FUNÇÃO QUE ALIMENTA OS DADOS NA TABELA ---
    def renderizar_tabela(dias=1):
        tabela_pedidos.rows.clear()

        try:
            pedidos_do_banco = db_listar_pedidos(dias)

            for p in pedidos_do_banco:
                tabela_pedidos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(p["pedido"])),
                            ft.DataCell(ft.Text(p["nome"])),
                            ft.DataCell(ft.Text("Sim" if p["iva"] else "Não")),
                            ft.DataCell(ft.Text("Sim" if p["valor"] else "Não")),
                            ft.DataCell(ft.Text("Sim" if p["flag"] else "Não")),
                            ft.DataCell(
                                ft.Text(
                                    p["data_avaliacao"].strftime("%d/%m/%Y %H:%M")
                                )
                            ),
                        ]
                    )
                )

            tabela_pedidos.update()

        except Exception as ex:
            mensagem(page, str(ex), ft.Colors.RED)


    table_container = ft.Column([
        ft.Text("Histórico de Pedidos Analisados", size=20, weight=ft.FontWeight.W_500),
        ft.Divider(),
        ft.Row([tabela_pedidos], scroll="always")
    ], spacing=10)


    page_componentes = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                padding=10,
                content=
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[Titulo(value="Listar Notas com Erros")],
                    ),
            ),
            ft.Container(
                expand=True,
                content=
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Text("asdf"), ft.Text("asdf"), ft.Text("asdf")],
                    ),
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    Botao3Dias(content="3 Dias", on_click=lambda e: renderizar_tabela(3)),
                    Botao3Dias(content="7 Dias", on_click=lambda e: renderizar_tabela(7)),
                    Botao3Dias(content="15 Dias", on_click=lambda e: renderizar_tabela(15)),
                    Botao3Dias(content="30 Dias", on_click=lambda e: renderizar_tabela(30)),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[ft.Text("asdf"), ft.Text("asdf"), ft.Text("asdf")],
            ),
            ft.Container(
                expand=True,
                content=ft.Row(controls=[table_container]),
            ),
        ],
    )


    page.add(header, page_componentes)

    # 9. Busca inicial: Carrega o banco assim que abre o programa
    renderizar_tabela()

ft.run(main)