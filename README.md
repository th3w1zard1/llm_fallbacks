# LLM Fallbacks CI/CD System

This directory contains the CI/CD infrastructure for automatically updating the `free_chat_models.json` file daily at 5 AM using your `generate_configs.py` script.

## Overview

The system replaces the hardcoded configmaps in your Docker Compose file with a dynamic configuration system that:

1. **Automatically generates** `free_chat_models.json` daily at 5 AM
2. **Runs entirely in containers** (no host cron required)
3. **Integrates with your existing** Docker Compose setup
4. **Provides CI/CD pipeline** for automated testing and deployment

## Architecture

### Services

- **`model-scheduler`**: Alpine-based cron service that runs daily at 5 AM
- **`model-updater`**: Python service that executes `generate_configs.py`
- **`litellm`**: Your existing LiteLLM service (now uses dynamic config)

### Data Flow

```
Daily at 5 AM:
model-scheduler → triggers → model-updater → generates → free_chat_models.json
                                                      ↓
                                              litellm service uses updated config
```

## Files

### Docker Images
- `Dockerfile.model-updater`: Python service for running generate_configs.py
- `Dockerfile.scheduler`: Alpine-based cron scheduler
- `requirements.txt`: Python dependencies for the model updater

### Scripts
- `scheduler.sh`: Cron job script that triggers model updates
- `deploy-llm-fallbacks.sh`: Deployment script for the entire system

### Configuration
- `docker-compose.llm.yml`: Updated Docker Compose with new services
- `.github/workflows/llm-fallbacks-ci.yml`: GitHub Actions CI/CD pipeline

## Quick Start

### 1. Deploy the System

```bash
# From the project root
./scripts/deploy-llm-fallbacks.sh deploy
```

### 2. Check Status

```bash
./scripts/deploy-llm-fallbacks.sh status
```

### 3. Force Model Update

```bash
./scripts/deploy-llm-fallbacks.sh update
```

### 4. View Logs

```bash
./scripts/deploy-llm-fallbacks.sh logs
```

## Manual Deployment

If you prefer to deploy manually:

```bash
# Build images
cd src/llm_fallbacks
docker build -f Dockerfile.model-updater -t llm-fallbacks:model-updater .
docker build -f Dockerfile.scheduler -t llm-fallbacks:scheduler .

# Deploy services
cd ../../compose
docker-compose -f docker-compose.llm.yml up -d
```

## Configuration

### Environment Variables

The system requires these environment variables:

- `OPENROUTER_API_KEY`: For fetching model information
- `POSTGRES_PASSWORD`: For database connections
- `TZ`: Timezone (defaults to UTC)

### Volume Mounts

- `/var/run/docker.sock`: For scheduler to control Docker containers
- `${CONFIG_PATH}/litellm`: For storing generated configuration files
- `scheduler-logs`: For storing scheduler logs

## Monitoring

### Health Checks

- **model-scheduler**: Runs continuously with cron daemon
- **model-updater**: Runs on-demand, completes and stops
- **litellm**: Standard health check endpoint

### Logs

```bash
# View all logs
docker-compose -f compose/docker-compose.llm.yml logs

# View specific service logs
docker-compose -f compose/docker-compose.llm.yml logs model-scheduler
docker-compose -f compose/docker-compose.llm.yml logs model-updater
```

### Troubleshooting

1. **Check if scheduler is running**:
   ```bash
   docker ps | grep model-scheduler
   ```

2. **Check cron logs**:
   ```bash
   docker exec model-scheduler cat /var/log/model-updater.log
   ```

3. **Force manual update**:
   ```bash
   ./scripts/deploy-llm-fallbacks.sh update
   ```

## CI/CD Pipeline

The GitHub Actions workflow provides:

- **Automated testing** on multiple Python versions
- **Docker image building** and testing
- **Daily model updates** via scheduled runs
- **Manual trigger** for forced updates
- **Automatic commits** of updated model configurations

### Workflow Triggers

- **Push/PR**: Runs tests and builds on code changes
- **Schedule**: Daily at 6 AM UTC (tests model updater)
- **Manual**: Workflow dispatch for forced updates

## Security Considerations

- **Docker socket access**: The scheduler needs access to Docker socket to control containers
- **API keys**: Store sensitive keys as environment variables or secrets
- **Non-root containers**: All services run as non-root users
- **Read-only volumes**: Where possible, volumes are mounted read-only

## Customization

### Change Update Schedule

Edit `Dockerfile.scheduler`:
```dockerfile
# Change from "0 5 * * *" to your preferred schedule
RUN echo "0 5 * * * /app/scheduler.sh" > /var/spool/cron/crontabs/root
```

### Add More Providers

Modify `generate_configs.py` to include additional model providers in the `CUSTOM_PROVIDERS` list.

### Custom Health Checks

Add health check endpoints to your services and update the Docker Compose file accordingly.

## Backup and Recovery

### Backup Configuration

```bash
# Backup current configuration
cp configs/litellm/free_chat_models.json configs/litellm/free_chat_models.json.backup
```

### Restore Configuration

```bash
# Restore from backup
cp configs/litellm/free_chat_models.json.backup configs/litellm/free_chat_models.json
docker-compose -f compose/docker-compose.llm.yml restart litellm
```

## Performance Considerations

- **Model updater**: Runs on-demand, minimal resource usage
- **Scheduler**: Lightweight Alpine container, minimal overhead
- **Caching**: Uses Docker volumes for persistent storage
- **Parallel execution**: Services can run independently

## Support

For issues or questions:

1. Check the logs: `./scripts/deploy-llm-fallbacks.sh logs`
2. Verify service status: `./scripts/deploy-llm-fallbacks.sh status`
3. Test manual update: `./scripts/deploy-llm-fallbacks.sh update`
4. Review this README for troubleshooting steps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
