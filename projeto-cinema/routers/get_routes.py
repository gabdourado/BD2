from fastapi import APIRouter, HTTPException
from conecao import get_connection

router = APIRouter(prefix="", tags=["GET"])

@router.get("/")
def boas_vindas():
    return {"saudacao": "Olá, Professor!"}

@router.get("/mostrar-sessoes")
def listar_filmes_sessao():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(""" 
        SELECT 
            A.id,
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
        ORDER BY A.data_sessao, A.id;
        """)
        
        resposta = cursor.fetchall()

        if not resposta:
            raise HTTPException(status_code=404,  detail="Nenhuma sessao encontrada")
        
        sessoes = []
        for linha in resposta:
            sessoes.append({
                "agenda_sessao_id": linha[0],
                "data_sessao":linha[1],
                "nome_sala":linha[2],
                "horario": linha[3],
                "Filme": linha[4],
                "duracao": linha[5],
                "formato":linha[6],
                "preco": float(linha[7])
            })

        return {"sessoes": sessoes}
    
    except HTTPException:
            raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar sessoes: {str(e)}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@router.get("/mostrar-assentos-disponiveis")
def mostrar_assentos_disponiveis():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                SELECT 
                    AG.id,
                    AG.data_sessao,
                    Se.horario_padrao,
                    Sa.nome,
                    Ass.numero
                FROM Agenda_Sessao AS AG
                JOIN Sessoes AS Se ON AG.sessao_id = Se.id
                JOIN Assentos AS Ass ON Se.sala_id = Ass.sala_id
                JOIN Salas AS Sa ON Ass.sala_id = Sa.id
                WHERE (AG.id, Ass.id) NOT IN (
                    SELECT agenda_sessao_id, assento_id
                    FROM Reservas
                )
                ORDER BY AG.id, Ass.numero;
            """)
            
        resposta = cursor.fetchall()

        if not resposta:
            raise HTTPException(status_code=404,  detail="Nenhuma assento encontrado")
        
        assentos = []
        for linha in resposta:
            assentos.append({
                "agenda_sessao":linha[0],
                "data": linha[1],
                "horario": linha[2],
                "sala":linha[3],
                "assento":linha[4]
            })

        return {"assentos": assentos}
    
    except HTTPException:
            raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar assentos: {str(e)}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@router.get("/mostrar-reservas")
def mostrar_reservas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
        SELECT 
            R.id,
            U.nome,
            F.titulo,
            A.data_sessao,
            Se.horario_padrao,
            Sa.nome,
            Ass.numero
        FROM Reservas AS R
        JOIN Usuarios AS U ON R.usuario_id = U.id
        JOIN Agenda_Sessao AS A ON R.agenda_sessao_id = A.id
        JOIN Sessoes AS Se ON A.sessao_id = Se.id
        JOIN Filmes AS F ON Se.filme_id = F.id
        JOIN Salas AS Sa ON Se.sala_id = Sa.id
        JOIN Assentos AS Ass ON R.assento_id = Ass.id
        ORDER BY A.data_sessao, Se.horario_padrao;
    """)
    
        resposta = cursor.fetchall()
        
        if not resposta:
            raise HTTPException(status_code=404, detail="Nenhuma reserva encontrada.")
        
        reservas = []
        for linha in resposta:
            reservas.append({
                "id_reserva": linha[0],
                "nome_usuario": linha[1],
                "filme": linha[2],
                "data": linha[3],
                "horario": linha[4],
                "sala": linha[5],
                "assento": linha[6]
            })
        
        return {"reservas": reservas}

    except HTTPException:
            raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar sessões: {str(e)}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()