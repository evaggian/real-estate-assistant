FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

# Expose port 5500
EXPOSE 5500

# Serve static frontend
CMD ["python", "-m", "http.server", "5500"]