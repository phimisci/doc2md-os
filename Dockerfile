FROM pandoc/core:3.4.0.0-ubuntu

RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        git \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy files
COPY markdown_cleaner /app/markdown_cleaner
COPY doc2md.py /app/doc2md.py
COPY requirements.txt /app/requirements.txt

# Create folder for file input/output
RUN mkdir /app/files

ENTRYPOINT ["python3", "/app/doc2md.py"]