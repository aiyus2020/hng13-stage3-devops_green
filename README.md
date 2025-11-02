# 🚀 Stage 3: Blue-Green Deployment with Automated Slack Alerts

**Author:** Sandra Olisama  
**Project:** DevOps Stage 3 — Observability, Failover & Alerting  
**Date:** November 2025  

---

## 🧭 Overview

This project implements a **Blue-Green Deployment strategy** with **automated monitoring and alerting**.  
It extends the previous Stage 2 setup by introducing:

- 🟦 **Blue** and 🟩 **Green** application environments (zero-downtime switching)
- 🔁 **Nginx reverse proxy** for traffic routing between blue and green pools
- 🧠 **Python-based Watcher** that monitors logs and posts **Slack alerts**
- ⚡ **Chaos testing** to simulate failovers and high error rates
- 📟 **Slack notifications** for observability and recovery actions

---

## 🧩 Architecture

```text
                ┌────────────────────────────────────────────┐
                │                  SLACK                     │
                │  #alerts-channel ← watcher.py sends alerts  │
                └────────────────────────────────────────────┘
                                 ▲
                                 │
                   ┌──────────────────────────┐
                   │  Alert Watcher (Python)  │
                   │ - Reads Nginx logs       │
                   │ - Detects errors/failover│
                   │ - Posts alerts to Slack  │
                   └──────────────────────────┘
                                 ▲
                                 │ Shared Volume (nginx_logs)
                                 ▼
           ┌────────────────────────────────────────────┐
           │                   NGINX                   │
           │  - Routes traffic between Blue/Green apps  │
           │  - Logs requests & upstream status         │
           └────────────────────────────────────────────┘
               ▲                      ▲
               │                      │
    ┌───────────────────┐   ┌───────────────────┐
    │   App (Blue)      │   │   App (Green)     │
    │ port: 8081        │   │ port: 8082        │
    └───────────────────┘   └───────────────────┘


