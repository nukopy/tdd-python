FROM python:3.9

LABEL  maintainer "nukopy <pytwbf201830@gmail.com>"

WORKDIR /workdir

# install packages
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      git \
    && rm -rf /var/lib/apt/lists/*

# install Python packages
RUN pip install -U --no-cache-dir pip poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install

# pythonpath setting
ENV PYTHONPATH "/"

CMD ["/bin/bash"]