FROM python:3.10-slim

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
