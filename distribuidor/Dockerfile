FROM python:3.10
COPY main.py routes.py requirements.txt /
COPY templates/index.html /templates/
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn"]
CMD ["--access-logfile", "-", "-b", "0.0.0.0:5000", "main:app"]
EXPOSE 5000