FROM python:3.13-slim AS builder

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv pip compile pyproject.toml -o requirements.txt

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]