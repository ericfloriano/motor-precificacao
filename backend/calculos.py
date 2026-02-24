# Base DIFAL Table (Origin: Minas Gerais [MG] to Destination State [UF])
# These reference values are provided by the official tax spreadsheet
DIFAL_TABLE = {
    "PR": 7.50,
    "RS": 5.0,
    "SC": 5.0,
    "ES": 10.0,
    "RJ": 10.0,
    "SP": 6.0,
    "DF": 13.0,
    "GO": 12.0,
    "MT": 10.0,
    "MS": 10.0,
    "AL": 13.0,
    "BA": 13.50,
    "CE": 13.0,
    "MA": 16.0,
    "PB": 13.0,
    "PE": 13.50,
    "PI": 15.50,
    "RN": 13.0,
    "SE": 13.0,
    "AC": 12.0,
    "AP": 11.0,
    "AM": 13.0,
    "PA": 12.0,
    "RO": 12.50,
    "RR": 13.0,
    "TO": 13.0,
    "MG": 0.0 # Internal operation (Same state)
}

def precificar(data: dict) -> dict:
    quantidade = max(1, data.get("quantidade", 1))
    valor_tabela_original = data.get("valor_tabela", 0.0)
    
    # Frete compõe o Custo Base
    frete_tipo = data.get("frete_tipo", "FOB").upper()
    valor_frete = data.get("valor_frete", 0.0)
    frete_calculo = valor_frete if frete_tipo == "CIF" else 0.0
    
    # 0. Custo Base (Equipamento + Frete)
    valor_tabela = valor_tabela_original + frete_calculo
    
    # 1. Comissão (Linear sobre a Tabela+Frete)
    tem_comissao = data.get("comissao_representante", False)
    perc_comissao = data.get("percentual_comissao", 0.0) / 100.0 if tem_comissao else 0.0
    valor_comissao = valor_tabela * perc_comissao
    valor_com_comissao = valor_tabela + valor_comissao
    
    # 2. Margem (Linear sobre a Tabela+Frete)
    margem_perc = data.get("margem_negociacao_perc", 0.0) / 100.0
    valor_margem = valor_tabela * margem_perc
    valor_com_margem = valor_com_comissao + valor_margem
    
    # 3. DIFAL
    estado = data.get("estado_destino", "MG").upper()
    percentual_difal = DIFAL_TABLE.get(estado, 0.0)
    valor_difal = valor_com_margem * (percentual_difal / 100.0)
    
    # 4. Total Cheio (Max Price)
    valor_venda_cheio = valor_com_margem + valor_difal
    
    # 5. Valor Mínimo Permitido (Mínimo p/ Lucidez da Operação)
    # Regra: Base Total (comissão + frete + equipamento) + DIFAL em cima disso.
    valor_minimo_venda = valor_com_comissao + (valor_com_comissao * (percentual_difal / 100.0))
    
    # 6. Desconto Concedido
    desconto_concedido_perc = data.get("desconto_concedido_perc", 0.0) / 100.0
    valor_com_desconto = valor_venda_cheio - (valor_venda_cheio * desconto_concedido_perc)
    
    venda_total = valor_com_desconto * quantidade
    
    return {
        "valor_margem": round(valor_margem, 2),
        "valor_comissao": round(valor_comissao, 2),
        "valor_com_comissao": round(valor_com_comissao, 2),
        "valor_com_margem": round(valor_com_margem, 2),
        "base_calculo": round(valor_com_margem, 2),
        "percentual_difal": percentual_difal,
        "valor_difal": round(valor_difal, 2),
        "valor_venda_cheio": round(valor_venda_cheio, 2),
        "valor_minimo_venda": round(valor_minimo_venda, 2),
        "valor_com_desconto": round(valor_com_desconto, 2),
        "venda_unitario": round(valor_com_desconto, 2),
        "venda_total": round(venda_total, 2)
    }
