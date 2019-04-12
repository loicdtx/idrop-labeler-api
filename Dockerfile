FROM python:3.7
MAINTAINER loicdtx
RUN apt-get update -y && \
	apt-get install -y --no-install-recommends git 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
