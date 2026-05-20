#!/bin/bash
check() {
    port=$1
    name=$2
    if ! lsof -i TCP:$port | grep LISTEN >/dev/null 2>&1; then
        echo "🚨 $name 挂了，自动重启..."
        cd /app/$name && nohup gunicorn main:app -c gunicorn_conf.py >> ../logs/restart.log 2>&1 &
    fi
}

check 8000 gateway-service
check 8001 system-service
check 8002 product-service
check 8003 stock-service
check 8004 production-service
check 8005 report-service
check 8006 approval-service
check 8007 partner-service