FROM ubuntu:18.04
MAINTAINER loicdtx
RUN apt-get update -y && \
	apt-get install -y --no-install-recommends git \
        python3 python3-pip python3-setuptools
# This needs to be set for CLick
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
RUN pip3 install -e .
ENV FLASK_APP=api
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
