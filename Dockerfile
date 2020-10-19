FROM python:3.7-buster

ADD requirements.txt /requirements.txt
ADD main.py /main.py
RUN apt-get update && apt-get install -y python-opencv
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/main.py"]

