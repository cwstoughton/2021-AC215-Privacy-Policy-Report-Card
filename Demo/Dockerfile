# Use the official Debian-hosted Python image
FROM python:3.8-slim-buster

ENV PYENV_SHELL=/bin/bash

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential ffmpeg && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    mkdir -p /app 


# Expose port
EXPOSE 9000
    
    
WORKDIR /app

ADD --chown=app:app Pipfile /app/

RUN pipenv install

ADD --chown=app:app . /app

# Entry point
ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]

# ENTRYPOINT ["/bin/bash"]

# CMD ["-c", "pipenv shell"]
# CMD ["uvicorn", "app:app", "--reload"]


