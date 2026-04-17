FROM python:3.13
COPY requirements.txt /bookapp/requirements.txt
WORKDIR /bookapp
RUN pip install -r requirements.txt
COPY . /bookapp
ENTRYPOINT ["python"]
CMD ["app.py"]