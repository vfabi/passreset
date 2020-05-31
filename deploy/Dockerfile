FROM python:3.6-alpine AS compile-image
RUN apk add --no-cache uwsgi uwsgi-python uwsgi-http python-dev build-base linux-headers pcre-dev zlib-dev jpeg-dev freetype-dev git
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.6-alpine AS build-image
COPY --from=compile-image /app/.venv /app/.venv
RUN apk add --no-cache pcre libjpeg freetype
WORKDIR /app
COPY . .
RUN chown -R nobody:nobody /app/
USER nobody
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uwsgi", "--ini", "/app/config/uwsgi.ini"]