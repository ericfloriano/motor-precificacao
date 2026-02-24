import React, { useState, useEffect } from 'react';
import { formatCurrency, formatPercent } from '../utils/math';

export default function HistoryDashboard({ isAdmin }) {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchHistory = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/history`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Erro ao buscar histórico");
            const data = await res.json();
            setHistory(data);
        } catch (err) {
            console.error(err);
            setError("Falha ao carregar histórico. Verifique se a API está rodando.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const handleExport = (id, format) => {
        // format can be 'pdf' or 'excel'
        window.open(`${import.meta.env.VITE_API_URL}/api/v1/export/${format}/${id}`, '_blank');
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Certeza que deseja deletar esta cotação?")) return;
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/history/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Erro ao deletar cotação");
            fetchHistory();
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="glass-panel animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ margin: 0, border: 'none', padding: 0 }}>Histórico de Cotações</h2>
                <button onClick={fetchHistory} className="btn btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}>Atualizar</button>
            </div>

            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}

            {loading ? (
                <div>Carregando...</div>
            ) : (
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid var(--surface-border)', color: 'var(--text-secondary)' }}>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Data</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Protocolo</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Responsável</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Cliente</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Equipamento</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Venda Total</th>
                                <th style={{ padding: '1rem', fontWeight: 500, textAlign: 'center' }}>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.length === 0 ? (
                                <tr>
                                    <td colSpan="7" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                                        Nenhuma cotação encontrada.
                                    </td>
                                </tr>
                            ) : (
                                history.map(item => (
                                    <tr key={item.id} style={{ borderBottom: '1px solid var(--surface-border)' }}>
                                        <td style={{ padding: '1rem' }}>{item.data_precificacao}</td>
                                        <td style={{ padding: '1rem', fontFamily: 'monospace', color: 'var(--accent)' }}>{item.protocolo}</td>
                                        <td style={{ padding: '1rem' }}>{item.owner_name}</td>
                                        <td style={{ padding: '1rem' }}>{item.nome_cliente}</td>
                                        <td style={{ padding: '1rem' }}>{item.nome_equipamento} (x{item.quantidade})</td>
                                        <td style={{ padding: '1rem', color: 'var(--success)', fontWeight: 600 }}>{formatCurrency(item.venda_total)}</td>
                                        <td style={{ padding: '1rem', display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                                            <button className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }} onClick={() => handleExport(item.id, 'pdf')}>
                                                PDF
                                            </button>
                                            <button className="btn btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }} onClick={() => handleExport(item.id, 'excel')}>
                                                XLSX
                                            </button>
                                            {isAdmin && (
                                                <button className="btn" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem', backgroundColor: 'transparent', color: 'var(--error)', border: '1px solid var(--error)' }} onClick={() => handleDelete(item.id)}>
                                                    DEL
                                                </button>
                                            )}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
