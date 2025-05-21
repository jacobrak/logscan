FROM python:3.11-slim

ENV AIRFLOW_HOME=/app/airflow
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR $AIRFLOW_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Install Airflow with constraints
COPY requirements.txt .
COPY main.py $AIRFLOW_HOME/dags/
COPY scripts/ $AIRFLOW_HOME/scripts/
# Get constraints URL for Airflow version
ARG AIRFLOW_VERSION=2.8.1
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.11.txt"

RUN pip install --upgrade pip && \
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" && \
    pip install -r requirements.txt

COPY . .

CMD ["airflow", "standalone", "main.py"]
