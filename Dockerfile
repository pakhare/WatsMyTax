# Build app
FROM python:3.9-slim AS backend

# Set working directory for backend
WORKDIR ./app

# Install backend dependencies
COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . /app

EXPOSE 8080

# Start gunicorn server for backend
CMD [ "python", "streamlit_app.py" ]
