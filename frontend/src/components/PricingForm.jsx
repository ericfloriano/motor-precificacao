import React, { useState, useEffect } from 'react';
import { calculatePricing, formatCurrency, formatPercent, DIFAL_TABLE } from '../utils/math';

const getLocalDateString = () => {
    const d = new Date();
    return new Date(d.getTime() - (d.getTimezoneOffset() * 60000)).toISOString().split('T')[0];
};

const initialForm = {
    data_precificacao: getLocalDateString(),
    nome_cliente: '',
    nome_equipamento: '',
    quantidade: 1,
    valor_tabela: '',
    margem_negociacao_perc: '',
    comissao_representante: false,
    percentual_comissao: '',
    frete_tipo: 'FOB',
    valor_frete: '',
    estado_destino: 'SP'
};

export default function PricingForm() {
    const [form, setForm] = useState(initialForm);
    const metrics = calculatePricing(form);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        let finalVal = type === 'checkbox' ? checked : value;

        // Keep string format from HTML input instead of parsing prematurely
        // Float inputs in javascript forms sometimes lose precise string decimal dots when cast to Number randomly
        setForm(prev => {
            let nextForm = { ...prev, [name]: finalVal };
            // Rule: if no comissao, reset percentual
            if (name === 'comissao_representante' && !checked) {
                nextForm.percentual_comissao = '';
            }
            return nextForm;
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage(null);
        try {
            // Setup backend integration here
            const token = localStorage.getItem('token');
            const payload = { ...form };

            // Ensure precise floats before submitting
            const numberFields = ['valor_tabela', 'margem_negociacao_perc', 'percentual_comissao', 'valor_frete'];
            numberFields.forEach(field => {
                if (payload[field] === '') {
                    payload[field] = 0;
                } else {
                    payload[field] = parseFloat(payload[field]);
                }
            });
            payload.quantidade = parseInt(payload.quantidade) || 1;

            const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/calculate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });
            if (!res.ok) throw new Error("Erro na API");
            const data = await res.json();
            setMessage({ type: 'success', text: `Cotação salva com sucesso! Protocolo: ${data.data.protocolo}` });

            // Note: intentionally not clearing the form to allow easy re-quotes 
            // but the success message shows the saved protocol
        } catch (error) {
            console.error(error);
            setMessage({ type: 'error', text: 'Erro ao conectar com servidor' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="grid-2-col">
            <div className="glass-panel animate-fade-in">
                <h2>Entrada de Dados</h2>
                <form onSubmit={handleSubmit}>

                    <div className="input-group">
                        <label>Data da Precificação *</label>
                        <input type="date" name="data_precificacao" value={form.data_precificacao} onChange={handleChange} required />
                    </div>

                    <div className="input-group">
                        <label>Nome do Cliente *</label>
                        <input type="text" name="nome_cliente" value={form.nome_cliente} onChange={handleChange} required placeholder="Ex: Hospital D'Or" />
                    </div>

                    <div className="input-group">
                        <label>Equipamento *</label>
                        <input type="text" name="nome_equipamento" value={form.nome_equipamento} onChange={handleChange} required placeholder="Ex: ReCARE Plus 12CH" />
                    </div>

                    <div className="input-group">
                        <label>Quantidade *</label>
                        <input type="number" name="quantidade" min="1" value={form.quantidade} onChange={handleChange} required />
                    </div>

                    <div className="input-group">
                        <label>Valor de Tabela (R$) *</label>
                        <input type="number" step="0.01" name="valor_tabela" value={form.valor_tabela} onChange={handleChange} required placeholder="Ex: Informe o valor unitário base" />
                    </div>

                    <div className="input-group">
                        <label>Margem para Negociação (%) *</label>
                        <input type="number" step="0.1" name="margem_negociacao_perc" value={form.margem_negociacao_perc} onChange={handleChange} required placeholder="Ex: Informe o percentual de margem desejada" />
                    </div>

                    <div className="input-group" style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                        <label>Comissão Representante</label>
                        <label className="toggle-switch">
                            <input type="checkbox" name="comissao_representante" checked={form.comissao_representante} onChange={handleChange} />
                            <span className="slider"></span>
                        </label>
                    </div>

                    {form.comissao_representante && (
                        <div className="input-group animate-fade-in">
                            <label>Percentual de Comissão (%) *</label>
                            <input type="number" step="0.1" name="percentual_comissao" value={form.percentual_comissao} onChange={handleChange} required placeholder="Ex: Informe o percentual de comissão" />
                        </div>
                    )}

                    <div className="input-group">
                        <label>Frete *</label>
                        <select name="frete_tipo" value={form.frete_tipo} onChange={handleChange} required>
                            <option value="FOB">FOB (Por conta do cliente)</option>
                            <option value="CIF">CIF (Incluso)</option>
                        </select>
                    </div>

                    {form.frete_tipo === 'CIF' && (
                        <div className="input-group animate-fade-in">
                            <label>Valor do Frete (R$) *</label>
                            <input type="number" step="0.01" name="valor_frete" value={form.valor_frete} onChange={handleChange} required placeholder="Ex: Valor total do frete" />
                        </div>
                    )}

                    <div className="input-group">
                        <label>Estado de Destino *</label>
                        <select name="estado_destino" value={form.estado_destino} onChange={handleChange} required>
                            {Object.keys(DIFAL_TABLE).sort().map(uf => (
                                <option key={uf} value={uf}>{uf} - {formatPercent(DIFAL_TABLE[uf])} DIFAL</option>
                            ))}
                        </select>
                    </div>

                    {message && (
                        <div style={{ padding: '1rem', marginBottom: '1rem', borderRadius: '8px', background: message.type === 'success' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)', color: message.type === 'success' ? '#10b981' : '#ef4444' }}>
                            {message.text}
                        </div>
                    )}

                    <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }} disabled={loading}>
                        {loading ? 'Salvando...' : 'Salvar Cotação'}
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
                    </button>
                </form>
            </div>

            <div className="glass-panel animate-fade-in" style={{ position: 'sticky', top: '100px', height: 'fit-content' }}>
                <h2>Resumo da Precificação</h2>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                        <span>Valor Unitário da Margem:</span>
                        <span>{formatCurrency(metrics.valor_margem)}</span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                        <span>Valor da Comissão (Unitário):</span>
                        <span>{formatCurrency(metrics.valor_comissao)}</span>
                    </div>

                    {form.frete_tipo === 'CIF' && (
                        <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                            <span>Valor do Frete (Adicionado):</span>
                            <span>{formatCurrency(form.valor_frete || 0)}</span>
                        </div>
                    )}

                    <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1rem' }}>
                        <span style={{ fontWeight: 600 }}>Base de Cálculo:</span>
                        <span style={{ fontWeight: 600 }}>{formatCurrency(metrics.base_calculo)}</span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                        <span>Aliquota DIFAL ({form.estado_destino}):</span>
                        <span>{formatPercent(metrics.percentual_difal)}</span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', color: '#ef4444' }}>
                        <span>Valor do Imposto (DIFAL):</span>
                        <span>{formatCurrency(metrics.valor_difal)}</span>
                    </div>

                    <div className="result-card">
                        <div style={{ color: 'var(--text-primary)', marginBottom: '0.5rem', fontWeight: 600 }}>Valor Unitário de Venda</div>
                        <div className="result-value">{formatCurrency(metrics.venda_unitario)}</div>

                        <div style={{ color: 'var(--text-secondary)', marginTop: '1.5rem', marginBottom: '0.5rem', fontSize: '0.9rem' }}>Valor Total (x{form.quantidade})</div>
                        <div className="result-value" style={{ fontSize: '1.5rem', color: 'var(--text-primary)' }}>
                            {formatCurrency(metrics.venda_total)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
