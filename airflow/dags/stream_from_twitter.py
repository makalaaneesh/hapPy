from bot.airflow_helpers.twitter_helper import read_stream_of_tweets
from bot.airflow_helpers.replies import MONGODB_COLLECTION_TWEETS_SOURCE, MONGODB_DB
from bot.airflow_helpers.db_helper import delete_docs_older_than

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

NO_OF_TWEETS_TO_STREAM = 5000
DELETE_OLDER_TWEETS_DAYS = 1

with DAG("stream_from_twitter",
         catchup=False,
         default_args=default_args,
         schedule_interval="0 */6 * * *") as dag:
    task1 = PythonOperator(task_id="delete_older_tweets",
                           python_callable=delete_docs_older_than,
                           op_args=(MONGODB_DB, MONGODB_COLLECTION_TWEETS_SOURCE, DELETE_OLDER_TWEETS_DAYS))
    task2 = PythonOperator(task_id="stream_from_twitter_to_kafka",
                           python_callable=read_stream_of_tweets,
                           op_args=(NO_OF_TWEETS_TO_STREAM,))


task1 >> task2
