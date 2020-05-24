from bot.airflow_helpers.replies import follow_up_with_replies
from bot.airflow_helpers.analytics import perform_analytics

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


# https://github.com/karpenkovarya/airflow_for_beginners/blob/master/dags/dags.py
default_args = {
    "owner": "me",
    "depends_on_past": False,
    "start_date": datetime(2020, 1, 20),
    "email": ["makalaaneesh18@mail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

NO_OF_REPLIES = 2

with DAG("follow_up",
         catchup=False,
         default_args=default_args,
         schedule_interval="@hourly") as dag:
    task1 = PythonOperator(task_id="follow_up_with_replies",
                           python_callable=follow_up_with_replies)



task1
