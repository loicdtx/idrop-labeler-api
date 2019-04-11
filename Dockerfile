FROM ubuntu:latest
MAINTAINER loicdtx
RUN apt-get update -y
RUN apt-get install -y python3-pip git
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
