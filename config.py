# 应用配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-placeholder-change-via-env'
    
    # 数据库配置
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///users.db'
    
    # 服务器配置
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5000)
    
    # 安全配置
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 静态文件缓存时间（秒）
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1年

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 8000)
    
    # 生产环境安全设置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 启用永久会话
    PERMANENT_SESSION_LIFETIME = 3600  # 1小时

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True

# 配置映射
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# 获取当前配置
def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)