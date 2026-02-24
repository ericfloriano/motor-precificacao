# 🚀 Guia de Deploy (Produção)

Este projeto foi desenhado sob a arquitetura de **Microserviços** (Frontend VS Backend) com o objetivo de ser 100% gratuito (Free Tier). Para colocar a aplicação na nuvem, você precisará de 3 contas gratuitas:
1. **GitHub** (Para hospedar o código).
2. **Render** ou **Railway** (Para rodar o Backend em Python/FastAPI).
3. **Vercel** ou **Netlify** (Para rodar o Frontend em Vite/React).
4. **Supabase** (Banco de Dados PostgreSQL).

---

## Passo 1: O Banco de Dados (Supabase)
Atualmente a API usa um arquivo `sqlite.db` local. No Supabase:
1. Crie um projeto no **Supabase**.
2. Vá em `Project Settings > Database` e copie sua **Connection String** (URI PostgreSQL).
3. Ela se parecerá com: `postgresql://postgres.[sua-ref]:[sua-senha]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres`
4. Essa será a sua `DATABASE_URL` no Backend.

---

## Passo 2: O Backend (Render / Railway)
Para subir a API Python:
1. Crie uma conta no **Render.com** e conecte seu GitHub.
2. Clique em **New > Web Service**. Selecione o repositório deste projeto.
3. Nas configurações:
   - **Root Directory**: `backend` (Muito importante, pois o `main.py` e o `requirements.txt` estão na pasta `backend`).
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Em **Environment Variables**, adicione as seguintes regras:
   - `DATABASE_URL` = [Cole a URL do Supabase gerada no Passo 1]
   - `SECRET_KEY` = [Gere uma chave super secreta e longa, ex: `94f8b9d3e5a...`]
   - `INVITE_CODE` = [Opcional: Crie uma Senha Corporativa para blindar novos cadastros. Se omitido, o padrão será `VISURI2026`]
5. Mande dar **Deploy**! Ao final, o Render te dará um link como `https://motor-precifica-backend.onrender.com`. Guarde este link, ele é a sua **URL_DA_API**.

> **Atenção sobre o Banco de Dados Novo:** Depois que subir pela primeira vez, as tabelas serão criadas vazias no Supabase. Crie sua conta pela UI, vá no SQL Editor do Supabase e rode: `UPDATE users SET is_admin = true WHERE id = 1;` para se dar poder de Admin!

---

## Passo 3: O Frontend (Vercel)
O React precisa saber onde o Backend foi parar agora que ele não é mais `localhost:8000`.
1. Vá no arquivo `frontend/src/components/PricingForm.jsx`, `Auth.jsx`, `AdminDashboard.jsx`, e `HistoryDashboard.jsx`.
2. Onde tiver `http://localhost:8000/api/v1/...`, você deve substituir pela sua **URL_DA_API** do Render.
   *(Dica Pro: Você poderia colocar isso numa variável de ambiente `import.meta.env.VITE_API_URL`)*.
3. Entre na **Vercel.com**, crie um projeto e escolha o repositório do GitHub.
4. Nas configurações da Vercel:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
5. Clique em **Deploy**! A Vercel vai instalar os pacotes Node, compilar sua aplicação pra HTML dinâmico hiperveloz e te entregar um link público oficial (ex: `https://motor-precificacao.vercel.app`).

Pronto! Seu sistema está de pé, acessível no celular de toda sua equipe via navegador, usando computação na nuvem gratuita.
