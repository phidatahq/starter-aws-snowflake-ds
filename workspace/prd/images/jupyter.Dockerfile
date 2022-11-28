FROM phidata/jupyterlab-r:3.4.8

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/prd/jupyter_resources /usr/local/jupyter
RUN pip install -r /usr/local/jupyter/requirements-jupyter.txt

RUN ln -s /usr/local/jupyter/gitconfig ~/.gitconfig
