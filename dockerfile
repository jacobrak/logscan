FROM python:3.11-slim

# Environment variables
ENV AIRFLOW_HOME=/app/airflow
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR $AIRFLOW_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Copy requirements and install Airflow
COPY requirements.txt .

ARG AIRFLOW_VERSION=2.8.1
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.11.txt"

RUN pip install --upgrade pip && \
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" && \
    pip install -r requirements.txt

# Copy your DAG and script files
COPY dags/ $AIRFLOW_HOME/dags/
COPY scripts/ $AIRFLOW_HOME/scripts/

# Set Airflow dags folder explicitly (optional if you mount it)
ENV AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/dags
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
# Copy any remaining files (optional)
COPY . .

# Run airflow standalone
CMD ["airflow", "standalone"]
