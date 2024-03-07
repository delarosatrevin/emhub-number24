
FROM python:3.8

WORKDIR /python-docker

COPY . .
RUN pip3 install -e .

RUN pwd
RUN ls

RUN python -m emhub.data --create_instance /instance
ENV EMHUB_INSTANCE /instance

# Create a new user with UID 10016
RUN addgroup -g 10016 choreo && \
    adduser  --disabled-password  --no-create-home --uid 10016 --ingroup choreo choreouser
USER 10016
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0"]
#CMD [ "gunicorn", "-k", "gevent", "--workers=2", "emhub:create_app()", "--bind", "0.0.0.0:8080" ]