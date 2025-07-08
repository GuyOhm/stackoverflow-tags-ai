# 
# Base image with all dependencies
#

FROM python:3.12-slim as base

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files and install dependencies
COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv pip install -e . --system

#
# API image
#
FROM base as api

# The API needs the models, which will be mounted as a volume.
# We create the directory so that permissions are correct if a volume is mounted.
RUN mkdir -p /app/models

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

#
# Streamlit image
#
FROM base as streamlit

EXPOSE 8501
CMD ["streamlit", "run", "src/streamlit/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"] 