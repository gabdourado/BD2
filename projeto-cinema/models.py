from pydantic import BaseModel

class ReservaRequest(BaseModel):
    usuario_id: int
    agenda_sessao_id: int
    assento_numero: str

class AssentoCreate(BaseModel):
    sala_id: int
    assento_numero: str

class AssentoRemove(BaseModel):
    sala_id: int
    assento_numero: str

class CadastraFilme(BaseModel):
    titulo: str
    genero: str
    duracao: str
    formato: str