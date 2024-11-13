# This Dockerfile sets up a container environment for running the doc2md.py script.
# It uses the pandoc/core:3.4.0.0-ubuntu base image and installs Python 3, Git, and other dependencies.
# The working directory is set to /app, and the necessary files are copied into the container.
# Finally, the entrypoint is set to run the doc2md.py script using Python 3.

FROM pandoc/core:3.4.0.0-ubuntu

RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        git \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# copy files
COPY markdown_cleaner /app/markdown_cleaner
COPY doc2md.py /app/doc2md.py
COPY requirements.txt /app/requirements.txt

# create folder for file input/output
RUN mkdir /app/files

ENTRYPOINT ["python3", "/app/doc2md.py"]