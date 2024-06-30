FROM python:3.10.4-alpine3.16

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8000

RUN apk --no-cache update && apk --no-cache add zlib-dev jpeg-dev gcc musl-dev \
    && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install


COPY . .

COPY entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]