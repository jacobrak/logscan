from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.insert(0, '/app/airflow')
from scripts.extract import save_clean_dataframe
from scripts.optuna_optimizer import study_
from scripts.random_forest_ import model_to_file

default_args = {
    'owner': 'you',
    'start_date': datetime(2025, 5, 21),
    'retries': 1,
}

with DAG('main',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    t1 = PythonOperator(
        task_id='extract',
        python_callable=save_clean_dataframe,
    )

    t2 = PythonOperator(
        task_id='optuna',
        python_callable=study_,
    )

    t3 = PythonOperator(
        task_id='randomforest',
        python_callable=model_to_file,
    )

    t1 >> t2 >> t3
