FROM python:latest

WORKDIR /app/nssit

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python -m flask run" ]