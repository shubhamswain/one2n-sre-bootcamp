FROM python:3.12-alpine AS build

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/student-app

# Install build dependencies if needed (uncomment if you have native deps)
# RUN apk add --no-cache gcc musl-dev

COPY requirements.txt ./
RUN python -m venv /opt/venv && pip install --no-cache-dir -r requirements.txt

COPY . . 
RUN flask db upgrade

FROM python:3.12-alpine AS production

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app/student-app

COPY --from=build /opt/venv /opt/venv
COPY --from=build /app/student-app /app/student-app

# Optionally set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=true

EXPOSE 5000
CMD ["flask", "run", "-h", "0.0.0.0"]