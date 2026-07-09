import flet as ft
import datetime
# IMPORTANTE: Aqui trazemos as funções que criamos no outro arquivo
from banco import inicializar_banco, db_criar_pedido, db_listar_pedidos
from componentes.botoes import Botao, BotaoSalvar, BotaoLimpar, Checkbox
from componentes.Textos import Textos, Titulo
from componentes.mensagens import mensagem


def main(page: ft.Page):

    # 1. Configurações da Janela
    page.window.width = 600
    page.window.height = 600
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



    # --- FUNÇÃO QUE ALIMENTA OS DADOS NA TABELA ---
    def renderizar_tabela():
        tabela_notas.rows.clear()
        try:
            pedidos_do_banco = db_listar_pedidos()
            for p in pedidos_do_banco:
                tabela_notas.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(p['pedido'])),
                            ft.DataCell(ft.Text(p['nome'])),
                            ft.DataCell(ft.Text("Sim" if p['iva'] else "Não")),
                            ft.DataCell(ft.Text("Sim" if p['valor'] else "Não")),
                            ft.DataCell(ft.Text("Sim" if p['flag'] else "Não")),
                            ft.DataCell(ft.Text(p['data_avaliacao'].strftime("%Y-%m-%d %H:%M:%S"))),  # Novo campo na tabela
                        ]
                    )
                )
        except Exception as ex:
            snack_erro = ft.SnackBar(ft.Text(f"Erro ao carregar tabela: {ex}"), bgcolor="red")
            page.overlay.append(snack_erro)
            snack_erro.open = True
        page.update()




   # 6. Criando a Estrutura da Tabela de Dados
    tabela_pedidos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("IVA")),
            ft.DataColumn(ft.Text("Valor")),
            ft.DataColumn(ft.Text("Flag")),
            ft.DataColumn(ft.Text("Data da Avaliação")),  # Novo campo na tabela
        ],
        rows=[]
    )

    # --- FUNÇÃO QUE ALIMENTA OS DADOS NA TABELA ---
    def renderizar_tabela():
        tabela_pedidos.rows.clear()
        try:
            pedidos_do_banco = db_listar_pedidos()
            for p in pedidos_do_banco:
                tabela_pedidos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(p['pedido'])),
                            ft.DataCell(ft.Text(p['nome'])),
                            ft.DataCell(ft.Text("Sim" if p['iva'] else "Não")),
                            ft.DataCell(ft.Text("Sim" if p['valor'] else "Não")),
                            ft.DataCell(ft.Text("Sim" if p['flag'] else "Não")),
                            ft.DataCell(ft.Text(p['data_avaliacao'].strftime("%Y-%m-%d %H:%M:%S"))),  # Novo campo na tabela
                        ]
                    )
                )
        except Exception as ex:
            snack_erro = ft.SnackBar(ft.Text(f"Erro ao carregar tabela: {ex}"), bgcolor="red")
            page.overlay.append(snack_erro)
            snack_erro.open = True
        page.update()




    #Montando o cabeçaçho   
    header = ft.Row(
        [titulo],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # 6. Criando a Estrutura da Tabela de Dados
    tabela_notas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("IVA")),
            ft.DataColumn(ft.Text("Valor")),
            ft.DataColumn(ft.Text("Flag")),
        ],
        rows=[]
    )
    
    table_container = ft.Column([
        ft.Text("Histórico de Pedidos Analisados", size=20, weight=ft.FontWeight.W_500),
        ft.Divider(),
        ft.Row([tabela_pedidos], scroll="always") # Impede erro lateral caso fique grande
    ], spacing=10)


    page_componentes = ft.Column(
        expand=True,
        controls=[  
            
            ft.Container(
                expand=True,
                padding=10,
                content=
                    ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER ,
                    controls=[
                        Titulo(value="Listar Notas com Erros")
                    ],
                )   
                
                
            ),
            ft.Container(
                expand=True,
                content=
                      ft.Row(
                          controls=[
                              ft.Text("Listar notas"),
                          ]
                    ),       
                
                
            ),

            ft.Container(
                expand=True,
                content=
                      ft.Row(
                          controls=[
                            table_container,
                          ]
                    ),       
                
                
            )

            

        ]
    )


    page.add(
        header,
        page_componentes,
    
    )
  # 9. Busca inicial: Carrega o banco assim que abre o programa
    renderizar_tabela()
if __name__ == "__main__":
    ft.run(main)