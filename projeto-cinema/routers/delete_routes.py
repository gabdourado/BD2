from fastapi import APIRouter, HTTPException
from conecao import get_connection
from models import AssentoRemove, RemoveReserva


router = APIRouter(prefix="", tags=["DELETE"])

@router.delete("/remover-assento")
def remover_assento(remove: AssentoRemove):
    conn = get_connection()
    cursor = conn.cursor()

    # Vendo se o assento existe
    cursor.execute(""" 
    SELECT 
        A.id,
        A.sala_id, 
        A.numero 
    FROM Assentos AS A 
    WHERE A.sala_id = %s AND A.numero = %s;
    """, (remove.sala_id, remove.assento_numero))
    
    resultado = cursor.fetchone()

    if resultado:
        assento_id = resultado[0]

        # Verificando se o assento está vinculado a alguma reserva
        cursor.execute("""
            SELECT 1 FROM Reservas WHERE assento_id = %s LIMIT 1;
        """, (assento_id,))
        
        reserva_existente = cursor.fetchone()
        if reserva_existente:
            return {
                "erro": f"O assento {remove.assento_numero} da sala {remove.sala_id} está reservado e não pode ser removido."
            }
        # Removendo o assento
        cursor.execute("""
        DELETE FROM Assentos 
        WHERE sala_id = %s AND numero = %s;
        """, (remove.sala_id, remove.assento_numero))
        conn.commit()

        return {"mensagem": f"Assento {remove.assento_numero} da sala {remove.sala_id} removido com sucesso."}
    else:
        return {"mensagem": f"Assento {remove.assento_numero} não encontrado na sala {remove.sala_id}."}

@router.delete("/deletar-reserva")
def deletar_reserva(remove: RemoveReserva):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Pegando o ID do assento
        cursor.execute("""
            SELECT id FROM Assentos WHERE numero = %s;
        """, (remove.assento_numero,))
        row = cursor.fetchone()

        if not row:
            return {'erro': "Assento inexistente."}
        
        assento_id = row[0]

        # Verifica se há reserva para esse assento na sessão e pelo usuário
        cursor.execute("""
            SELECT 1 FROM Reservas 
            WHERE usuario_id = %s AND agenda_sessao_id = %s AND assento_id = %s;
        """, (remove.usuario_id, remove.agenda_sessao_id, assento_id))

        if not cursor.fetchone():
            return {'erro': "Não há ninguém com essa reserva."}

        # Remove a reserva
        cursor.execute("""
            DELETE FROM Reservas 
            WHERE usuario_id = %s AND agenda_sessao_id = %s AND assento_id = %s;
        """, (remove.usuario_id, remove.agenda_sessao_id, assento_id))
        
        conn.commit()

        return {'mensagem': "Reserva cancelada com sucesso."}

    except Exception as e:
        conn.rollback()
        return {'erro': f"Erro ao cancelar reserva: {str(e)}"}
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()