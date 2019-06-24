FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev python3-venv \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app

WORKDIR /app

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main/flask_face_app.py"]