# --- Base Stage ---
FROM node:20-slim AS base

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies (including test dependencies)
RUN npm install

# Copy source code
COPY . .

# --- Test Stage ---
FROM base AS test
RUN echo "Running frontend tests..." && \
    npm test -- --passWithNoTests || \
    (echo "Frontend tests failed!" && exit 1)

# --- Production Stage ---
FROM python:3.12-slim-bookworm AS production

WORKDIR /app

# Copy only production files (no tests, no node_modules)
COPY index.html script.js ./

# Expose port 5500
EXPOSE 5500

# Serve static frontend
CMD ["python", "-m", "http.server", "5500"]