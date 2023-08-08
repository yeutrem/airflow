FROM apache/airflow:2.6.1-python3.8

USER root

ARG CLOUD_SDK_VERSION=392.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH "$PATH:/opt/google-cloud-sdk/bin/"

RUN apt-get update \
  && apt-get install -y --no-install-recommends vim \
  build-essential \
  acl \
  software-properties-common \
  git \
  gnupg 

RUN apt-get update \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /sources/dags
RUN chmod -R 777 /sources/dags

RUN pip3 install -U crcmod && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-sdk=${CLOUD_SDK_VERSION}-0 && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud --version

RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

RUN apt-get install -y kubectl

RUN groupmod -g 11000 root

VOLUME ["/root/.config"]
COPY requirements.txt /opt/airflow/requirements.txt
RUN chmod 755 /opt/airflow/requirements.txt

USER airflow

COPY operators /opt/airflow/libs/operators
COPY .airflowignore /opt/airflow/dags/.airflowignore
RUN /home/airflow/.local/bin/pip install --user --upgrade pip
RUN /home/airflow/.local/bin/pip install --no-cache-dir --user -r /opt/airflow/requirements.txt
