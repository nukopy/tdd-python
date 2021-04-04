FROM python:3.9

LABEL  maintainer "nukopy <pytwbf201830@gmail.com>"

WORKDIR /workdir

ENV PACKAGE_NAME "tasks"
ENV PACKAGE_VERSION "0.1.0"

# install packages
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -U --no-cache-dir pip poetry

# install Python packages
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project false
RUN poetry install

# PYTHONPATH
ENV PYTHONPATH "/workdir/src"

CMD ["/bin/bash"]