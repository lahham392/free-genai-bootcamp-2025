FROM python:3.9-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose ports for GraphQL server and Streamlit
EXPOSE 5001
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create an entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
