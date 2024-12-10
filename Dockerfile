FROM python:3.10.11

RUN mkdir /CS656Chat
WORKDIR /CS656Chat
ADD . /CS656Chat/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/CS656Chat/chat.py"]