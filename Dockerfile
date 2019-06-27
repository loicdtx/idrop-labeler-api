FROM ubuntu:18.04
MAINTAINER loicdtx
RUN apt-get update -y && \
	apt-get install -y --no-install-recommends git \
        python3-dev python3-pip python3-setuptools \
	build-essential
# This needs to be set for CLick
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
RUN pip3 install -e .
RUN pip3 install uwsgi
EXPOSE 5000
ENTRYPOINT ["uwsgi"]
CMD ["--socket", "0.0.0.0:5000", "--protocol=http", "-w", "api:app"]
