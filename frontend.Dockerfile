# frontend.Dockerfile

FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend code
COPY frontend/ .
#COPY frontend/app.py .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

