FROM python:3.11.4-slim

ENV POETRY_VERSION=1.5.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /opt

COPY poetry.lock pyproject.toml ./

#
#RUN poetry config virtualenvs.create false \
#    && poetry install --no-root

RUN poetry config virtualenvs.create false\
    && poetry install --without dev --no-root

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]