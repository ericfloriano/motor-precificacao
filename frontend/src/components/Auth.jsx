import React, { useState } from 'react';

export default function Auth({ onLogin }) {
    const [isLogin, setIsLogin] = useState(true);
    const [form, setForm] = useState({ email: '', password: '', full_name: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const endpoint = isLogin ? '/api/v1/auth/token' : '/api/v1/auth/register';

            const payload = isLogin
                ? { email: form.email, password: form.password, full_name: "admin", is_admin: false }
                : { email: form.email, password: form.password, full_name: form.full_name, is_admin: false };

            const res = await fetch(`http://localhost:8000${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || "Erro de autenticação");
            }

            if (isLogin) {
                localStorage.setItem('token', data.access_token);
                onLogin(data.access_token);
            } else {
                // Automatically login after register
                const loginRes = await fetch(`http://localhost:8000/api/v1/auth/token`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: form.email, password: form.password, full_name: "admin", is_admin: false })
                });
                const loginData = await loginRes.json();
                localStorage.setItem('token', loginData.access_token);
                onLogin(loginData.access_token);
            }

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container" style={{ maxWidth: '500px', marginTop: '10vh' }}>
            <div className="glass-panel animate-fade-in">
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Motor Precificação</h1>
                    <p style={{ color: 'var(--text-secondary)' }}>Acesso restrito a consultores autorizados</p>
                </div>

                <form onSubmit={handleSubmit}>
                    {!isLogin && (
                        <div className="input-group">
                            <label>Nome Completo</label>
                            <input
                                type="text"
                                value={form.full_name}
                                onChange={e => setForm({ ...form, full_name: e.target.value })}
                                required
                            />
                        </div>
                    )}
                    <div className="input-group">
                        <label>E-mail Corporativo</label>
                        <input
                            type="email"
                            value={form.email}
                            onChange={e => setForm({ ...form, email: e.target.value })}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label>Senha</label>
                        <input
                            type="password"
                            value={form.password}
                            onChange={e => setForm({ ...form, password: e.target.value })}
                            required
                        />
                    </div>

                    {error && <div style={{ color: 'var(--error)', marginBottom: '1rem', fontSize: '0.9rem' }}>{error}</div>}

                    <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
                        {loading ? 'Aguarde...' : (isLogin ? 'Entrar no Sistema' : 'Criar Conta')}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
                    <button
                        className="btn btn-secondary"
                        style={{ border: 'none', fontSize: '0.9rem' }}
                        onClick={() => setIsLogin(!isLogin)}
                    >
                        {isLogin ? 'Não tem conta? Registre-se aqui' : 'Já tem conta? Faça Login'}
                    </button>
                </div>
            </div>
        </div>
    );
}
