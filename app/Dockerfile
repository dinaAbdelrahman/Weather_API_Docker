##Setup the base image
from python=3.6.2

##Setup a key-value label for the Docker image
label maintainer="Dina AbdelRahman"

##Copy files from the host to the container
Copy . /app

##define the working directory for the container
WORKDIR /app

##install dependencies defined in the requirements.txt
RUN pip install -r requirements.txt

##starting the application
CMD ["python","app.py"]









