FROM python:3.11-slim
WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY . .

ENV PORT=5000
EXPOSE 5000
CMD ["python", "server/server.py"]