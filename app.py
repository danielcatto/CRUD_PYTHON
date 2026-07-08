import flet as ft
import datetime
# IMPORTANTE: Aqui trazemos as funções que criamos no outro arquivo
from banco import inicializar_banco, db_criar_pedido, db_listar_pedidos
from componentes.botoes import Botao, BotaoSalvar, BotaoLimpar, Checkbox
from componentes.Textos import Textos, Titulo
from componentes.mensagens import mensagem


def main(page: ft.Page):
    #Inicialização do Banco de Dados
    try:
        inicializar_banco()
    except Exception as e:
        
        page.update()
        return

    # 1. Configurações da Janela
    page.window.width = 800
    page.window.height = 600
    page.window.center()
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER


    page.title = "Cadastar notas fiscais para correção"
    page.theme_mode = ft.ThemeMode.DARK  # Força o modo escuro
    page.padding = 20                    # Margem interna nas bordas da janela
    page.scroll = "adaptive"             # Cria barra de rolagem se a tela encolher

    #configurando os campos e texto e botões
    @ft.control
    class Nome(Botao):
        expand: bool = True
        border_radius: int = 10
        filled: bool = True


    @ft.control
    class Texto(Textos):
        expand: bool = True
        border_radius: int = 10
        filled: bool = True
        background_color: str = "grey"
        font_color: str = "red"

    @ft.control
    class Check(Checkbox):
        expand: bool = True
        border_radius: int = 10
        filled: bool = True


    #FUNÇÃO PARA LIMPAR CAMPOS ---
    def limpar_campos(e):
        txt_pedido.value = ""
        txt_nome.value = ""
        ch_iva.value = False
        ch_valor.value = False
        cc_flag.value = False
        page.update()

    def salvar_dados(e):
        pedido = txt_pedido.value.strip()
        nome = txt_nome.value.strip()
        iva = ch_iva.value
        valor = ch_valor.value
        flag = cc_flag.value

        try:
            db_criar_pedido(pedido, nome, iva, valor, flag)
            # 3. Exibe a confirmação na tela
            snack = ft.SnackBar(
                content=ft.Text(f"✅ Pedido visto e salvo com sucesso!"),
                bgcolor="green"
            )
            atualizar_tabela_notas()
            page.overlay.append(snack)
            snack.open = True

        except Exception as e:
            snack = ft.SnackBar(
                content=ft.Text(f"❌ Erro ao salvar dados: {e}"),
                bgcolor="red"
            )
            page.overlay.append(snack)
            snack.open = True


   

    def atualizar_tabela_notas():
        tabela_notas.rows.append(
            ft.DataRow(
            cells=[
                    ft.DataCell(ft.Text(txt_pedido.value)), 
                    ft.DataCell(ft.Text(txt_nome.value)),
                    ft.DataCell(ft.Text("Sim" if ch_iva.value else "Não")),
                    ft.DataCell(ft.Text("Sim" if ch_valor.value else "Não")),
                    ft.DataCell(ft.Text("Sim" if cc_flag.value else "Não")),

                    

                ]
            )
        )       
        page.update()



    #criando os campos de texto e botões
    txt_pedido = Texto(label="Pedido", hint_text="Digite o Número do Pedido")
    txt_nome = Texto(label="Nome", hint_text="Digite o nome completo")
    ch_iva = Check(label="Iva", value=False)
    ch_valor = Check(label="Valor", value=False)
    cc_flag = Check(label="Flag", value=False)

    titulo = ft.Text("Checa erros das notas fiscais", size=40, weight=ft.FontWeight.BOLD)

    #Montando o cabeçaçho   
    header = ft.Row(
        [titulo],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
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
                        Titulo(value="Cadastro das Notas Faturadas")
                    ],
                )   
                
                
            ),
            ft.Container(
                expand=True,
                content=
                      ft.Row([
                        txt_pedido,
                        txt_nome,
                         ch_iva,
                        ch_valor,
                        cc_flag]
                    ),       
                
                
            )

        ]
    )
    btn_salvar = BotaoSalvar(content="Salvar", icon=ft.Icons.SAVE, on_click=salvar_dados)
    btn_limpar = BotaoLimpar(content="Limpar", icon=ft.Icons.CLEAR, on_click=limpar_campos)


    #organiza os botões em linha com o .Row
    botoes = ft.Row(
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=20,
    controls=[
        btn_salvar,
        btn_limpar,
    ],
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

    


    page.add(
        header,
        page_componentes,
        botoes,
        tabela_notas,
    )

if __name__ == "__main__":
    ft.run(main)