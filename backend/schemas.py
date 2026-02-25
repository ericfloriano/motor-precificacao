from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_admin: bool = False
    invite_code: Optional[str] = None

class UserUpdate(BaseModel):
    email: str
    password: Optional[str] = None
    full_name: str
    is_admin: bool

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    is_admin: bool
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PricingInput(BaseModel):
    data_precificacao: str
    nome_cliente: str
    nome_equipamento: str
    quantidade: int
    valor_tabela: float
    margem_negociacao_perc: float
    comissao_representante: bool
    percentual_comissao: float
    frete_tipo: str
    valor_frete: float
    estado_destino: str
    desconto_concedido_perc: float
    observacoes: Optional[str] = None
    protocolo_base: Optional[str] = None

class PricingHistoryOut(PricingInput):
    id: int
    owner_id: int
    protocolo: str
    created_at: datetime
    valor_margem: float
    valor_comissao: float
    base_calculo: float
    percentual_difal: float
    valor_difal: float
    valor_com_comissao: float
    valor_com_margem: float
    valor_venda_cheio: float
    valor_minimo_venda: float
    valor_com_desconto: float
    venda_unitario: float
    venda_total: float
    model_config = ConfigDict(from_attributes=True)
