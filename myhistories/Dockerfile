FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

# System deps:
RUN pip install "poetry"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /code/
