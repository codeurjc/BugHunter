FROM jupyter/minimal-notebook

RUN pip install --upgrade pip

COPY analysis/requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /home/jovyan/work/

CMD ["jupyter-notebook", "--notebook-dir=/home/jovyan/work/", "--ip='0.0.0.0'", "--port=8888","--NotebookApp.token=''","--allow-root"]

# BUILD docker build -f dockerfiles/analysis.Dockerfile -t regression-seeker-analysis:0.1.0 .