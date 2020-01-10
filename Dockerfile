# Matias Carrasco Kind
# mcarras2@illinos.edu
# 
#

FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y libaio1
RUN useradd --create-home --shell /bin/bash des --uid 1001
WORKDIR /home/des
RUN echo "source activate env" > /home/des/.bashrc
USER des
RUN git clone https://github.com/des-labs/desticket.git --single-branch --branch flask
EXPOSE 5000
RUN pip install easyaccess==1.4.7
RUN pip install jira
RUN pip install pyaml
WORKDIR /home/des/desticket
ENV HOME /home/des
CMD ["python","/home/des/desticket start_server.py"]
