# Use a slim Python base image for a smaller footprint
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first to leverage Docker caching
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y curl
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=findyourmatch.settings \
    STATIC_ROOT=/app/staticfiles \
    MEDIA_ROOT=/app/media

# Expose the default Daphne port
EXPOSE 8000

# Run migrations, collect static files, and start Daphne
CMD ["sh", "-c", "python manage.py migrate && \
                   python manage.py collectstatic --noinput && \
                   daphne -b 0.0.0.0 -p 8000 findyourmatch.asgi:application"]


