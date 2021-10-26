FROM python:3

RUN mkdir /application
WORKDIR /application
COPY python-requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r python-requirements.txt

VOLUME /application

EXPOSE 8000

CMD ["flask_main.py"]
ENTRYPOINT ["python3"]