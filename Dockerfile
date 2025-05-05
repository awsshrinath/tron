
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PAPER_MODE true

CMD ["python", "stock_trading/stock_runner.py"]
