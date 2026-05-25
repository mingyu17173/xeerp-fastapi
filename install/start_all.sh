#!/bin/bash

# 编码与颜色
export LANG=zh_CN.UTF-8
GREEN="\033[32m"
NC="\033[0m"

echo "=========================================="
echo "       ERP 微服务 一键启动脚本"
echo "=========================================="

# 启动函数
start_service() {
    local name=$1
    local dir=$2
    local file=$3
    echo -e "${GREEN}🔹 启动 $name ...${NC}"
    cd "$dir" || exit
    nohup python "$file" > ../logs/$name.log 2>&1 &
    sleep 1
    cd ..
}

# 创建日志目录
mkdir -p logs

# 依次启动所有服务
start_service "gateway"      "gateway"      "main.py"
start_service "system"       "system"       "system.py"
start_service "product"      "product"      "product.py"
start_service "stock"        "stock"        "stock.py"
start_service "sales"        "sales"        "sales.py"
start_service "production"   "production"   "production.py"
start_service "partner"      "partner"      "partner.py"
start_service "report"       "report"       "report.py"

echo "✅ 所有服务已后台启动完成！"
echo "📋 查看日志：tail -f logs/xxx.log"