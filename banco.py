# banco.py
import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


def _carregar_variaveis_env():
    """Carrega as variáveis do arquivo .env se ele existir."""
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for linha in env_path.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue

        chave, valor = linha.split("=", 1)
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        os.environ.setdefault(chave, valor)


_carregar_variaveis_env()

DB_NAME = os.getenv("DB_NAME", "db")
DB_USER = os.getenv("DB_USER", "daniel")
DB_PASSWORD = os.getenv("DB_PASSWORD", "p5kplp5k")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Credenciais do seu banco de dados
DB_CONFIG = (
    f"dbname={DB_NAME} "
    f"user={DB_USER} "
    f"password={DB_PASSWORD} "
    f"host={DB_HOST} "
    f"port={DB_PORT}"
)

def inicializar_banco():
    """Cria a tabela se ela ainda não existir."""
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notas_avaliadas (
                    id SERIAL PRIMARY KEY,
                    pedido VARCHAR(50) NOT NULL,
                    nome VARCHAR(100) NOT NULL,
                    iva BOOLEAN DEFAULT FALSE,
                    valor BOOLEAN DEFAULT FALSE,
                    flag BOOLEAN DEFAULT FALSE,
                    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Novo Campo aqui!
                );
            """)
            conn.commit()

def db_criar_pedido(pedido, nome, iva, valor, flag):
    """Insere um novo registro no banco de dados."""
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO notas_avaliadas (pedido, nome, iva, valor, flag) 
                   VALUES (%s, %s, %s, %s, %s);""",
                (pedido, nome, iva, valor, flag)
            )
            conn.commit()
        
# Adicione isso no final do seu banco.py

def db_listar_pedidos():
    """Busca todos os pedidos registrados ordenados pelo ID mais recente."""
    with psycopg.connect(DB_CONFIG) as conn:
        # Usamos o dict_row para retornar as colunas como um dicionário Python (fácil de ler)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id, pedido, nome, iva, valor, flag, data_avaliacao FROM notas_avaliadas WHERE data_avaliacao >= CURRENT_DATE - INTERVAL '7 days';")
            
            return cur.fetchall()