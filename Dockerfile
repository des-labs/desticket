# Matias Carrasco Kind
# mcarras2@illinos.edu
# 
#

FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y libaio1
RUN apt-get install -y git
RUN apt-get install -y python3.6
RUN apt-get remove python-pip-whl
RUN apt-get install -y python3-pip
RUN useradd --create-home --shell /bin/bash des --uid 1001
WORKDIR /home/des
RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip
USER des
RUN git clone https://github.com/des-labs/desticket.git --single-branch --branch flask
EXPOSE 5000
RUN pip3 install easyaccess
RUN pip3 install jira
RUN pip3 install pyaml
RUN pip3 install flask
RUN pip3 install wtforms
RUN pip3 install gevent
RUN pip3 install logging
WORKDIR /home/des/desticket
ENV HOME /home/des
CMD ["/usr/bin/python3","/home/des/desticket/start_server.py"]
