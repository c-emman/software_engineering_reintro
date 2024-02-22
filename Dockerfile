FROM python:3.12

COPY ./src /src

RUN pip install --no-cache-dir -r /src/requirements.txt

WORKDIR /src

EXPOSE 8000

ENTRYPOINT ["bash", "startup.sh"]
