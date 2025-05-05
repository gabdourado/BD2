from fastapi import FastAPI, HTTPException
from conecao import get_connection
from models import ReservaRequest

app = FastAPI()

""" Listando os filmes e suas sessões por data """
@app.get("/sessoes")
def listar_filmes_sessao():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT A.data_sessao, Se.horario_padrao, Sa.nome, F.titulo, F.duracao, F.formato, Se.preco  FROM Filmes AS F  JOIN Sessoes AS Se ON F.id = Se.filme_id JOIN Salas AS Sa ON Se.sala_id = Sa.id JOIN Agenda_Sessao AS A ON A.sessao_id = Se.id ORDER BY data_sessao;")
    resultados = cursor.fetchall()
    sessoes = []
    for linha in resultados:
        sessoes.append({
            "Data_Sessao":linha[0],
            "Horario": linha[1],
            "Nome_Sala":linha[2],
            "Filme": linha[3],
            "Duracao": linha[4],
            "Formato":linha[5],
            "Preco":linha[6]
        })
    cursor.close()
    conn.close()
    return {"assentos": sessoes}

""" Listar os assentos disponíveis dada uma sessão (Filme, Horário e Data) """
@app.get("/assentos")
def listar_assentos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT S.nome, A.numero, A.reservado FROM Assentos AS A JOIN Salas AS S ON S. ORDER BY S.id;")
    resultados = cursor.fetchall()
    assentos = []
    for linha in resultados:
        assentos.append({
            "Nome_Sala": linha[0],
            "Numero_Assento": linha[1],
            "Status": bool(linha[2])
        })
    cursor.close()
    conn.close()
    return {"assentos": assentos}

""""  Realizar uma reserva de um assento dada uma sessão (Filme, Data e Hora) """
@app.post("/reservar")
def reservar_assento(reserva: ReservaRequest):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.begin()
        # Pegando o ID do Assento
        cursor.execute("SELECT A.id FROM Assentos AS A JOIN Sessoes AS S ON A.sala_id = S.sala_id JOIN Agenda_Sessao AS AG ON AG.sessao_id = S.id WHERE AG.id = %s AND A.numero = %s FOR UPDATE", (reserva.agenda_sessao_id, reserva.assento_numero))
        resultado = cursor.fetchone()

        # Verificando se o assento é válido para uma dada sessão
        if not resultado:
            raise HTTPException(status_code=404, detail="Assento não encontrado para essa sessão.")
        
        assento_id = resultado[0]
        
        # Verificando se o assento não foi reservado para outra pessoa
        cursor.execute("SELECT 1 FROM Reservas WHERE agenda_sessao_id = %s AND assento_id = %s FOR UPDATE", (reserva.agenda_sessao_id, assento_id))

        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Assento já reservado para essa sessão.")
        
        # Reserva o assento
        cursor.execute("INSERT INTO Reservas (usuario_id, agenda_sessao_id, assento_id) VALUES (%s, %s, %s)", (reserva.usuario_id, reserva.agenda_sessao_id, assento_id))

        conn.commit()
        
        return {"mensagem": f"Assento {reserva.assento_numero} reservado com sucesso para a sessão {reserva.agenda_sessao_id}."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro na reserva: {e}")
    finally:
        cursor.close()
        conn.close()
