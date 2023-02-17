FROM python:3.10-slim
WORKDIR /code
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 8090
CMD ["python", "/code/app/main.py", "--host", "0.0.0.0", "--port", "8090"]

