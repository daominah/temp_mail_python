FROM daominah/python37

COPY ./requirements.txt /requirements.txt
RUN ${BIN_PYTHON} -m pip install -r /requirements.txt

ENV APP_DIR=/python/src/app
WORKDIR ${APP_DIR}
COPY . ${APP_DIR}

EXPOSE 16716

CMD ["bash", "-c", "${BIN_PYTHON} ${APP_DIR}/main.py"]
