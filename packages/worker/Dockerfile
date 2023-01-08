FROM python:3.10-buster

WORKDIR /opt/app

COPY packages/worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-um", "packages.worker.loop"]