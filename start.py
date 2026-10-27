#!/usr/bin/env python3
"""
启动脚本 - 支持跨网络环境访问

使用方式：
    # 开发环境
    python start.py

    # 生产环境
    FLASK_ENV=production python start.py

    # 指定端口
    PORT=8000 python start.py

环境变量：
    FLASK_ENV: 运行环境 (development/production/testing)
    HOST: 监听地址 (默认: 0.0.0.0)
    PORT: 监听端口 (默认: 5000/8000)
    DEBUG: 是否开启调试模式
    SECRET_KEY: 会话密钥
"""

import os
import sys
from app import app
from config import get_config

def setup_production_environment(app):
    """配置生产环境"""
    from flask_talisman import Talisman
    from flask_compress import Compress
    
    # 启用响应压缩
    Compress(app)
    
    # 安全头部设置
    Talisman(app, content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://ajax.googleapis.com https://maxcdn.bootstrapcdn.com",
        'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://maxcdn.bootstrapcdn.com",
        'font-src': "'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com",
        'img-src': "'self' data:",
        'connect-src': "'self'",
    })
    
    # 信任代理（用于部署在反向代理后）
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    print("✓ 生产环境安全配置已启用")

def setup_performance_enhancements(app):
    """配置性能优化"""
    # 启用静态文件缓存
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1年
    
    # 配置响应头
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response
    
    print("✓ 性能优化配置已启用")

def main():
    # 获取配置
    config = get_config()
    env = os.environ.get('FLASK_ENV', 'development')
    
    print(f"🚀 启动 Breast Cancer Detection 应用")
    print(f"📊 运行环境: {env}")
    print(f"🌐 监听地址: {config.HOST}:{config.PORT}")
    
    # 加载配置
    app.config.from_object(config)
    
    # 生产环境配置
    if env == 'production':
        setup_production_environment(app)
        setup_performance_enhancements(app)
    
    # 确保分类器加载
    from app import ensure_clf
    ensure_clf()
    print("✓ 机器学习模型已加载")
    
    # 启动应用
    try:
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True,
            use_reloader=config.DEBUG
        )
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()