FROM phidata/airflow:2.4.2

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/airflow_resources /
RUN pip install -r /requirements-airflow.txt

# Install python3 kernel for jupyter
RUN ipython kernel install --name "python3"
