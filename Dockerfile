FROM python:3-alpine3.7

# Install any needed packages specified in requirements.txt
RUN pip install Flask==0.11.1
RUN pip install viberbot==1.0.11
RUN pip install schedule==0.5.0

#RUN apt-get update && apt-get -q install -y --force-yes \
#    curl \
#    python-pip
RUN mkdir /app

ADD ./word_pickle /app/word_pickle

# Copy the current directory contents into the container at /app
ADD ./finder_for_bot.py /app
ADD ./viber_bot.py /app

# Set the working directory to /app
WORKDIR /app

# Make port 28888 available to the world outside this container
EXPOSE $PORT
CMD ["python", "viber_bot.py"]
