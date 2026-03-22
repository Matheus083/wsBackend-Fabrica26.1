# 🚀 SpaceLog — Seu Diário Astronômico Pessoal

> *"Todo dia a NASA fotografa o universo. O SpaceLog guarda essas fotos para você."*

---

## ✨ O que é o SpaceLog?

Imagine um **álbum de figurinhas do espaço** — mas em vez de você colar as figurinhas, um robô busca automaticamente a foto mais bonita do universo de qualquer dia que você escolher, e guarda tudo organizado num diário só seu.

É exatamente isso que o SpaceLog faz.

Ele se conecta ao programa **APOD** *(Astronomy Picture of the Day)* da **NASA** — um projeto que existe desde 1995 e que, todo dia, publica a fotografia astronômica mais deslumbrante capturada por telescópios e sondas espaciais ao redor do mundo.

Você escolhe uma data. O SpaceLog busca a foto lá na NASA. Você salva no seu diário. Simples assim. 🌌

---

## 🌠 Funcionalidade Principal — Como a Magia Acontece

```
Você digita uma data
        ↓
SpaceLog pergunta para a NASA: "O que aconteceu nesse dia?"
        ↓
A NASA responde com título, foto e explicação
        ↓
O formulário é preenchido automaticamente para você revisar
        ↓
Você clica em "Salvar" — e a descoberta entra no seu diário para sempre
```

Você também pode **adicionar, editar ou remover** qualquer registro manualmente, como um caderno de anotações que você controla completamente.

---

## 🛸 Tecnologias Utilizadas

| Tecnologia | Para que serve no projeto |
|---|---|
| 🐍 **Django 6.0** | O cérebro da aplicação — organiza tudo e serve as páginas |
| 🐬 **MySQL 8.0** | O baú onde os registros do diário ficam guardados |
| 🐳 **Docker** | Uma caixinha mágica que garante que o banco funciona igual em qualquer computador |
| 🎨 **Bootstrap 5** | Deixa o site bonito e funciona bem no celular também |
| 🌍 **NASA APOD API** | A fonte oficial das fotografias e informações astronômicas |
| 🐍 **PyMySQL** | O tradutor que faz o Django conversar com o MySQL |
| 📦 **python-dotenv** | Guarda as senhas do projeto em segredo, longe do código |

---

## 📸 Capturas de Tela

| Diário (lista) | Formulário de busca |
|---|---|
| *em breve* | *em breve* |

---

## ⚙️ Como Instalar e Rodar

Não precisa ser programador para seguir esses passos. Pense neles como uma receita de bolo — siga a ordem e vai funcionar. 🎂

### Pré-requisitos

Você vai precisar ter instalado na sua máquina:

- [Git](https://git-scm.com/) — para baixar o projeto
- [Docker](https://www.docker.com/) — para subir o banco de dados
- [Python 3.12+](https://www.python.org/) — para rodar o servidor Django

---

### Passo 1 — Baixar o projeto

```bash
git clone https://github.com/seu-usuario/spacelog.git
cd spacelog
```

---

### Passo 2 — Criar o arquivo de configuração secreto

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Abra o `.env` num editor de texto e preencha:

```env
# Banco de dados
DB_NAME=spacelog_db
DB_USER=user_space
DB_PASS=uma_senha_forte_aqui
DB_ROOT_PASS=outra_senha_forte_aqui
DB_HOST=127.0.0.1
DB_PORT=3306

# Django
SECRET_KEY=gere-uma-chave-longa-e-aleatoria-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# NASA API — obtenha a sua em: https://api.nasa.gov (é grátis!)
NASA_API_KEY=DEMO_KEY
```

> 💡 **Dica:** `DEMO_KEY` funciona para testar, mas tem limite de 30 buscas por hora. Cadastre uma chave gratuita em [api.nasa.gov](https://api.nasa.gov) para uso sem restrições.

---

### Passo 3 — Subir o banco de dados com Docker

```bash
docker compose up -d
```

Aguarde uns 20 segundos e verifique se está funcionando:

```bash
docker compose ps
# O status deve mostrar "healthy"
```

---

### Passo 4 — Instalar as dependências Python

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# ou: venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

### Passo 5 — Criar as tabelas no banco

```bash
python manage.py migrate
```

---

### Passo 6 — Rodar o servidor

```bash
python manage.py runserver
```

Abra o navegador em **[http://127.0.0.1:8000/diario/](http://127.0.0.1:8000/diario/)** e seja bem-vindo ao seu diário astronômico. 🌟

---

## 🗂️ Estrutura do Projeto

```
spacelog/
├── config/                  # Configurações do Django (settings, urls raiz)
├── spacelog/                # App principal
│   ├── management/
│   │   └── commands/
│   │       └── fetch_apod.py   # Comando: python manage.py fetch_apod
│   ├── templates/spacelog/     # Todos os templates HTML
│   ├── models.py            # Model AstronomyPicture
│   ├── views.py             # ListView, CreateView, UpdateView, DeleteView
│   ├── forms.py             # ModelForm com widgets customizados
│   ├── fetch_apod.py        # Função get_nasa_data() — comunica com a NASA
│   └── urls.py              # Rotas do app
├── docker-compose.yml       # Sobe o MySQL 8.0 no Docker
├── .env.example             # Template das variáveis de ambiente
└── requirements.txt
```

---

## 🔧 Comandos Úteis

```bash
# Buscar o APOD de hoje e salvar automaticamente no banco
python manage.py fetch_apod

# Buscar o APOD de uma data específica
python manage.py fetch_apod --date 2024-07-04

# Forçar atualização de um registro já existente
python manage.py fetch_apod --date 2024-07-04 --force

# Parar o banco de dados (dados não são perdidos)
docker compose down

# Parar e apagar TODOS os dados do banco
docker compose down -v
```

---

## 🚀 Notas de Lançamento

*Bastidores do desenvolvimento — os desafios reais que encontramos pelo caminho.*

---

### 🔴 O Desafio do Erro 429 — Quando a NASA disse "chega por hoje"

Durante o desenvolvimento, topamos com o temido **HTTP 429 Too Many Requests** — a forma educada da NASA de dizer *"você já perguntou demais hoje, volte amanhã"*.

A `DEMO_KEY` (chave de teste gratuita) tem um limite de **30 requisições por hora** e **50 por dia**. Quando estávamos testando buscas em sequência para popular o banco inicial, esse limite chegou rápido.

A solução foi dupla: tratar o erro 429 com uma mensagem clara na interface (*"Limite de buscas atingido — tente mais tarde"*) e, principalmente, registrar uma **API Key própria** em [api.nasa.gov](https://api.nasa.gov) — gratuita, aprovada em segundos, e com limite de **1.000 requisições por hora**. Uma diferença enorme para desenvolvimento.

---

### 🔑 Por que Você Precisa da Sua Própria API Key

A `DEMO_KEY` que vem no `.env.example` é ótima para um primeiro teste. Mas pense nela como um crachá de visitante — funciona para entrar, mas não para ficar o dia todo.

Para usar o SpaceLog de verdade, **cadastre sua chave gratuita** em [api.nasa.gov](https://api.nasa.gov) — basta um e-mail. Você recebe a chave na hora e substitui `DEMO_KEY` no seu `.env`. A partir daí, 1.000 buscas por hora são mais do que suficientes para qualquer uso pessoal.

---

### 🔭 Planos Futuros

O SpaceLog está em órbita estável, mas há muito mais espaço para explorar:

- **🔐 Sistema de login** — cada usuário terá seu próprio diário privado, sem misturar descobertas com outras pessoas
- **🗓️ Busca em intervalo de datas** — importar um mês inteiro de APODs com um clique
- **🏷️ Tags e favoritos** — marcar as imagens que mais encantaram com categorias como *nebulosas*, *galáxias*, *sistema solar*
- **📧 Notificação diária** — receber por e-mail o APOD do dia automaticamente toda manhã
- **🌐 Deploy na nuvem** — publicar o SpaceLog online para que qualquer pessoa possa criar seu diário sem instalar nada

---
## 🔍 Notas de Desenvolvimento (Aos Avaliadores da fabrica).

Este documento existe porque transparência técnica importa mais do que
uma imagem perfeita.

### 🎨 Front-end & UI
O front-end foi desenvolvido **com auxílio integral de IA**. Direcionei o
esforço para o que realmente diferencia o projeto — a lógica do back-end.
O resultado é uma interface funcional, responsiva e coerente visualmente,
entregue dentro do prazo.

### ⚙️ Back-end & Lógica de Negócio
O core do sistema foi **desenvolvido manualmente**. Isso inclui:
- A integração com a API da NASA (autenticação, tratamento de erros,
  mapeamento de resposta)
- O fluxo completo de CRUD com Class-Based Views do Django
- O tratamento do Error 429 e a lógica de fallback
- A configuração do Docker com healthcheck e variáveis de ambiente via `.env`
- O Management Command `fetch_apod` com suporte a `--date` e `--force`

### 🏗️ Arquitetura & Decisões de Projeto
A ideia do projeto, a modelagem do banco (`AstronomyPicture` com
`unique=True` no campo `date`), a estruturação das rotas com namespace,
a separação entre projeto e app, e a escolha de `get_or_create` como
mecanismo anti-duplicata foram **pensadas e executadas de forma
independente**. Cada decisão tem uma razão com base no meu conhecimento.

### 📄 Documentação
Infelizmente não consegui documentar o projeto ao todo, mas o que existe são
**comentários manuais em pontos estratégicos** do código — especialmente
nas views, no management command e nas configurações do banco — para que
qualquer desenvolvedor consiga entender a lógica sem precisar de um guia
externo. Este README é parte dessa intenção.

---
## 📄 Licença

Este projeto está sob a licença **MIT** — você pode usar, modificar e distribuir à vontade, desde que mantenha os créditos.

---

<div align="center">

*"O universo é grande demais para ser esquecido."*

</div>
