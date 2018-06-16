FROM python:3.5.1
ENV PYTHONUNBUFFERED 1

################################################################################
# CORE

RUN apt-get update && apt-get install -y \
    pkg-config \
    cmake \
    openssl \
    wget \
    git \
    vim

ADD requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

ADD . /code/


################################################################################
# Storage Locations

RUN mkdir -p /code/images && \
    mkdir -p /var/www/images && \
    chmod -R 0755 /code/images/ && \
    # Create hashed temporary upload locations
    mkdir -p /var/www/images/_upload/{0..9} && chmod 777 -R /var/www/images/_upload


WORKDIR /code

################################################################################
# Clean Up

RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD /code/run_uwsgi.sh

EXPOSE 3031
