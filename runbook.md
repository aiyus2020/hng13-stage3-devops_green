# Runbook — Blue/Green Observability & Alerts

## Overview
This runbook explains alerts emitted by the log-watcher and the recommended operator actions.

### Alert types
1. **Failover detected** (Blue → Green or Green → Blue)
   - **Meaning:** Nginx observed that upstream pool changed from primary to backup. Usually immediate cause: primary returned error or timed out.
   - **Immediate actions:**
     1. Check Nginx logs: `docker compose logs nginx` or `tail logs/nginx/access.log`.
     2. Inspect primary container: `docker logs app_blue` (or `app_green`).
     3. Check health endpoint: `curl http://localhost:8081/healthz` (or :8082).
     4. If it's an unwanted failure, restart the primary container:
        `docker restart app_blue`
     5. If intentional (maintenance), acknowledge in Slack channel and set `MAINTENANCE_MODE=1` (see suppression below).
2. **High error-rate detected**
   - **Meaning:** Last N requests contain > `ERROR_RATE_THRESHOLD`% 5xx responses.
   - **Immediate actions:**
     1. Run `docker compose logs app_blue --tail 200` and same for `app_green`.
     2. Identify recent deploys or config changes (look at `X-Release-Id`).
     3. Consider toggling active pool (call reload script or update `ACTIVE_POOL` and run `docker compose restart nginx`).
     4. Roll back recent deploy or increase capacity if under load.
3. **Recovery notification**
   - **Meaning:** System returned to normal (error rate dropped below threshold).
   - **Action:** No immediate action; verify app metrics and close incident.

## Suppression / Maintenance Mode
To avoid spamming alerts during planned maintenance:
- Set environment var `MAINTENANCE_MODE=1` in `.env` and restart `alert_watcher`.
- The watcher respects maintenance mode by not posting alerts (you will need to implement a simple `if os.environ.get('MAINTENANCE_MODE') == '1'` check in watcher.py or stop the watcher container temporarily).

## Where to look
- Nginx logs: `logs/nginx/access.log`
- Watcher logs: `docker logs alert_watcher`
- App logs: `docker logs app_blue` / `docker logs app_green`

## Escalation
- If repeated failovers or persistent high error rates occur, escalate to platform lead with:
  - time window, error rate, last deployment id (X-Release-Id), and container logs.

