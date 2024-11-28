import sqlite3
from screen import AmigoSecretoApp

def criar_tabelas():
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()

    # Tabela de participantes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    # Tabela de presentes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participante_id INTEGER,
            presente TEXT NOT NULL,
            FOREIGN KEY (participante_id) REFERENCES participantes (id)
        )
    """)

    # Tabela de mensagens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remetente_id INTEGER,
            destinatario_id INTEGER,
            mensagem TEXT NOT NULL,
            FOREIGN KEY (remetente_id) REFERENCES participantes (id),
            FOREIGN KEY (destinatario_id) REFERENCES participantes (id)
        )
    """)

    # Tabela de sorteios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sorteio (
            id_sorteio INTEGER PRIMARY KEY AUTOINCREMENT,
            id_part_sort INTEGER NOT NULL,
            id_part_pres INTEGER NOT NULL,
            dt_sorteio DATE DEFAULT (DATE('now')),
            FOREIGN KEY (id_part_sort) REFERENCES participantes (id),
            FOREIGN KEY (id_part_pres) REFERENCES participantes (id)
        )
    """)

    conn.commit()
    conn.close()


def adicionar_participante(nome):
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO participantes (nome) VALUES (?)", (nome,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Evitar nomes duplicados
    conn.close()

def obter_participantes():
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM participantes")
    participantes = cursor.fetchall()
    conn.close()
    return participantes

def cadastrar_presente(participante_id, presente):
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presentes (participante_id, presente) VALUES (?, ?)", (participante_id, presente))
    conn.commit()
    conn.close()
    
def registrar_sorteio(par_sort_id, par_pres_id):
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sorteio (id_part_sort, id_part_pres, dt_sorteio)
        VALUES (?, ?, DATE('now'))
    """, (par_sort_id, par_pres_id))
    conn.commit()
    conn.close()

def obter_sorteios():
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p1.nome AS sorteador, p2.nome AS presenteado, s.dt_sorteio
        FROM sorteio s
        JOIN participantes p1 ON s.id_part_sort = p1.id
        JOIN participantes p2 ON s.id_part_pres = p2.id
    """)
    sorteios = cursor.fetchall()
    conn.close()
    return sorteios

def enviar_mensagem(remetente_id, destinatario_id, mensagem):
    conn = sqlite3.connect("amigo_secreto.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mensagens (remetente_id, destinatario_id, mensagem) 
        VALUES (?, ?, ?)
    """, (remetente_id, destinatario_id, mensagem))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    app = AmigoSecretoApp(
        adicionar_participante,
        obter_participantes,
        cadastrar_presente,
        enviar_mensagem,
        registrar_sorteio,
        obter_sorteios
    )
    app.run()

