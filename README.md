# Motor de Precificação Web 🚀

Um sistema moderno, rápido e reativo para cálculo de impostos (DIFAL), custos logísticos, margens e comissões. Desenvolvido para substituir planilhas opacas de Excel por uma interface "premium" e responsiva, mantendo custo computacional zero com as soluções de nuvem mais modernas.

![App Example](https://img.shields.io/badge/Status-Completed-success) ![Python](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi) ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)

---

## 🏗️ Arquitetura

O projeto foi dividido em duas áreas distintas para maximizar a escalabilidade, reatividade e isolamento de lógica:
1. **Frontend**: React.js (com Vite) + Vanilla CSS (Glassmorphism e Neumorphism UI).
2. **Backend**: Python 3.x (FastAPI) + SQLite local (substituível por PostgreSQL em Supabase/Neon).

## ✨ Principais Funcionalidades

- **Reatividade Zero-Lag**: Os cálculos matemáticos são pré-validados e formatados visualmente diretamente pelo frontend a cada tecla digitada. Apenas no salvamento ocorre o tráfego HTTP para o Backend, garantindo máxima velocidade na operação comercial.
- **Protocolamento Automático e Revisões**: Toda cotação ganha um UUID/Protocolo numérico sequencial instantâneo no formato corporativo rastreável. Ao reabrir cotações através do Histórico, o backend gerencia revisões automáticas no formato `-REV.1`, `-REV.2`.
- **Tabela Dinâmica DIFAL**: Lookup customizado por estado configurado e embutido no motor base.
- **Segurança e Hierarquia (ACL)**: Módulo de gestão de permissões contendo Login Automático, restrição de domínios (apenas e-mails autorizados da empresa), controle Anti-Spam via Código de Convite Privado e visibilidade global com poderes de Exclusão de Histórico exclusivo para Administradores.
- **Matemática de Vendas**: Lógica de precificação robusta em múltiplas camadas (Markup Linear, Subtotais Base, Valor Mínimo de Margem Operacional e Teto de Descontos Concedidos - Máx. Permitido).
- **Exportação Formatada**: Relatórios em `.xlsx` e `.pdf` corporativos formatados para envio direto ou upload em CRMs, contendo dados do protocolo, cálculos precisos de impostos, e com botões de interface integrados à visualização do histórico.
- **UI Responsiva e Premium**: Visual *Dark Mode* corporativo, com micro-animações, campos transparentes com efeito de vidro (Glassmorphism), e botões texturizados *Dark Glow* interativos.

## 🚀 Como Executar Localmente

### 1. Iniciar o Backend
Abra um terminal, vá para a pasta \`backend\` e siga:
```bash
# Ativar o ambiente virtual e instalar dependências
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt # (Os pacotes já foram instalados no setup)

# Executar a API via Uvicorn
uvicorn main:app --reload
```
> A aplicação responderá na porta `http://localhost:8000/`. Você pode testar os endpoints através do Swagger UI visitando \`http://localhost:8000/docs\`.

### 2. Iniciar o Frontend
Abra um **segundo terminal**, vá para a pasta \`frontend\`:
```bash
# Instalar dependências node
npm install

# Rodar em ambiente dev
npm run dev
```
> Acesse no navegador o link gerado pelo Vite (normalmente `http://localhost:5173/`).

## ⚙️ Configurações Customizáveis

Os valores base para o DIFAL podem ser ajustados com facilidade editando o objeto `DIFAL_TABLE` presente no arquivo `/frontend/src/utils/math.js` e correspondente na API `/backend/calculos.py`. 

## 🛡️ Segurança

A persistência em banco está protegida por um schema robusto e higienizado desenvolvido sobre **Pydantic**. 
Autenticação via JWT já está integrada com expiração controlada e segregação de permissões de banco de dados (Apenas admins apagam dados ou veem todos).
O controle do Cadastro é feito via verificação de domínio atrelado a um cofre de Ambiente (ENV) contendo senhas e chaves ocultas.
