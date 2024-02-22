#FROM ubuntu:20.04
#
#RUN apt update
#
#RUN apt install -y python3.12
#
#RUN apt-get update && apt-get install -y \
#    python3-pip
#
#COPY ./src /src
#
#RUN pip install -r /src/requirements.txt
#
#WORKDIR /src

FROM python:3.12

COPY ./src /src

RUN pip install --no-cache-dir -r /src/requirements.txt

WORKDIR /src

ENTRYPOINT ["bash", "startup.sh"]
#CMD ["bash startup.sh"]

