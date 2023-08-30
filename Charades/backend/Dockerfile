FROM python:3.11

COPY app app
WORKDIR app
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"


ENTRYPOINT ["python"]

CMD ["website/app/app.py"]
#CMD python website/app/app.py