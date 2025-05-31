# 1. Base image
FROM python:3.10-slim

# 2. Set workdir
WORKDIR /app

# 3. Copy requirements (you must have a requirements.txt)
COPY backend/requirements.txt .

# 4. Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy code
COPY backend .

# 6. Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 7. Add startup script
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 8. Default run command
ENTRYPOINT ["/entrypoint.sh"]
