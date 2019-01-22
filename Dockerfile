# Matias Carrasco Kind
# mcarras2@illinos.edu
# 
#

FROM continuumio/miniconda3
RUN apt-get update
RUN apt-get install -y libaio1
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN useradd --create-home --shell /bin/bash des --uid 1001
WORKDIR /home/des
RUN echo "source activate env" > /home/des/.bashrc
RUN chown -R des:des /opt/conda
USER des
RUN git clone https://github.com/des-labs/desticket.git
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN conda create -n env python=3.6
RUN conda install --yes -c anaconda -c mgckind -c conda-forge easyaccess==1.4.6 jira pyyaml -n env
WORKDIR /home/des/desticket
ENV PYTHONPATH /opt/conda/envs/env
ENV HOME /home/des
