FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir flask numpy numpy-financial pandas flask-cors pvlib numba
COPY . .
CMD ["python", "functions/server.py"]
EXPOSE 5002