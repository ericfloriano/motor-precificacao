import React, { useState, useEffect } from 'react';
import PricingForm from './components/PricingForm';
import HistoryDashboard from './components/HistoryDashboard';
import AdminDashboard from './components/AdminDashboard';
import Auth from './components/Auth';

function App() {
    const [view, setView] = useState('pricing');
    const [session, setSession] = useState(null); // { token, user: { is_admin } }
    const [quoteToEdit, setQuoteToEdit] = useState(null);

    const handleLogin = (token) => {
        fetch(`${import.meta.env.VITE_API_URL}/api/v1/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(res => {
                if (!res.ok) throw new Error("Token Invalido");
                return res.json();
            })
            .then(user => setSession({ token, user }))
            .catch(() => handleLogout());
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) handleLogin(token);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        setSession(null);
    };

    if (!session || !session.user) {
        return <Auth onLogin={handleLogin} />;
    }

    return (
        <div className="app-container">
            <nav className="navbar" style={{ marginBottom: '2rem', borderRadius: '12px' }}>
                <div className="nav-logo">
                    <span style={{ color: 'var(--accent)' }}>Motor</span> Precificação
                </div>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <button
                        className="btn btn-secondary"
                        style={{ borderColor: view === 'pricing' ? 'var(--accent)' : 'var(--surface-border)' }}
                        onClick={() => { setQuoteToEdit(null); setView('pricing'); }}
                    >
                        Nova Cotação
                    </button>
                    <button
                        className="btn btn-secondary"
                        style={{ borderColor: view === 'history' ? 'var(--accent)' : 'var(--surface-border)' }}
                        onClick={() => setView('history')}
                    >
                        Meu Histórico
                    </button>
                    {session.user.is_admin && (
                        <button
                            className="btn btn-secondary"
                            style={{ borderColor: view === 'admin' ? 'var(--accent)' : 'var(--surface-border)' }}
                            onClick={() => setView('admin')}
                        >
                            Gestão de Usuários
                        </button>
                    )}
                    <button
                        className="btn"
                        style={{ color: 'var(--error)', background: 'transparent', border: 'none', marginLeft: '1rem' }}
                        onClick={handleLogout}
                    >
                        Sair
                    </button>
                </div>
            </nav>

            {view === 'pricing' && <PricingForm initialData={quoteToEdit} />}
            {view === 'history' && <HistoryDashboard isAdmin={session.user.is_admin} onLoadQuote={(quote) => { setQuoteToEdit(quote); setView('pricing'); }} />}
            {view === 'admin' && session.user.is_admin && <AdminDashboard token={session.token} />}
        </div>
    );
}

export default App;
