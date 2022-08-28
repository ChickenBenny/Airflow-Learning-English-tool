FROM python:3.9
WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install -r requirements.txt
COPY ./credentials /credentials
COPY ./main.py /main.py