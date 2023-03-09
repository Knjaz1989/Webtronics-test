FROM python:3.10-alpine3.17
COPY ./backend ./backend
WORKDIR /backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ./manager.py site run
