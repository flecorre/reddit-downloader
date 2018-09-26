FROM python:3.5-alpine
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade oauth2client
RUN pip3 install -r requirements.txt
CMD ["python", "./reddit.py"]
