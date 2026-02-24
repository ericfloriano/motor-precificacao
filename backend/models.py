from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_admin = Column(Boolean, default=False)
    
    pricings = relationship("PricingHistory", back_populates="owner")

import pytz

def get_local_time():
    return datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))

class PricingHistory(Base):
    __tablename__ = "pricing_history"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    protocolo = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=get_local_time)
    
    # Inputs
    data_precificacao = Column(String)
    nome_cliente = Column(String, index=True)
    nome_equipamento = Column(String)
    quantidade = Column(Integer)
    valor_tabela = Column(Float)
    margem_negociacao_perc = Column(Float)
    comissao_representante = Column(Boolean)
    percentual_comissao = Column(Float)
    frete_tipo = Column(String)
    valor_frete = Column(Float)
    estado_destino = Column(String)
    
    # Outputs
    valor_margem = Column(Float)
    valor_comissao = Column(Float)
    valor_com_comissao = Column(Float)
    valor_com_margem = Column(Float)
    base_calculo = Column(Float)
    percentual_difal = Column(Float)
    valor_difal = Column(Float)
    venda_unitario = Column(Float)
    venda_total = Column(Float)
    
    # Novas regras (Trava & Desconto)
    valor_venda_cheio = Column(Float)
    valor_minimo_venda = Column(Float)
    desconto_concedido_perc = Column(Float, default=0.0)
    valor_com_desconto = Column(Float)

    owner = relationship("User", back_populates="pricings")
