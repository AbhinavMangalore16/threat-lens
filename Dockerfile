FROM python:3.10-slim-bookworm
WORKDIR /app

# Copy everything
COPY . /app

# Update packages
RUN apt update -y && apt install -y awscli

# Upgrade pip and install the local package in editable mode
RUN python -m pip install --upgrade pip
RUN pip install -e . 

# RUN pip install -r requirements-test.txt

# Run the app
CMD ["python3", "app.py"]
