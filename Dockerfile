FROM node:slim AS frontend-build

WORKDIR /app

ADD frontend/package.json /app/package.json

RUN npm install

COPY frontend/ /app
ENV DOCKER_BUILD=1

RUN npm run build
RUN ls -la /app

FROM python:3-slim

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

COPY static /app/static
COPY src /app/src
COPY main.py /app/main.py

COPY --from=frontend-build /app/static/ /app/static/

ENTRYPOINT [ "python", "/app/main.py" ]



