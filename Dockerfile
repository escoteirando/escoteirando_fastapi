FROM node:slim AS frontend-build

WORKDIR /app

ADD frontend/package.json /app/package.json

RUN npm install

COPY frontend/ /app
ENV DOCKER_BUILD=1

RUN npm run build

FROM python:3-slim

WORKDIR /app

ADD requirements.txt /app

# RUN apk add python3-dev
RUN pip install -r requirements.txt

COPY static /app/static
COPY src /app/src
COPY main.py /app/main.py

COPY --from=frontend-build /static/ /app/static/

ENTRYPOINT [ "python", "/app/main.py" ]



