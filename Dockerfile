# Use the official OpenJDK image as the base image
FROM python:3.8.9

# Set the working directory inside the container
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

# Define the command to run your application
CMD ["python3", "LoadGenerator.py" ]