@echo off
chcp 65001
echo ==============================================
echo        ERP 微服务 一键启动脚本
echo ==============================================
echo.

echo 🔹 启动 网关服务 gateway
start "gateway" cmd /k "python gateway/gateway.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 系统服务 system
start "system" cmd /k "python system/system.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 商品服务 product
start "product" cmd /k "python product/product.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 库存服务 stock
start "stock" cmd /k "python stock/stock.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 销售服务 sales
start "sales" cmd /k "python sales/sales.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 生产服务 production
start "production" cmd /k "python production/production.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 采购服务 purchase
start "purchase" cmd /k "python purchase/purchase.py"
timeout /t 1 /nobreak > nul


echo 🔹 启动 伙伴服务 partner
start "partner" cmd /k "python partner/partner.py"
timeout /t 1 /nobreak > nul

echo 🔹 启动 报表服务 report
start "report" cmd /k "python report/report.py"
timeout /t 1 /nobreak > nul

echo.
echo ✅ 所有服务已启动！
echo.
pause