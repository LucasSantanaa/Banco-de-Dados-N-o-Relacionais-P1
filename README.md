# FastAPI Chat (Refatorado)

## O que foi refatorado (resumo)
- Modularização: separação em `config.py`, `database.py`, `models.py`, `ws_manager.py`, `routes/messages.py` e `main.py`.
- Validação: `MessageIn` e `MessageOut` (Pydantic) para entrada/saída de mensagens.
- Erros: `before_id` inválido retorna 400; mensagens vazias não são salvas.
- Conexão DB: `get_db()` centraliza e reutiliza o client MongoDB.
- WebSockets: `WSManager` gerencia conexões por sala e broadcast com limpeza de sockets fechados.
- Comentários: Alguns Comentarios do que achei o essencial no codigo

## Como rodar (local)
1. Preencha `.env` com `MONGO_URL`.
2. Instale dependências: `pip install -r requirements.txt`
3. Crie uma Venv: `python -m venv .venv`
4. Ative a Venv: `.venv\Scripts\Activate.ps1`
5. Rode: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
6. Abra: http://localhost:8000 e http://localhost:8000/docs

## Prints do db com alguns testes realizados

<img width="1396" height="723" alt="Mongodb_testes" src="https://github.com/user-attachments/assets/bf10c20f-7e99-4e8b-a3c8-a4dfacfe37e9" />

<img width="633" height="178" alt="Terminal" src="https://github.com/user-attachments/assets/d10aaf08-2af9-48d7-a6d1-61d448734d09" />

<img width="1391" height="666" alt="Chat_mensagens" src="https://github.com/user-attachments/assets/75ac59fc-b814-4f00-8799-ec4e6b267377" />
