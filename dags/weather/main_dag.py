"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os
import json
import numpy as np

from weather.task_helpers import get_weather


default_args = {
    'owner': 'rnewman',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['robertlnewman@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'weather',
    description='Get current weather',
    default_args=default_args,
    schedule_interval=timedelta(days=1)
)

with dag:

    task0 = DummyOperator(
        task_id='kick_off_dag'
    )

    task1 = PythonOperator(
        task_id='get_current_weather',
        python_callable=get_weather
    )

    task2 = BashOperator(
        task_id='add_to_quilt',
        bash_command='python src/add_to_quilt.py',
        retries=3
    )

    task3 = BashOperator(
        task_id='upload_to_s3',
        bash_command='python src/upload_to_s3.py',
        retries=3
    )

# Connect the DAG --------
task0 >> task1 >> task2 >> task3
