# 乳腺癌检测应用部署指南

## 概述
本指南详细说明如何部署乳腺癌检测应用，使其能够在互联网环境中稳定运行，支持跨网络访问。

## 环境要求

### 服务器要求
- 操作系统：Linux (Ubuntu 20.04+/CentOS 7+)
- Python版本：3.8+
- 内存：至少2GB
- 存储：至少1GB可用空间

### 网络要求
- 公网IP地址
- 开放端口：8000（或自定义端口）
- 可选：SSL证书（推荐用于生产环境）

## 部署步骤

### 1. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python和虚拟环境
sudo apt install python3 python3-venv python3-dev -y

# 创建虚拟环境
cd breast-cancer-detection-master
python3 -m venv venv
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件，根据实际情况修改：

```env
FLASK_ENV=production
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

### 3. 启动应用

#### 开发环境（本地测试）

```bash
FLASK_ENV=development python start.py
```

#### 生产环境

```bash
# 方式1：使用Flask内置服务器（不推荐生产环境）
FLASK_ENV=production python start.py

# 方式2：使用Gunicorn（推荐）
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# 方式3：使用nohup后台运行
nohup gunicorn -w 4 -b 0.0.0.0:8000 app:app > app.log 2>&1 &
```

### 4. 配置Nginx反向代理（推荐）

```bash
# 安装Nginx
sudo apt install nginx -y

# 创建配置文件
sudo nano /etc/nginx/sites-available/breast-cancer.conf
```

配置内容：

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
    }

    # 静态文件缓存
    location /static/ {
        root /path/to/breast-cancer-detection-master;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 日志配置
    access_log /var/log/nginx/breast-cancer-access.log;
    error_log /var/log/nginx/breast-cancer-error.log;
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/breast-cancer.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 配置SSL证书（推荐）

使用Let's Encrypt：

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动更新证书
sudo systemctl enable --now certbot.timer
```

## 安全配置

### 防火墙配置

```bash
# 允许HTTP/HTTPS访问
sudo ufw allow 'Nginx Full'
sudo ufw allow 8000/tcp
sudo ufw enable
```

### 安全头部

应用已内置安全头部配置：

- X-Content-Type-Options: nosniff
- X-Frame-Options: SAMEORIGIN
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000; includeSubDomains

## 监控和日志

### 日志查看

```bash
# 应用日志
tail -f app.log

# Nginx日志
tail -f /var/log/nginx/breast-cancer-access.log
tail -f /var/log/nginx/breast-cancer-error.log
```

### 进程管理

```bash
# 查看进程
ps aux | grep gunicorn

# 重启应用
killall gunicorn
nohup gunicorn -w 4 -b 0.0.0.0:8000 app:app > app.log 2>&1 &
```

## 性能优化

### Gunicorn配置建议

```bash
# 根据CPU核心数调整workers
# 推荐：workers = (CPU核心数 * 2) + 1
gunicorn -w 5 -b 0.0.0.0:8000 app:app

# 启用异步工作器（如果需要）
gunicorn -w 5 -k gevent -b 0.0.0.0:8000 app:app
```

### 静态文件优化

应用已启用静态文件压缩和缓存，建议配合CDN使用。

## 故障排除

### 常见问题

1. **应用无法启动**
   - 检查端口是否被占用：`netstat -tlnp | grep 8000`
   - 检查依赖是否安装完整
   - 查看日志文件

2. **无法从外部访问**
   - 检查防火墙设置
   - 检查Nginx配置
   - 检查云服务商安全组配置

3. **SSL证书问题**
   - 确保域名解析正确
   - 检查证书有效期
   - 重新获取证书

## 备份策略

### 数据库备份

```bash
# 备份数据库
sqlite3 users.db ".backup users_backup.db"

# 定时备份（每日凌晨2点）
crontab -e
# 添加：0 2 * * * sqlite3 /path/to/users.db ".backup /path/to/backups/users_$(date +%Y%m%d).db"
```

## 更新应用

```bash
# 停止服务
killall gunicorn

# 拉取更新
git pull

# 安装新依赖
pip install -r requirements.txt

# 重启服务
nohup gunicorn -w 4 -b 0.0.0.0:8000 app:app > app.log 2>&1 &
```

## 联系支持

如有问题，请联系系统管理员。