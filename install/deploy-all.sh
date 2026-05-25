#!/bin/bash
cd /opt/erp
git pull
docker-compose down
docker-compose up -d --build
echo "✅ 所有服务更新完成！"