FROM ubuntu:18.04
MAINTAINER loicdtx
RUN apt-get update -y && \
	apt-get install -y --no-install-recommends git \
        python3 python3-pip python3-setuptools
COPY . /app
WORKDIR /app
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]
