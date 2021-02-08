# Use the python3.7.2 container image
FROM python:3.7.2-stretch

# Set the working directory to /src
WORKDIR /src

# Copy the current directory contents into the container at /src
ADD . /src

# Install the dependencies within container
RUN pip install -r requirements.txt

# start uWSGI application server
CMD ["uwsgi", "uwsgi.ini"]