from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'you',
    'start_date': datetime(2025, 5, 21),
    'retries': 1,
}

with DAG('main',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    t1 = BashOperator(
        task_id='TestFileGeneration',
        bash_command='python /app/scripts/TestFileGeneration.py'
    )

    t2 = BashOperator(
        task_id='extract',
        bash_command='python /app/scripts/extract.py'
    )

    t3 = BashOperator(
        task_id='optuna',
        bash_command='python /app/scripts/optuna_optimizer.py'
    )

    t4 = BashOperator(
        task_id='randomforest',
        bash_command='python /app/scripts/random_forest_.py'
    )

    t1 >> t2 >> t3 >> t4