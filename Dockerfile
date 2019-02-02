FROM __BASEIMAGE_ARCH__/python:3.6-alpine3.8
WORKDIR /pyduofern-server

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
