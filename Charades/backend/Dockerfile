FROM python:3.11

COPY backend backend
WORKDIR backend
RUN pip install -r requirements.txt

CMD cd app && python app.py