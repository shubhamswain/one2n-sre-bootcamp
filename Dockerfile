FROM python:3.12-alpine AS build
WORKDIR /app/student-app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/student-app
RUN python -m venv /opt/venv && pip install --no-cache-dir -r /app/student-app/requirements.txt && flask db upgrade


FROM python:3.12-alpine
WORKDIR /app/student-app
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=build /opt/venv /opt/venv
COPY --from=build /app/student-app/*.py /app/student-app/*env /app/student-app/
COPY --from=build /app/student-app/instance /app/student-app/instance
CMD ["flask", "run", "-h", "0.0.0.0"]

EXPOSE 5000