ARG USERNAME=app_user
ARG GROUPNAME=app_user
ARG APP_PATH=/workspace

FROM    registry.access.redhat.com/ubi9/ubi-init:9.4 as common_build
ARG USERNAME
ARG GROUPNAME
ARG APP_PATH

WORKDIR $APP_PATH

RUN --mount=type=secret,id=host_certificate_file,dst=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
    dnf install -y \
    langpacks-en \
    wget \
    unzip \
    gcc \
    python3.11 \
    python3.11-devel \
    python3.11-pip \
&&  alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 100 \
&&  alternatives --set python3 /usr/bin/python3.11 \
&&  pip3.11 install poetry==1.8.4 \
&&  poetry config virtualenvs.create false \
&&  groupadd $GROUPNAME \
&&  useradd -m -s /bin/bash -g $GROUPNAME $USERNAME

COPY pyproject.toml poetry.lock $APP_PATH/

RUN --mount=type=secret,id=host_certificate_file,dst=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
    python3 -m poetry install --only first_install \
&&  python3 -m poetry install \
&&  dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo \
&&  dnf install -y \
    sudo \
    git \
    vim \
    diffutils \
    bind-utils \
    iputils \
    docker-ce-cli \
    jq \
&&  usermod -G wheel $USERNAME \
&&  echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers \
&&  echo "%${GROUPNAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# USER root
# RUN chmod a+x entrypoint.sh
USER $USERNAME
