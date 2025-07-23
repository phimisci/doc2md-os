FROM pandoc/core:3.6.4.0-ubuntu

RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        git \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy files
COPY markdown_cleaner.py /app/markdown_cleaner.py
COPY find_citation_candidates.py /app/find_citation_candidates.py
COPY hand-written-citations.py /app/hand-written-citations.py
COPY doc2md.py /app/doc2md.py
COPY requirements.txt /app/requirements.txt

# Create folder for file input/output
RUN mkdir /app/files

ENTRYPOINT ["python3", "/app/doc2md.py"]
