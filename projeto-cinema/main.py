from fastapi import FastAPI, HTTPException
from conecao import get_connection
from models import ReservaRequest, AssentoCreate, AssentoRemove, CadastraFilme, UsuarioCreate

app = FastAPI()

""" Boas Vindas da Aplicação :) (GET) """
@app.get("/")
def boas_vindas():
    return {"saudacao":"Olá, Professor!"}
    
""""  Adicionar um novo usuário no banco de dados. (POST) """
@app.post("/cadastrar-usuario")
def cadastrar_usuario(usuario: UsuarioCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO Usuarios (nome, email) VALUES (%s, %s)",
            (usuario.nome, usuario.email)
        )
        conn.commit()
        return {"mensagem": "Usuário cadastrado com sucesso!"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Lista as sessões com seus respectivos filmes. (GET) """
@app.get("/mostrar-sessoes")
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

"""  Listar assentos disponíveis para uma sessão específica. (GET) """
@app.get("/mostrar-assentos-disponiveis")
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

""" Reserva um assento para uma sessão específica. (POST) """
@app.post("/fazer-reserva")
def reservar_assento(reserva: ReservaRequest):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.begin()
        # Pegando o ID do Assento
        cursor.execute(""" 
        SELECT A.id FROM Assentos AS A 
        JOIN Sessoes AS S ON A.sala_id = S.sala_id 
        JOIN Agenda_Sessao AS AG ON AG.sessao_id = S.id 
        WHERE AG.id = %s AND A.numero = %s FOR UPDATE
        """, (reserva.agenda_sessao_id, reserva.assento_numero))
        
        resultado = cursor.fetchone()

        # Verificando se o assento é válido para uma dada sessão
        if not resultado:
            raise HTTPException(status_code=404, detail="Assento não encontrado para essa sessão.")
        
        assento_id = resultado[0]
        
        # Verificando se o assento não foi reservado para outra pessoa
        cursor.execute("""
        SELECT 1 FROM Reservas 
        WHERE agenda_sessao_id = %s AND assento_id = %s FOR UPDATE
        """, (reserva.agenda_sessao_id, assento_id))

        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Assento já reservado para essa sessão.")
        
        # Reserva o assento
        cursor.execute(""" 
        INSERT INTO Reservas (
            usuario_id,
            agenda_sessao_id,
            assento_id
        ) VALUES (
            %s,
            %s,
            %s
        );
        """, (reserva.usuario_id, reserva.agenda_sessao_id, assento_id))

        conn.commit()
        
        return {"mensagem": f"Assento {reserva.assento_numero} reservado com sucesso para a sessão {reserva.agenda_sessao_id}."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro na reserva: {e}")
    finally:
        cursor.close()
        conn.close()

""" Mostra todas as reservas de uma determinada sessão (GET) """
@app.get("/mostrar-reservas")
def mostrar_reservas():
    return {"status":"Vem air!"}

""""  Altera uma reserva feita por um usuário específico. (PUT) """
@app.put("/alterar-reserva/{reserva_id}")
def alterar_reserva(reserva_id: int, nova_reserva: ReservaRequest):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn.begin()

        # Verifica se a reserva existe
        cursor.execute("SELECT assento_id FROM Reservas WHERE id = %s", (reserva_id,))
        reserva_antiga = cursor.fetchone()
        if not reserva_antiga:
            raise HTTPException(status_code=404, detail="Reserva não encontrada.")

        # Busca o novo assento na nova sessão
        cursor.execute("""
            SELECT A.id FROM Assentos AS A
            JOIN Sessoes AS S ON A.sala_id = S.sala_id
            JOIN Agenda_Sessao AS AG ON AG.sessao_id = S.id
            WHERE AG.id = %s AND A.numero = %s FOR UPDATE
        """, (nova_reserva.agenda_sessao_id, nova_reserva.assento_numero))
        resultado = cursor.fetchone()

        if not resultado:
            raise HTTPException(status_code=404, detail="Assento não encontrado para essa sessão.")

        novo_assento_id = resultado[0]

        # Verifica se o novo assento já está reservado
        cursor.execute(""" 
        SELECT 1 FROM Reservas 
        WHERE agenda_sessao_id = %s AND assento_id = %s
        """, (nova_reserva.agenda_sessao_id, novo_assento_id))
        
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Novo assento já está reservado.")

        # Atualiza a reserva para o novo assento e sessão
        cursor.execute("""
            UPDATE Reservas 
            SET usuario_id = %s, agenda_sessao_id = %s, assento_id = %s 
            WHERE id = %s
        """, (nova_reserva.usuario_id, nova_reserva.agenda_sessao_id, novo_assento_id, reserva_id))

        conn.commit()
        return {"mensagem": f"Reserva {reserva_id} alterada com sucesso para o assento {nova_reserva.assento_numero}."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao alterar reserva: {e}")
    finally:
        cursor.close()
        conn.close()

""" Deleta uma reserva para uma sessão específica. (POST)  """
@app.delete("/deletar-reserva")
def deletar_reserva():
    return {"status":"Vem air!"}

""" Adicionar um novo assento em determinada sala """
@app.post("/adicionar_assento")
def adicionar_assento(create: AssentoCreate):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Vendo se o assento já existe
    cursor.execute("""
    SELECT 
    A.sala_id, 
    A.numero 
    FROM Assentos AS A 
    WHERE A.sala_id = %s AND A.numero = %s;
    """, (create.sala_id, create.assento_numero))
    
    resultado = cursor.fetchone()

    if not resultado:
        # Inserindo o assento novo
        cursor.execute("""
        INSERT INTO Assentos (
            sala_id, 
            numero
        ) VALUES(
            %s, 
            %s
        );
        """, (create.sala_id, create.assento_numero))
        conn.commit()
        return {"mensagem": f"Assento {create.assento_numero} adicionado na sala {create.sala_id}."}
    else:
        return {"mensagem": f"Assento {create.assento_numero} já existe na sala {create.sala_id}"}
        

""" Remover um determinado assento de determinada sala """
@app.delete("/remover-assento")
def remover_assento(remove: AssentoRemove):
    conn = get_connection()
    cursor = conn.cursor()

    # Vendo se o assento existe
    cursor.execute(""" 
    SELECT 
        A.sala_id, 
        A.numero 
    FROM Assentos AS A 
    WHERE A.sala_id = %s AND A.numero = %s;
    """, (remove.sala_id, remove.assento_numero))
    
    resultado = cursor.fetchone()

    if resultado:
        # Removendo o assento
        cursor.execute("""
        DELETE FROM Assentos 
        WHERE sala_id = %s AND numero = %s;
        """, (remove.sala_id, remove.assento_numero))
        conn.commit()
        return {"mensagem": f"Assento {remove.assento_numero} da sala {remove.sala_id} removido com sucesso."}
    else:
        return {"mensagem": f"Assento {remove.assento_numero} não encontrado na sala {remove.sala_id}."}
    
""""  Adicionar um novo filme no banco de dados. (POST) """
@app.post("/cadastrar-filme")
def cadastrar_filme(filme: CadastraFilme):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Filmes (
                titulo, 
                genero, 
                duracao, 
                formato
            ) VALUES (
                %s, 
                %s, 
                %s, 
                %s
            );
            """,
            (filme.titulo, filme.genero, filme.duracao, filme.formato))
        
        conn.commit()
        return {"mensagem": f"Filme '{filme.titulo}' cadastrado com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar filme: {e}")
    finally:
        cursor.close()
        conn.close()