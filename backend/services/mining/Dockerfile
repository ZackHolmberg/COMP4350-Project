# Use the python3.7 container image
FROM python:3.8-alpine

# Set the working directory to /src
WORKDIR /src

# Copy the current directory contents into the container at /src
ADD . /src

# Install the dependencies within container

RUN pip install -r requirements.txt \
    pip install flask-socketio flask-cors; 

ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 5000
# start gUnicorn application server
CMD ["flask", "run"]