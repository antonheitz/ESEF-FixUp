FROM python:3.10-buster

WORKDIR /opt/app

COPY packages/backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "packages.backend.main:app", "--host", "0.0.0.0", "--port", "3001"]