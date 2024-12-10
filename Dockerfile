FROM python:3.12.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ /app
EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]
