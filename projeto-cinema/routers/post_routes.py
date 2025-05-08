from fastapi import APIRouter, HTTPException
from conecao import get_connection
from models import ReservaRequest, AssentoCreate, AssentoRemove, CadastraFilme, UsuarioCreate, RemoveReserva

router = APIRouter(prefix="", tags=["POST"])

@router.post("/cadastrar-usuario")
def cadastrar_usuario(usuario: UsuarioCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()

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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@router.post("/fazer-reserva")
def reservar_assento(reserva: ReservaRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@router.post("/adicionar_assento")
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
        return {"mensagem": f"Assento {create.assento_numero} já foi adicionado na sala {create.sala_id}"}

@router.post("/cadastrar-filme")
def cadastrar_filme(filme: CadastraFilme):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
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
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()