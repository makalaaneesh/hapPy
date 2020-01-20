from bot.twitter_stream import read_stream_of_tweets

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
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
    # "schedule_interval": "@hourly",
}

NO_OF_TWEETS_TO_STREAM = 100

with DAG("stream_from_twitter",
         catchup=False,
         default_args=default_args,
         schedule_interval="@hourly") as dag:
    task1 = PythonOperator(task_id="stream_from_twitter_to_kafka",
                           python_callable=read_stream_of_tweets,
                           op_args=(NO_OF_TWEETS_TO_STREAM,))

    # Need to refactor this.
    # Not ideal.
    # calling the function directly using a pythonoperator was not working.
    # Return code -6 was returned.
    # task1 = BashOperator(task_id="stream_from_twitter_to_kafka",
    #                      bash_command="source /Users/aneeshmakala/Documents/ComputerScience/datascience/venv_datascience/bin/activate; python /Users/aneeshmakala/Documents/ComputerScience/datascience/hapPy/bot/twitter_stream.py")


task1
