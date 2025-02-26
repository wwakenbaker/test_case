FROM python:3.12-slim
COPY --from=openjdk:17-slim /usr/local/openjdk-17 /usr/local/openjdk-17

ENV JAVA_HOME /usr/local/openjdk-17

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-17/bin/java 1

RUN apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*

COPY . /server

WORKDIR /server

RUN pip install -U pip setuptools

RUN pip install "cython<3.0.0" wheel && pip install "pyyaml==5.4.1" --no-build-isolation

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "app:app", "--workers 4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000","--log-level=error"]