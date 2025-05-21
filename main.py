from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'you',
    'start_date': datetime(2025, 5, 21),
    'retries': 1,
}

with DAG('run_my_scripts',
         default_args=default_args,
         schedule_interval=None,  # run manually or trigger on demand
         catchup=False) as dag:

    t1 = BashOperator(
        task_id='testfilegeneration',
        bash_command='python /app/scripts/testfilegeneration.py'
    )

    t2 = BashOperator(
        task_id='extract',
        bash_command='python /app/scripts/extract.py'
    )

    t3 = BashOperator(
        task_id='optuna',
        bash_command='python /app/scripts/optuna.py'
    )

    t4 = BashOperator(
        task_id='randomforest',
        bash_command='python /app/scripts/randomforest.py'
    )

    # Define the order: t1 -> t2 -> t3 -> t4
    t1 >> t2 >> t3 >> t4
