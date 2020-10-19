FROM python:3.7-buster

ADD requirements.txt /requirements.txt
ADD main.py /main.py
RUN apt install -y libgl-dev
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/main.py"]

