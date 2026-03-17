FROM python:3.12-alpine AS build

RUN apk update && \
apk add --no-cache --virtual build-deps gcc musl-dev && \
apk add postgresql-dev py3-psycopg2

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/student-app

COPY requirements.txt ./
RUN python -m venv /opt/venv && pip install --no-cache-dir -r requirements.txt

COPY . . 

FROM python:3.12-alpine AS production

RUN apk update && \
apk add --no-cache --virtual postgresql-dev py3-psycopg2

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app/student-app

COPY --from=build /opt/venv /opt/venv
COPY --from=build /app/student-app /app/student-app
COPY entrypoint.sh /app/student-app/
RUN chmod +x entrypoint.sh
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app/student-app
USER appuser
RUN mkdir -p logs

# Optionally set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production


EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/v1/healthcheck || exit 1
CMD ["./entrypoint.sh"]
LABEL maintainer="shubham.swain3@gmail.com"
LABEL version="0.1.0"