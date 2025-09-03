ARG USERNAME=app_user
ARG GROUPNAME=app_user
ARG APP_PATH=/workspace

FROM    registry.access.redhat.com/ubi9/ubi-init:9.4 as common_build
ARG USERNAME
ARG GROUPNAME
ARG APP_PATH

WORKDIR $APP_PATH

# ensure local pypy3 is preferred over distribution pypy3
ENV PATH /opt/pypy/bin:$PATH

# Python 3.11.13
ENV PYPY_VERSION 7.3.20

RUN --mount=type=secret,id=host_certificate_file,dst=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
    set -eux \
&&  dnf install -y \
    langpacks-en \
    wget \
    unzip \
    gcc \
    bzip2 \
    # python3.11 \
    # python3.11-devel \
    # python3.11-pip
#     alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 100 \
# &&  alternatives --set python3 /usr/bin/python3.11 \
&&  wget -O pypy.tar.bz2 https://downloads.python.org/pypy/pypy3.11-v7.3.20-linux64.tar.bz2 --progress=dot:giga \
&&  mkdir /opt/pypy \
&&  tar -xjC /opt/pypy --strip-components=1 -f pypy.tar.bz2 \
&&  find /opt/pypy/lib* -depth -type d -a \( -name test -o -name tests \) -exec rm -rf '{}' + \
&&  rm pypy.tar.bz2 \
&&  alternatives --install /usr/bin/python3 python3 /opt/pypy/bin/python3.11 100 \
&&  alternatives --set python3 /opt/pypy/bin/python3.11 \
&&  alternatives --install /usr/bin/pip3.11 pip3.11 /opt/pypy/bin/pip3.11 100 \
&&  alternatives --set pip3.11 /opt/pypy/bin/pip3.11 \
&&  python3 -m ensurepip \
&&  pip3.11 install --disable-pip-version-check --no-cache-dir --no-compile 'wheel<0.46' \
&& 	find /opt/pypy -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' + \
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
