FROM python:3.7

ADD . /usr/gogetter

WORKDIR /usr/gogetter

COPY . .

RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8888:8888

CMD ["/bin/bash", "deploy/run.sh"]
