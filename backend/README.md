## Python DB 初始化及建置
1. 啟用虛擬環境
```bash
cd backend
uv venv
.venv\Scripts\activate
```

2. 初始化DB
```bash
uv run python -m flask db init
uv run python -m flask db migrate -m "Initial migration"
uv run python -m flask db upgrade
```