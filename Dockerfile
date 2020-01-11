# Matias Carrasco Kind
# mcarras2@illinos.edu
# 
#

# Build from a parent image
FROM oraclelinux:7-slim as oracle

RUN  curl -o /etc/yum.repos.d/public-yum-ol7.repo https://yum.oracle.com/public-yum-ol7.repo && \
     yum-config-manager --enable ol7_oracle_instantclient && \
     yum -y install oracle-instantclient18.3-basic

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
WORKDIR /home/des/desticket
ENV PATH=$PATH:/usr/lib/oracle/18.3/client64/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/18.3/client64/lib:/usr/lib
COPY --from=oracle /usr/lib/oracle/ /usr/lib/oracle
COPY --from=oracle /lib64/libaio.so.1 /usr/lib

CMD ["/usr/bin/python3","/home/des/desticket/start_server.py"]
