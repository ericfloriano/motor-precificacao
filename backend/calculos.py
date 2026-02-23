# Tabela de DIFAL Base (Origem MG para UF Destino)
# Referência informada via planilha
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
    "MG": 0.0 # Operação interna
}

def precificar(data: dict) -> dict:
    quantidade = max(1, data.get("quantidade", 1))
    valor_tabela = data.get("valor_tabela", 0.0)
    margem_perc = data.get("margem_negociacao_perc", 0.0) / 100.0
    
    # 1. Valor da Margem
    valor_margem = valor_tabela * margem_perc
    
    # 2. Comissão
    tem_comissao = data.get("comissao_representante", False)
    perc_comissao = data.get("percentual_comissao", 0.0) / 100.0 if tem_comissao else 0.0
    valor_comissao = (valor_tabela + valor_margem) * perc_comissao
    
    # 3. Frete
    frete_tipo = data.get("frete_tipo", "FOB").upper()
    valor_frete = data.get("valor_frete", 0.0)
    frete_calculo = valor_frete if frete_tipo == "CIF" else 0.0
    
    # 4. Base de Cálculo
    # Base = Valor Tabela + Valor Margem + Valor Comissão + Valor Frete (Se CIF)
    base_calculo = valor_tabela + valor_margem + valor_comissao + frete_calculo
    
    # 5. DIFAL
    estado = data.get("estado_destino", "MG").upper()
    percentual_difal = DIFAL_TABLE.get(estado, 0.0)
    valor_difal = base_calculo * (percentual_difal / 100.0)
    
    # 6. Finais
    venda_unitario = base_calculo + valor_difal
    venda_total = venda_unitario * quantidade
    
    return {
        "valor_margem": round(valor_margem, 2),
        "valor_comissao": round(valor_comissao, 2),
        "base_calculo": round(base_calculo, 2),
        "percentual_difal": percentual_difal,
        "valor_difal": round(valor_difal, 2),
        "venda_unitario": round(venda_unitario, 2),
        "venda_total": round(venda_total, 2)
    }
