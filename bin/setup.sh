#!/usr/bin/env bash
# clone repo

# export HAPPY_HOME="<location of cloned repo>"
# export AIRFLOW_HOME="$HAPPY_HOME/airflow"

# install system packages
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update

sudo apt-get install default-jre default-jdk -y
sudo apt-get install python3.7 libmysqlclient-dev python-dev libssl-dev virtualenv python-pip -y
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
sudo apt-get install python-dev python3.7-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev -y


#install mysql
# ENTER password while installing
sudo apt-get install mysql-server -y

# install mongo
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start


# install kafka
wget http://apachemirror.wuchna.com/kafka/2.4.0/kafka_2.12-2.4.0.tgz
tar zxvf kafka_2.12-2.4.0.tgz
mv kafka_2.12-2.4.0 kafka


# create virtualenv
virtualenv -p python3 ~/venv

# enter virtualenv
source ~/venv/bin/activate

# install pip packages
pip install -r "$HAPPY_HOME/requirements.txt"
python -c "import nltk; nltk.download('stopwords')"

# inlcude HAPPY_HOME in python path
echo "$HAPPY_HOME" > ~/venv/lib/python3.7/site-packages/happy.pth


# test imports
python -c "from models.model import load_model; m=load_model(); m.predict('I hate my life')"



#setup kafka
# create systemd configs
# https://gist.github.com/vipmax/9ceeaa02932ba276fa810c923dbcbd4f


# setup airflow
# Copy passwords file to $HAPPY_HOME/bot/airflow_helpers/passwords.py
# create systemd configs

airflow initdb





