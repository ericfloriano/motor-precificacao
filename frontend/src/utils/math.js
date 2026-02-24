export const DIFAL_TABLE = {
    PR: 7.5, RS: 5.0, SC: 5.0, ES: 10.0, RJ: 10.0, SP: 6.0,
    DF: 13.0, GO: 12.0, MT: 10.0, MS: 10.0, AL: 13.0, BA: 13.5,
    CE: 13.0, MA: 16.0, PB: 13.0, PE: 13.5, PI: 15.5, RN: 13.0,
    SE: 13.0, AC: 12.0, AP: 11.0, AM: 13.0, PA: 12.0, RO: 12.5,
    RR: 13.0, TO: 13.0, MG: 0.0
};

export function calculatePricing(data) {
    const quantidade = Math.max(1, Number(data.quantidade) || 1);
    const valor_tabela_original = Number(data.valor_tabela) || 0.0;

    // Frete
    const frete_tipo = data.frete_tipo || "FOB";
    const valor_frete = Number(data.valor_frete) || 0.0;
    const frete_calculo = frete_tipo === "CIF" ? valor_frete : 0.0;

    // 0. Base Custo
    const valor_tabela = valor_tabela_original + frete_calculo;

    // 1. Comissão
    const tem_comissao = data.comissao_representante;
    const perc_comissao = tem_comissao ? (Number(data.percentual_comissao) || 0.0) / 100.0 : 0.0;
    const valor_comissao = valor_tabela * perc_comissao;
    const valor_com_comissao = valor_tabela + valor_comissao;

    // 2. Margem
    const margem_perc = (Number(data.margem_negociacao_perc) || 0.0) / 100.0;
    const valor_margem = valor_tabela * margem_perc;
    const valor_com_margem = valor_com_comissao + valor_margem;

    // 3. DIFAL
    const estado = data.estado_destino || "MG";
    const percentual_difal = DIFAL_TABLE[estado] || 0.0;
    const valor_difal = valor_com_margem * (percentual_difal / 100.0);

    // 4. Venda Cheio (Máximo)
    const valor_venda_cheio = valor_com_margem + valor_difal;

    // 5. Mínimo Permitido
    const valor_minimo_venda = valor_com_comissao + (valor_com_comissao * (percentual_difal / 100.0));

    // Desconto Automático (Máximo Permitido %)
    let desconto_maximo_perc = 0;
    if (valor_venda_cheio > 0) {
        desconto_maximo_perc = ((valor_venda_cheio - valor_minimo_venda) / valor_venda_cheio) * 100;
    }

    // 6. Desconto Aplicado
    const desconto_concedido_perc = (Number(data.desconto_concedido_perc) || 0.0) / 100.0;
    const valor_com_desconto = valor_venda_cheio - (valor_venda_cheio * desconto_concedido_perc);

    const venda_unitario = valor_com_desconto;
    const venda_total = venda_unitario * quantidade;

    return {
        valor_margem,
        valor_comissao,
        valor_com_comissao,
        valor_com_margem,
        base_calculo: valor_com_margem,
        percentual_difal,
        valor_difal,
        valor_venda_cheio,
        valor_minimo_venda,
        desconto_maximo_perc,
        valor_com_desconto,
        venda_unitario,
        venda_total
    };
}

export const formatCurrency = (val) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
};

export const formatPercent = (val) => {
    return new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 }).format(val) + '%';
};
