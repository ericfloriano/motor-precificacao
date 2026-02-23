import React, { useState, useEffect } from 'react';

export default function AdminDashboard({ token }) {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/admin/users`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Erro ao buscar usuários");
            const data = await res.json();
            setUsers(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handleDelete = async (userId) => {
        if (!window.confirm("Certeza que deseja deletar este usuário?")) return;
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/admin/users/${userId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Erro ao deletar");
            fetchUsers();
        } catch (err) {
            alert(err.message);
        }
    };

    const toggleAdminStatus = async (user) => {
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/admin/users/${user.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    email: user.email,
                    full_name: user.full_name,
                    is_admin: !user.is_admin
                })
            });
            if (!res.ok) throw new Error("Erro ao atualizar status");
            fetchUsers();
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="glass-panel animate-fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 style={{ margin: 0 }}>Gestão de Usuários (Admin)</h2>
                <button onClick={fetchUsers} className="btn btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}>Atualizar</button>
            </div>

            {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}

            {loading ? (
                <div>Carregando...</div>
            ) : (
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid var(--surface-border)', color: 'var(--text-secondary)' }}>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Nome</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>E-mail</th>
                                <th style={{ padding: '1rem', fontWeight: 500 }}>Cargo</th>
                                <th style={{ padding: '1rem', fontWeight: 500, textAlign: 'center' }}>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map(user => (
                                <tr key={user.id} style={{ borderBottom: '1px solid var(--surface-border)' }}>
                                    <td style={{ padding: '1rem' }}>{user.full_name}</td>
                                    <td style={{ padding: '1rem' }}>{user.email}</td>
                                    <td style={{ padding: '1rem' }}>
                                        <span style={{
                                            padding: '0.25rem 0.5rem',
                                            borderRadius: '4px',
                                            fontSize: '0.8rem',
                                            background: user.is_admin ? 'rgba(56, 189, 248, 0.2)' : 'rgba(255, 255, 255, 0.1)',
                                            color: user.is_admin ? 'var(--accent)' : 'var(--text-secondary)'
                                        }}>
                                            {user.is_admin ? 'Admin' : 'Consultor'}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem', display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                                        <button
                                            className="btn btn-secondary"
                                            style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
                                            onClick={() => toggleAdminStatus(user)}
                                        >
                                            {user.is_admin ? 'Remover Admin' : 'Tornar Admin'}
                                        </button>
                                        <button
                                            className="btn"
                                            style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem', background: 'rgba(239, 68, 68, 0.2)', color: '#ef4444' }}
                                            onClick={() => handleDelete(user.id)}
                                        >
                                            Deletar
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
