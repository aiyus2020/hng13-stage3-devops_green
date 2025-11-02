#!/bin/bash

# Webhook URL (replace with your actual Slack webhook URL)
SLACK_WEBHOOK_URL=    # replace this with webhook URL

# Message to send
MESSAGE="Failover 🚨"

# Send to Slack
curl -X POST -H 'Content-type: application/json' \
     --data "{\"text\":\"$MESSAGE\"}" \
     $SLACK_WEBHOOK_URL

