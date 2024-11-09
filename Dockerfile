# Dockerfile

# Use Python 3.11
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock first
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the application code
COPY src/ ./src/
COPY main.py ./

# Command to run your application
CMD ["python", "main.py"]
