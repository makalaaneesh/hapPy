from bot.airflow_helpers.replies import follow_up_with_replies
from bot.airflow_helpers.db_helper import delete_docs_older_than
from bot.airflow_helpers.replies import MONGODB_DB, MONGODB_COLLECTION_TWEET_REPLIES_SOURCE
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

DELETE_OLDER_TWEETS_DAYS = 2

with DAG("follow_up",
         catchup=False,
         default_args=default_args,
         schedule_interval="0 */24 * * *") as dag:
    task1 = PythonOperator(task_id="delete_older_tweets",
                           python_callable=delete_docs_older_than,
                           op_args=(MONGODB_DB, MONGODB_COLLECTION_TWEET_REPLIES_SOURCE, DELETE_OLDER_TWEETS_DAYS))
    task2 = PythonOperator(task_id="follow_up_with_replies",
                           python_callable=follow_up_with_replies)



task1 >> task2
