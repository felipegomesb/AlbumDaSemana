# AlbumDaSemana

## Requisitos
- Docker e Docker Compose

## Rodar com Docker
```bash
docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Rodar localmente (sem Docker)

### Backend
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
npm install
npm run dev
```

## Variáveis de ambiente
- Backend: `.env.local` (veja `.env.local.example`)
- Frontend: `.env.development`

## Padroes de Projeto

a gente usa dois padroes de projeto aqui:

**Facade** - basicamente o arquivo `api_rest/spotify.py` é uma fachada pra API do Spotify. toda aquela parte chata de pegar token, montar header com base64, fazer request etc fica escondida la dentro. no resto do codigo a gente so chama `search_spotify()` ou `get_album_tracks()` e pronto, nao precisa saber como funciona por baixo

**Observer** - na parte do front quando o cara faz login ou logout o componente dispara um evento chamado `album-user-changed`. o header da pagina fica ouvindo esse evento e quando ele acontece o header se atualiza sozinho (mostra o link de perfil, esconde login/cadastro etc). nao precisa ficar chamando funcao manualmente pra atualizar, ele reage sozinho

## Endpoints principais
| Método | URL | Descrição |
|--------|-----|-----------|
| POST | /api/data/register/ | Cadastro |
| POST | /api/data/login/ | Login |
| GET | /api/users/ | Listar usuários |