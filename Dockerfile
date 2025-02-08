FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY ./ ./

RUN poetry install

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "llama_mcp_streamlit/main.pyy", "--server.port=8501", "--server.address=0.0.0.0"]