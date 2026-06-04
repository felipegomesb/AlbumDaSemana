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

## Endpoints principais
| Método | URL | Descrição |
|--------|-----|-----------|
| POST | /api/data/register/ | Cadastro |
| POST | /api/data/login/ | Login |
| GET | /api/users/ | Listar usuários |