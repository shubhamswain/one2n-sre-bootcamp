FROM python:3.9-slim
WORKDIR /app/student-app
COPY requirements.txt /app/student-app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/student-app/

RUN flask db upgrade
CMD ["flask", "run", "-h", "0.0.0.0"]