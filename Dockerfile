FROM python:latest

WORKDIR /my_project

COPY . /my_project

RUN mkdir /my_project/results

RUN pip install -r requirements.txt

CMD [ "python", "myAsyncBot.py" ]