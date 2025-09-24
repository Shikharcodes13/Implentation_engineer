# Windmill Setup Guide

This guide will help you set up Windmill locally for the CSV upload system.

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)
- At least 4GB RAM available for Docker containers
- Port 80 available on your system

## Installation Steps

### 1. Clone and Prepare the Project

```bash
git clone <repository-url>
cd Zenskar_assignment
```

### 2. Create Environment Configuration

Create a `.env` file in the project root:

```bash
# Windmill Configuration
WM_IMAGE=ghcr.io/windmill-labs/windmill:main
DATABASE_URL=postgresql://postgres:changeme@db:5432/windmill

# Logging Configuration
LOG_MAX_SIZE=20m
LOG_MAX_FILE=10

# Base URL for local development
BASE_URL=:80
ADDRESS=0.0.0.0
```

### 3. Start Windmill Services

```bash
# Start all services
docker-compose -f windmill-docker-compose.yml up -d

# Check service status
docker-compose -f windmill-docker-compose.yml ps
```

### 4. Verify Installation

1. Open your browser and navigate to `http://localhost`
2. You should see the Windmill login page
3. Create an admin account on first visit

### 5. Import Project Scripts

After Windmill is running:

1. Navigate to the Scripts section in Windmill UI
2. Import the scripts from the `windmill-scripts/` directory
3. Import the flows from the `flows/` directory

## Common Issues and Solutions

### Issue: Port 80 Already in Use

**Solution**: Modify the port mapping in `windmill-docker-compose.yml`:
```yaml
ports:
  - 8080:80  # Change 80 to your preferred port
```

Then update your `.env` file:
```bash
BASE_URL=:8080
```

### Issue: Database Connection Errors

**Solution**: Ensure PostgreSQL container is healthy:
```bash
docker-compose -f windmill-docker-compose.yml logs db
```

### Issue: Out of Memory

**Solution**: Reduce worker replicas in `windmill-docker-compose.yml`:
```yaml
deploy:
  replicas: 1  # Reduce from 3
```

## Service Architecture

The setup includes:

- **windmill_server**: Main Windmill server (port 8000)
- **windmill_worker**: Background job workers (3 replicas)
- **windmill_worker_native**: Native job workers (1 replica)
- **db**: PostgreSQL database
- **caddy**: Reverse proxy and load balancer
- **lsp**: Language Server Protocol for code assistance

## Accessing Windmill

- **Main Interface**: http://localhost (or your configured port)
- **API Documentation**: http://localhost/api/docs
- **Database**: postgresql://postgres:changeme@localhost:5432/windmill

## Next Steps

After successful setup:

1. Configure MockAPI.io endpoint (see [MockAPI Setup Guide](mockapi-setup.md))
2. Import the CSV processing scripts
3. Test with sample data
4. Customize transformation rules as needed

## Stopping Services

```bash
# Stop all services
docker-compose -f windmill-docker-compose.yml down

# Stop and remove volumes (WARNING: This will delete all data)
docker-compose -f windmill-docker-compose.yml down -v
```
