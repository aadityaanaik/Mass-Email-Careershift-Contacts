from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pytz import timezone
import subprocess

def run_main():
    subprocess.run(["python3", "/Users/adityavnaik/Data/Repositories/fetch-email-selenium/main.py"], check=True)


# Default arguments for the DAG
default_args = {
    'owner': 'Aditya',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'dag_send_email',
    default_args=default_args,
    description='DAG to send emails to Data Managers',
    schedule_interval='30 14 * * *',  # Change this to your desired schedule
    start_date=datetime(2023, 9, 1, tzinfo=timezone('America/Chicago')),
    catchup=False,
)

# Run the task
run_main_py = PythonOperator(
    task_id='dag_send_email',
    python_callable=run_main,
    dag=dag,
)