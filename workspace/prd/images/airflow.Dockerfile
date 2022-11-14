FROM phidata/airflow:2.4.2

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/prd/airflow_resources/requirements-airflow.txt /
RUN pip install -r /requirements-airflow.txt

COPY workspace/prd/airflow_resources/webserver_config.py ${AIRFLOW_HOME}/
