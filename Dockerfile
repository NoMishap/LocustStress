# Start from python 3
FROM python:3

# Set the loading test application folder
WORKDIR /home/load-test

# Install python dependencies
RUN pip install -r requirements.txt

# Expose locust required ports
EXPOSE 5557 5558 8089

# Copy the content into the image
COPY . .