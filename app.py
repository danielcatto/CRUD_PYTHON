import flet as ft
# IMPORTANTE: Aqui trazemos as funções que criamos no outro arquivo
from banco import inicializar_banco, db_criar_pedido, db_listar_pedidos
from componentes.botoes import Botao, Checkbox
from componentes.Textos import Textos, Titulo


def main(page: ft.Page):
    # 1. Configurações da Janela
    page.window.width = 800
    page.window.height = 600
    page.window.center()
    #page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    #page.vertical_alignment = ft.MainAxisAlignment.CENTER


    page.title = "Checa erros das notas fiscais"
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

    #criando os campos de texto e botões
    txt_pedido = Texto(label="Pedido", hint_text="Digite o Número do Pedido")
    txt_nome = Texto(label="Nome", hint_text="Digite o nome completo")
    ch_iva = Check(label="Iva", value=False)
    ch_valor = Check(label="Valor", value=False)
    cc_flag = Check(label="Flag", value=False)

    titulo = ft.Text("Checa erros das notas fiscais", size=28, weight=ft.FontWeight.BOLD)

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
                        Titulo(value="Cadastro de Clientes")
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


    #FUNÇÃO PARA LIMPAR CAMPOS ---
    def limpar_campos(e):
        txt_pedido.value = ""
        txt_nome.value = ""
        ch_iva.value = False
        ch_valor.value = False
        cc_flag.value = False
        page.update()




#   btn_salvar = Botao("Salvar", icon=ft.Icons.SAVE, on_click=salvar_dados)

    btn_salvar = Botao(content="Salvar", icon=ft.Icons.SAVE)
    btn_limpar = Botao(content="Limpar", icon=ft.Icons.CLEAR, on_click=limpar_campos)
    page.add(
        header,
        page_componentes,
        btn_salvar,
        btn_limpar,
    )

if __name__ == "__main__":
    ft.app(target=main)