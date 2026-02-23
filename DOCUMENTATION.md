# 📚 Documentação de Arquitetura (Guia de Estudo)

Olá Engenheiro! Este documento foi redigido com o intuito de servir como um trampolim para seus estudos. O Motor de Precificação Web é um excelente "Laboratório Full-Stack", pois abrange **Frontend Reativo** (React), **Backend API Rest** (FastAPI) e **Banco de Dados Relacional** (SQLAlchemy).

## 1. Visão Geral da Arquitetura
A aplicação adota um padrão de arquitetura **Cliente-Servidor (Client-Server)** desacoplada. Isso significa que a Interface Visual onde os usuários clicam (Frontend) não roda no mesmo "Liquidificador" que as senhas e os bancos de dados (Backend). 
Eles conversam entre si usando a linguagem universal da internet: Pedidos HTTP (Requests) com mensagens formatadas em **JSON**.

---

## 2. Mergulhando no Frontend (React + Vite)
O código mora na pasta `/frontend/src`. A responsabilidade dele é ser "burro" para segredos empresariais, mas ser "extremamente inteligente" para a Experiência do Usuário (UX).

* **`App.jsx`**: É o "Esqueleto" do site. Nele usamos `useState` (Gancho do React para memorizar variáveis) para saber se a pessoa está Autenticada (`session`). Se não estiver, ele mostra o componente `<Auth />`, se estiver logado, exibe os botões de navegação.
* **`components/Auth.jsx`**: Cuida do Login e do Registro. Ele fala com a API no `/api/v1/auth...`. Ao logar, a API devolve um `token` longo (JWT). Nós o salvamos no cofre secreto do navegador (`localStorage.getItem('token')`) para provar quem somos a cada clique na plataforma.
* **`components/PricingForm.jsx`**: Este é o coração do Vendedor. O `useState` vigia cada letra ditada nos campos `onChange`. 
   > *Curiosidade de Desempenho:* Ao invés de mandar um pedido pra API toda vez que você bate no teclado (o que travaria tudo), usamos o arquivo `/utils/math.js`. Ele clona a lógica exata de impostos da API e faz a conta ali, no próprio navegador, piscando o preço na tela em milissegundos. Assim que o usuário clica em **Salvar**, a API é chamada *uma única vez*.
* **O Efeito Visual (Vanilla CSS)**: Perceba o arquivo `index.css`. Todos aqueles botões azuis e as bordas de vidro (Glassmorphism) são feitos na mão com *backdrop-filter: blur* e gradientes.

---

## 3. Mergulhando no Backend (Python + FastAPI)
O código mora na pasta `/backend`. Aqui não existe cor, botão ou tela. É o "Cérebro" da empresa. Só lida com Regras Cruéis e Dados Frios.

* **`main.py`**: É o grande Maestro. Ele escuta as "Portas" do servidor. Cada `@app.get` ou `@app.post` é um ouvido dele.
   > Quando o Frontend bate ali e manda um JSON pedindo para Salvar Cotação, o FastAPI ativa a função `calculate_pricing()`. Ele também executa a "Segurança Automática" olhando pra tag `Depends(auth.get_current_user)`, que impede a execução se o Token JWT não for válido.
* **`models.py` (SQLAlchemy)**: Transforma tabelas chatas de Banco de Dados (`CREATE TABLE users...`) em "Classes Python". Assim, em vez de escrever SQL puro que poderia causar dor de cabeça pra migrar, usamos ORM (Object-Relational Mapping).
* **`schemas.py` (Pydantic)**: São os Vigias da Máquina. Uma classe como `UserCreate` ali diz assim: *"O email não pode ser Nulo e a senha precisa ser texto"*. O FastAPI usa isso para devolver **Erro 422 Automático** caso alguém tente hackear o formulário com dados falsos.
* **`calculos.py`**: Onde os centavos batem. Nele escrevemos o fluxo financeiro exato: Margem, Comissão, Imposto e Frete. A constante `DIFAL_TABLE` foi importada da sua planilha antiga e embutida aqui de modo nativo, operando com chaves literais de Estados Brasileiros.
* **`export.py`**: A fábrica de relatórios.
   - **Excel**: Usa Pandas para transformar uma `dict` chata num bonito `DataFrame`, e injeta num arquivo binário falso (`BytesIO`).
   - **PDF**: Usa `ReportLab`. É uma biblioteca que "pinta" um papel A4 e vai desenhando textos (`Paragraph`) e grades (`Table`). Foi a alternativa rápida pro Pipefy, injetando as variáveis do Banco dentro da estilização dos Componentes.

---

## 4. Banco de Dados e Segurança
Usamos Autenticação **JWT (JSON Web Token)**. 
1. O usuário manda senha pro backend.
2. O Backend hasheia com `Bcrypt` (uma criptografia irremovível) e acha ele no SQLite.
3. O Backend empacota uma espécie de "Bilhete de Passagem de Ônibus Virtual" digitalmente assinado usando o `SECRET_KEY` do arquivo `.env`. Esse passe vale por algumas horas.
4. O Frontend guarda o passe na bolsinha (`localStorage`).
5. Se uma pessoa mal-intencionada forjar o passe ou espionar a tela, ela não terá o `SECRET_KEY` assinado pelo Python, então todo pedido de Cotação de Administrador bate na parede com um "Erro 401: Unauthorized HTTP".

## 5. Dicas de Evolução
* Tente estudar a aba **Hooks** do React (`useEffect` dentro do `AdminDashboard`). Ele é quem atira a função de "Buscar Cotações na API" assim que a aba é aberta.
* Tente ler a biblioteca **FastAPI-Limiter** no `main.py` que bloqueia ataques DDOS (Spamming de cotações em 1 minuto) através da verificação de IP. 

Ótimos estudos e Sucesso!
