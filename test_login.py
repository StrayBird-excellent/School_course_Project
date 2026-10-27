#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试登录流程的脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, session
import sqlite3
import hashlib

def test_login_flow():
    """测试登录流程"""
    print("=== 测试登录流程 ===")
    
    # 模拟Flask应用
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY') or 'dev-only-placeholder-change-via-env'
    
    # 测试数据库连接
    print("\n1. 测试数据库连接...")
    try:
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(f"   数据库连接成功，找到 {len(users)} 个用户")
        for user in users:
            print(f"   - 用户: {user['name']}, 手机号: {user['phone']}")
        conn.close()
    except Exception as e:
        print(f"   数据库连接失败: {e}")
        return False
    
    # 测试密码哈希
    print("\n2. 测试密码哈希...")
    test_password = "123456"
    hashed_password = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"   原始密码: {test_password}")
    print(f"   哈希密码: {hashed_password}")
    
    # 测试用户验证
    print("\n3. 测试用户验证...")
    try:
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        user = conn.execute("SELECT * FROM users WHERE phone = ?", ("11111111111",)).fetchone()
        if user:
            print(f"   找到用户: {user['name']}")
            print(f"   数据库密码哈希: {user['password']}")
            print(f"   测试密码哈希: {hashed_password}")
            if user["password"] == hashed_password:
                print("   ✓ 密码验证成功")
            else:
                print("   ✗ 密码验证失败")
        else:
            print("   ✗ 未找到用户")
        conn.close()
    except Exception as e:
        print(f"   用户验证失败: {e}")
        return False
    
    print("\n=== 测试完成 ===")
    return True

if __name__ == "__main__":
    success = test_login_flow()
    sys.exit(0 if success else 1)