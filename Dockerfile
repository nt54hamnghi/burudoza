# Python 3.11 as base images
FROM python:3.11-slim-buster
# Set env poetry
ENV POETRY_VIRTUALENVS_CREATE=false \ 
    POETRY_VERSION=1.3.2 
# Set env pip
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \  
    PIP_DEFAULT_TIMEOUT=100 \ 
    PIP_NO_CACHE_DIR=off
# Install poetry
RUN pip install "poetry==$POETRY_VERSION"
# Build directory
ARG APP_DIR="/app"
# Create app dicrectory
RUN mkdir ${APP_DIR}
# Set working directory 
WORKDIR ${APP_DIR}
# Copy config files for dependency installation
COPY pyproject.toml poetry.lock ${APP_DIR}
# Install dependencies
RUN poetry install --without dev --no-interaction --no-ansi
# Copy source code over
COPY . ${APP_DIR}
# Module directory
ARG MODULE_DIR="${APP_DIR}/burudoza"
# Extend Path
ENV PATH="${APP_DIR}:${PATH}"
ENV PYTHONPATH="${MODULE_DIR}:${PYTHONPATH}"
# Expore port 
EXPOSE 8501
# Launch streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["/app/burudoza/app.py"]