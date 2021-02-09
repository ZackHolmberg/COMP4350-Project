# Use the python3.7 container image
FROM python:3.7-alpine

# Set the working directory to /src
WORKDIR /src

# Copy the current directory contents into the container at /src
ADD . /src

# Install the dependencies within container

RUN set -e; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    ; \
    pip install -r requirements.txt; \
    apk del .build-deps;

# start uWSGI application server
CMD ["uwsgi", "uwsgi.ini"]