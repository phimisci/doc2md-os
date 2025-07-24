FROM pandoc/core:3.6.4.0-ubuntu

RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        git \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Configure a VENV to use Python in
ENV PANENV = /app/panenv
RUN python3 -m venv $PANENV
ENV PATH="$PANENV/bin:${PATH}"

# Install Python dependencies 
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copy files
COPY doc2md.py /app/
COPY markdown_cleaner.py /app/
COPY find_citation_candidates.py /app/
COPY hand-written-citations.py /app/

# Create folder for file input/output
RUN mkdir /app/files

ENTRYPOINT ["/app/venv/bin/python", "/app/doc2md.py"]
