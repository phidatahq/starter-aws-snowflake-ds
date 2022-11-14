FROM phidata/superset:2.0.0

RUN pip install --upgrade pip

COPY workspace/prd/superset_resources/requirements-superset.txt /
RUN pip install -r /requirements-superset.txt

COPY workspace/prd/superset_resources /app/docker/
