import flet as ft
# IMPORTANTE: Aqui trazemos as funções que criamos no outro arquivo
from banco import inicializar_banco, db_criar_pedido, db_listar_pedidos

def main(page: ft.Page):
    # 1. Configurações da Janela
    page.title = "Checa erros das notas fiscais"
    page.theme_mode = ft.ThemeMode.DARK  # Força o modo escuro
    page.padding = 20                    # Margem interna nas bordas da janela
    page.scroll = "adaptive"             # Cria barra de rolagem se a tela encolher
    
    # 2. Inicialização do Banco de Dados
    try:
        inicializar_banco()
    except Exception as e:
        page.add(ft.Text(f"❌ Erro ao conectar ao banco: {e}", color="red", size=16))
        page.update()
        return

    # 3. Elementos de Rótulo e Mensagens
    titulo = ft.Text("Checa erros das notas fiscais", size=28, weight=ft.FontWeight.BOLD)
    msg1 = ft.Text("Marcar as opções divergentes.", size=16)

    # 4. Componentes do Formulário (Inputs)
    txt_pedido = ft.TextField(label="Pedido", hint_text="Digite o Número do Pedido", expand=True)
    txt_nome = ft.TextField(label="Nome", hint_text="Digite o nome completo", expand=True)
    chk_iva = ft.Checkbox(label="", value=False)
    chk_valor = ft.Checkbox(label="", value=False)
    chk_flag = ft.Checkbox(label="", value=False)

    # --- POP-UP DE VALIDAÇÃO (AlertDialog) ---
    def fechar_dialogo(e):
        janela_aviso.open = False
        page.update()

    janela_aviso = ft.AlertDialog(
        title=ft.Text("⚠️ Campos Obrigatórios"),
        content=ft.Text("Por favor, preencha os campos Pedido e Nome antes de salvar!"),
        actions=[
            ft.TextButton("OK", on_click=fechar_dialogo)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # --- FUNÇÃO PARA LIMPAR CAMPOS ---
    def limpar_campos(e):
        txt_pedido.value = ""
        txt_nome.value = ""
        chk_iva.value = False
        chk_valor.value = False
        chk_flag.value = False
        page.update()

    # --- FUNÇÃO SALVAR ---
    def salvar_dados(e):
        pedido = txt_pedido.value.strip()
        nome = txt_nome.value.strip()
        iva = chk_iva.value
        valor = chk_valor.value
        flag = chk_flag.value

        if not pedido or not nome:
            page.overlay.append(janela_aviso)
            janela_aviso.open = True
            page.update()
            return

        try:
            # 1. Tenta salvar no banco de dados
            db_criar_pedido(pedido, nome, iva, valor, flag)
            
            # 2. Limpa os campos após salvar
            txt_pedido.value = ""
            txt_nome.value = ""
            chk_iva.value = False
            chk_valor.value = False
            chk_flag.value = False
            
            # 3. Exibe a confirmação na tela
            snack = ft.SnackBar(
                content=ft.Text("✅ Pedido visto e salvo com sucesso!"),
                bgcolor="green"
            )
            page.overlay.append(snack)
            snack.open = True
            
            # 4. Atualiza as linhas da tabela em tempo real!
            renderizar_tabela()
            
        except Exception as ex:
            snack_erro = ft.SnackBar(
                content=ft.Text(f"❌ Erro ao salvar: {ex}"),
                bgcolor="red"
            )
            page.overlay.append(snack_erro)
            snack_erro.open = True
        
        page.update()

    # 5. Criando os Botões
    btn_salvar = ft.ElevatedButton("Salvar", icon=ft.Icons.SAVE, on_click=salvar_dados)
    btn_limpar = ft.OutlinedButton("Limpar campos", icon=ft.Icons.CLEAR, on_click=limpar_campos)
    
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

    # 7. Estruturação dos Containers de Layout
    header = ft.Row(
        [titulo],
        alignment=ft.MainAxisAlignment.CENTER
    )

#    form_container = ft.Column([
#        ft.Row([txt_pedido, txt_nome], alignment=ft.MainAxisAlignment.CENTER),
#        ft.Row([msg1], alignment=ft.MainAxisAlignment.CENTER),
#        ft.Row([ft.Text("IVA:"), chk_iva], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
#        ft.Row([ft.Text("Valor:"), chk_valor], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
#        ft.Row([ft.Text("Flag:"), chk_flag], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
#        ft.Container(height=10),
#        ft.Row([btn_salvar, btn_limpar], alignment=ft.MainAxisAlignment.CENTER),
#    ])

    table_container = ft.Column([
        ft.Text("Histórico de Pedidos Analisados", size=20, weight=ft.FontWeight.W_500),
        ft.Divider(),
        ft.Row([tabela_pedidos], scroll="always") # Impede erro lateral caso fique grande
    ], spacing=10)

    # 8. Renderiza e monta a interface na tela
    page.add(
        header,
        ft.Container(height=20),
        #form_container,
        ft.Container(height=30),
        table_container
    )

    # 9. Busca inicial: Carrega o banco assim que abre o programa
    renderizar_tabela()

if __name__ == "__main__":
    ft.app(target=main)