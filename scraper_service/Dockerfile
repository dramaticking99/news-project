# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first for layer caching
# NOTE: scraper_service should also have its own requirements.txt
COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Scrapy project code
COPY . .

# This command keeps the container running indefinitely.
# You can then run scrapes using 'docker-compose exec scraper_service scrapy crawl ...'
CMD ["tail", "-f", "/dev/null"]