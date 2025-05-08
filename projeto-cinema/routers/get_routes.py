from fastapi import APIRouter
from conecao import get_connection

router = APIRouter(prefix="", tags=["GET"])

@router.get("/")
def boas_vindas():
    return {"saudacao": "Olá, Professor!"}

@router.get("/mostrar-sessoes")
def listar_filmes_sessao():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
    SELECT 
        A.data_sessao, 
        Sa.nome, 
        Se.horario_padrao, 
        F.titulo, 
        F.duracao, 
        F.formato, 
        Se.preco  
    FROM Filmes AS F 
    JOIN Sessoes AS Se ON F.id = Se.filme_id 
    JOIN Salas AS Sa ON Se.sala_id = Sa.id 
    JOIN Agenda_Sessao AS A ON A.sessao_id = Se.id 
    ORDER BY data_sessao;
    """)
    
    resultados = cursor.fetchall()
    sessoes = []
    for linha in resultados:
        sessoes.append({
            "Data_Sessao":linha[0],
            "Nome_Sala":linha[1],
            "Horario": linha[2],
            "Filme": linha[3],
            "Duracao": linha[4],
            "Formato":linha[5],
            "Preco":linha[6]
        })
    cursor.close()
    conn.close()
    return {"assentos": sessoes}

@router.get("/mostrar-assentos-disponiveis")
def mostrar_assentos_disponiveis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT 
                AG.id AS agenda_sessao_id,
                S.sala_id,
                A.numero AS assento_numero
            FROM Agenda_Sessao AS AG
            JOIN Sessoes AS S ON AG.sessao_id = S.id
            JOIN Assentos AS A ON S.sala_id = A.sala_id
            WHERE (AG.id, A.id) NOT IN (
                SELECT agenda_sessao_id, assento_id
                FROM Reservas
            )
            ORDER BY AG.id, A.numero;
        """)
        
    respostas = cursor.fetchall()
    dados = []
    for resposta in respostas:
        dados.append({
            "Agenda_Sessao":resposta[0],
            "Sala_ID":resposta[1],
            "Assento":resposta[2]
        })
    cursor.close()
    conn.close()
    return {"dados": dados}

@router.get("/mostrar-reservas")
def mostrar_reservas():
    return {"status": "Vem air!"}
