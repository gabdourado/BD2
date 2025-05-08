from fastapi import APIRouter, HTTPException
from conecao import get_connection
from models import ReservaRequest


router = APIRouter(prefix="", tags=["PUT"])

""""  Altera uma reserva feita por um usuário específico. (PUT) """
@router.put("/alterar-reserva/{reserva_id}")
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