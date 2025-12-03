FROM pandoc/core:3.6.4.0-ubuntu

RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Configure a VENV to use Python in
RUN python3 -m venv /app/panenv
ENV PATH="/app/panenv/bin:$PATH"

# Install Python dependencies 
COPY requirements.txt /app/
RUN /app/panenv/bin/pip install -r /app/requirements.txt

# Copy files
COPY doc2md.py /app/
COPY markdown_cleaner.py /app/
COPY find_citation_candidates.py /app/
COPY hand_written_citations.py /app/

# Create folder for file input/output
RUN mkdir /app/files

ENTRYPOINT ["python", "/app/doc2md.py"]
