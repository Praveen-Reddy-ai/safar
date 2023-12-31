FROM python:3.10

ENV APP_HOME /app
WORKDIR $APP_HOME
copy . ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python app.py