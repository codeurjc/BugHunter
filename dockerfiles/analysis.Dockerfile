FROM jupyter/minimal-notebook

RUN pip install --upgrade pip

USER root 
RUN sudo apt-get update && sudo apt-get -y install graphviz
USER jovyan

COPY analysis/requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /home/jovyan/work/

CMD ["jupyter-notebook", "--notebook-dir=/home/jovyan/work/", "--ip='0.0.0.0'", "--port=8888","--NotebookApp.token=''","--allow-root"]

# sudo apt-get update && sudo apt-get install graphviz
# BUILD docker build -f dockerfiles/analysis.Dockerfile -t regression-seeker-analysis:0.1.1 .