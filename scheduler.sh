#!/bin/bash

# Scheduler script for model updater service
# This script is called by cron daily at 5 AM

set -e

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/model-updater.log
}

# Get the current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log "Starting daily model update at $TIMESTAMP"

# Check if model-updater service is running
if ! docker ps --format "table {{.Names}}" | grep -q "model-updater"; then
    log "Model updater service is not running, starting it..."
    
    # Get the directory where this script is located
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Navigate to the docker-compose directory
    cd "$SCRIPT_DIR/../../compose"
    
    # Start the model-updater service
    if docker-compose -f docker-compose.llm.yml up -d model-updater; then
        log "Model updater service started successfully"
        
        # Wait for the service to complete
        log "Waiting for model updater to complete..."
        timeout 300 docker-compose -f docker-compose.llm.yml logs -f model-updater | while read line; do
            echo "$line"
            if echo "$line" | grep -q "Saving free_chat_models.json"; then
                log "Model update completed successfully"
                break
            fi
        done
        
        # Stop the service after completion
        docker-compose -f docker-compose.llm.yml stop model-updater
        log "Model updater service stopped"
        
    else
        log "ERROR: Failed to start model updater service"
        exit 1
    fi
else
    log "Model updater service is already running, triggering update..."
    
    # Trigger the update by restarting the service
    cd "$SCRIPT_DIR/../../compose"
    docker-compose -f docker-compose.llm.yml restart model-updater
    
    # Wait for completion
    timeout 300 docker-compose -f docker-compose.llm.yml logs -f model-updater | while read line; do
        echo "$line"
        if echo "$line" | grep -q "Saving free_chat_models.json"; then
            log "Model update completed successfully"
            break
        fi
    done
fi

# Verify the file was updated
if [ -f "../../configs/litellm/free_chat_models.json" ]; then
    FILE_SIZE=$(stat -c%s "../../configs/litellm/free_chat_models.json")
    FILE_MOD=$(stat -c%Y "../../configs/litellm/free_chat_models.json")
    CURRENT_TIME=$(date +%s)
    
    # Check if file was modified in the last hour
    if [ $((CURRENT_TIME - FILE_MOD)) -lt 3600 ]; then
        log "SUCCESS: free_chat_models.json updated successfully (size: ${FILE_SIZE} bytes)"
    else
        log "WARNING: free_chat_models.json exists but may not have been updated recently"
    fi
else
    log "ERROR: free_chat_models.json not found after update"
    exit 1
fi

log "Daily model update completed at $(date '+%Y-%m-%d %H:%M:%S')"
