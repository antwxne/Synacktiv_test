FROM python:3.12.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ /app
RUN touch secret.json
EXPOSE 8000

# CMD ["fastapi", "run", "main.py", "--port", "8000"]
CMD ["fastapi", "dev", "main.py", "--port", "8000"]