FROM python:3.6-alpine

WORKDIR /app
COPY ./requirements.txt .
RUN apk add --no-cache uwsgi uwsgi-python uwsgi-http python-dev build-base linux-headers pcre-dev zlib-dev jpeg-dev freetype-dev \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . .
RUN chown -R nobody:nobody /app/
USER nobody

EXPOSE 8000
CMD ["uwsgi", "--ini", "/app/deploy/uwsgi.ini"]