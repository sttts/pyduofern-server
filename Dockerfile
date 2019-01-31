FROM python:3.6

WORKDIR /pyduofern-server

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
