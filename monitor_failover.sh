#!/bin/bash

# Containers to monitor
CONTAINERS=("app_green" "app_blue")

for CONTAINER in "${CONTAINERS[@]}"; do
    STATUS=$(docker inspect -f '{{.State.Running}}' $CONTAINER 2>/dev/null)
    if [ "$STATUS" != "true" ]; then
        # Send Slack alert
        ./notify_slack.sh "Failover 🚨 - $CONTAINER is down!"
    fi
done

