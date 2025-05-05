from pydantic import BaseModel

class ReservaRequest(BaseModel):
    usuario_id: int
    agenda_sessao_id: int
    assento_numero: str
