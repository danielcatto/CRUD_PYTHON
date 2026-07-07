


import flet as ft
import psycopg
from psycopg.rows import dict_row

# ATENÇÃO: Altere com as suas credenciais locais do Postgres
#DB_CONFIG = "dbname=seu_banco user=seu_usuario password=sua_senha host=localhost port=5432"
DB_CONFIG = "dbname=lojas_db_python user=daniel password=p5kplp5k host=2804:10f8:ce00:400::b:222 port=5432"

# --- FUNÇÕES DE BANCO DE DADOS (DB) ---

def inicializar_banco():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    telefone VARCHAR(20)
                );
            """)
            conn.commit()

def db_criar_cliente(nome, email, telefone):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s);",
                (nome, email, telefone)
            )
            conn.commit()

def db_listar_clientes():
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY id DESC;")
            return cur.fetchall()

def db_atualizar_cliente(id_cliente, nome, email, telefone):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE clientes SET nome = %s, email = %s, telefone = %s WHERE id = %s;",
                (nome, email, telefone, id_cliente)
            )
            conn.commit()

def db_deletar_cliente(id_cliente):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clientes WHERE id = %s;", (id_cliente,))
            conn.commit()


# --- APLICAÇÃO VISUAL (FLET) ---

def main(page: ft.Page):
    page.title = "Gerenciador de Clientes - CRUD"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "adaptive"
    
    # Atualiza as configurações iniciais da página imediatamente para evitar a tela branca
    page.update()

    # Tenta conectar ao banco de dados com segurança
    try:
        inicializar_banco()
    except Exception as e:
        # Se falhar, exibe um alerta textual na tela para você saber o que houve
        page.add(ft.Text(f"❌ Erro ao conectar ao banco de dados: {e}", color="red", size=16))
        page.update()
        return

    cliente_em_edicao_id = None

    # Campos do Formulário (Corrigidos)
    txt_nome = ft.TextField(label="Nome", hint_text="Digite o nome completo", expand=True)
    txt_email = ft.TextField(label="E-mail", hint_text="exemplo@email.com", expand=True)
    txt_telefone = ft.TextField(label="Telefone", hint_text="(00) 00000-0000", expand=True)
    
    btn_salvar = ft.ElevatedButton("Cadastrar Cliente", icon=ft.Icons.SAVE, on_click=lambda e: salvar_cliente())
    btn_cancelar = ft.TextButton("Cancelar Edição", visible=False, on_click=lambda e: limpar_formulario())

    # Tabela de dados
    tabela_clientes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("E-mail")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def renderizar_tabela():
        tabela_clientes.rows.clear()
        try:
            clientes = db_listar_clientes()
            for c in clientes:
                tabela_clientes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(c['id']))),
                            ft.DataCell(ft.Text(c['nome'])),
                            ft.DataCell(ft.Text(c['email'])),
                            ft.DataCell(ft.Text(c['telefone'] or "-")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT, 
                                        icon_color="blue",
                                        on_click=lambda e, idx=c['id'], n=c['nome'], em=c['email'], t=c['telefone']: carregar_para_edicao(idx, n, em, t)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE, 
                                        icon_color="red",
                                        on_click=lambda e, idx=c['id']: remover_cliente(idx)
                                    ),
                                ])
                            ),
                        ]
                    )
                )
        except Exception as ex:
            mostrar_snack_bar(f"Erro ao carregar dados: {ex}", "red")
        page.update()

    def salvar_cliente():
        nonlocal cliente_em_edicao_id
        nome = txt_nome.value.strip()
        email = txt_email.value.strip()
        telefone = txt_telefone.value.strip() or None

        if not nome or not email:
            mostrar_snack_bar("Nome e E-mail são obrigatórios!", "orange")
            return

        try:
            if cliente_em_edicao_id is None:
                db_criar_cliente(nome, email, telefone)
                mostrar_snack_bar("Cliente cadastrado com sucesso!", "green")
            else:
                db_atualizar_cliente(cliente_em_edicao_id, nome, email, telefone)
                mostrar_snack_bar("Cliente atualizado com sucesso!", "green")
            
            limpar_formulario()
            renderizar_tabela()
        except psycopg.errors.UniqueViolation:
            mostrar_snack_bar("Erro: Este e-mail já está cadastrado.", "red")
        except Exception as ex:
            mostrar_snack_bar(f"Erro na operação: {ex}", "red")

    def carregar_para_edicao(id_cliente, nome, email, telefone):
        nonlocal cliente_em_edicao_id
        cliente_em_edicao_id = id_cliente
        txt_nome.value = nome
        txt_email.value = email
        txt_telefone.value = telefone or ""
        btn_salvar.text = "Atualizar Dados"
        btn_salvar.icon = ft.Icons.REFRESH
        btn_cancelar.visible = True
        page.update()

    def remover_cliente(id_cliente):
        try:
            db_deletar_cliente(id_cliente)
            mostrar_snack_bar("Cliente removido com sucesso.", "blue_grey")
            if cliente_em_edicao_id == id_cliente:
                limpar_formulario()
            renderizar_tabela()
        except Exception as ex:
            mostrar_snack_bar(f"Erro ao deletar: {ex}", "red")

    def limpar_formulario():
        nonlocal cliente_em_edicao_id
        cliente_em_edicao_id = None
        txt_nome.value = ""
        txt_email.value = ""
        txt_telefone.value = ""
        btn_salvar.text = "Cadastrar Cliente"
        btn_salvar.icon = ft.Icons.SAVE
        btn_cancelar.visible = False
        page.update()

    def mostrar_snack_bar(mensagem, cor):
        page.snack_bar = ft.SnackBar(ft.Text(mensagem), bgcolor=cor)
        page.snack_bar.open = True
        page.update()

    # --- MONTAGEM DA INTERFACE (LAYOUT) ---
    header = ft.Row(
        [ft.Text("👥 Cadastro de Clientes", size=28, weight=ft.FontWeight.BOLD)],
        alignment=ft.MainAxisAlignment.CENTER
    )

    form_container = ft.Column([
        ft.Row([txt_nome, txt_email, txt_telefone]),
        ft.Row([btn_salvar, btn_cancelar], alignment=ft.MainAxisAlignment.END)
    ])

    table_container = ft.Column(
        [
            ft.Text("Clientes Registrados", size=20, weight=ft.FontWeight.W_500),
            ft.Divider(),
            # Usando uma Row com scroll para a tabela não estourar lateralmente
            ft.Row([tabela_clientes], scroll="always")
        ],
        spacing=10
    )

    # Renderiza a estrutura básica na tela
    page.add(
        header,
        ft.Container(height=20),
        form_container,
        ft.Container(height=30),
        table_container
    )

    # Puxa os dados salvos do Postgres para popular a tabela
    renderizar_tabela()

if __name__ == "__main__":
    ft.app(target=main)