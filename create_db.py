import sqlite3

# 创建数据库连接
conn = sqlite3.connect('users.db')

# 创建游标
cursor = conn.cursor()

# 创建用户表（如果不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    id_card TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    password TEXT NOT NULL
)
''')

# 创建预测记录表（新增）
cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    result TEXT NOT NULL,
    prob_benign REAL NOT NULL,
    prob_malignant REAL NOT NULL,
    accuracy REAL NOT NULL,
    inference_time REAL NOT NULL,
    prediction_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# 提交更改
conn.commit()

# 关闭连接
conn.close()

print("数据库创建成功！预测记录表已添加。")
