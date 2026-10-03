python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

select interpreter => choose workspace

uv init
uv add requests
uv run main.py or uvicorn main:app --reload




DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=url_shortener