#!/bin/bash
set -e

SERVICE=$1

if [ -z "$SERVICE" ]; then
  echo "用法：./deploy-service.sh system"
  exit 1
fi

echo "==================================="
echo " 正在部署：$SERVICE"
echo "==================================="

cd /opt/erp

git pull

docker-compose build $SERVICE
docker-compose up -d $SERVICE

echo "✅ $SERVICE 部署完成！"