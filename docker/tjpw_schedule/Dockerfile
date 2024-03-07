FROM python:3.11-slim-buster

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en

WORKDIR /app

RUN \
  pip install selenium>=4.11.2 && \
  pip install python-dateutil>=2.8.2 && \
  pip install requests>=2.31.0

ENTRYPOINT [ "python" ]
CMD [ "-m", "tjpw_schedule" ]
