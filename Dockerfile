# Use official Python image
FROM python:3.11-slim

LABEL maintainer="Jesus Alcocer Tagua"
LABEL org.opencontainers.image.description="Testing MCP with Ollama and Streamlit"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Install Node.js and npx (corrected)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -f /usr/bin/npx && \
    npm install -g npx

# Set working directory
WORKDIR /app

# Copy project files (ensure poetry.lock is included)
COPY poetry.lock pyproject.toml /app/
COPY ./ ./

# Install Python dependencies with Poetry (corrected)
RUN poetry install --no-root

# Expose the Streamlit default port
EXPOSE 8501

# Run the Streamlit app
#ENTRYPOINT ["streamlit", "run", "llama_mcp_streamlit/main.py", "--server.port=8501", "--server.address=0.0.0.0"]

##############

# # Use official Python image
# FROM python:3.11-slim

# LABEL maintainer="Jesus Alcocer Tagua"
# LABEL org.opencontainers.image.description="Testing MCP with Ollama and Streamlit"

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PIP_NO_CACHE_DIR=1 \
#     PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PIP_ROOT_USER_ACTION=ignore

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     curl \
#     git \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Install Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="/root/.local/bin:$PATH"

# # Install Node.js and npx
# RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
#     apt-get install -y nodejs && \
#     npm install -g npx

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY ./ ./

# # Install Python dependencies with Poetry
# RUN poetry install --no-root --no-dev

# # Expose the Streamlit default port
# EXPOSE 8501

# # Run the Streamlit app
# ENTRYPOINT ["streamlit", "run", "llama_mcp_streamlit/main.py", "--server.port=8501", "--server.address=0.0.0.0"]