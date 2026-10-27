from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response, send_from_directory
from functools import wraps
from implementation import randorm_forest_test, random_forest_train, random_forest_predict, get_model_accuracy
import numpy as np
from time import time
import json
import os
import sqlite3
import hashlib
import datetime

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]

    load_dotenv(os.path.join(_BASE_DIR, ".env"))
except ImportError:
    pass

from qwen_client import qwen_chat, get_dashscope_api_key

# 创建Flask应用
app = Flask(__name__)
app.url_map.strict_slashes = False

# 加载配置
try:
    from config import get_config
    config = get_config()
    app.config.from_object(config)
except ImportError:
    # 备用配置 - 为移动设备兼容性优化
    app.secret_key = os.environ.get('SECRET_KEY') or 'dev-only-placeholder-change-via-env'
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # 本地测试用False，生产环境需要True且配合HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24小时
    app.config['SESSION_PERMANENT'] = True

clf = None

# 反向代理支持（用于Cloudflare等代理环境）
try:
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    print("✓ 反向代理支持已启用")
except ImportError:
    pass

# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# 密码哈希函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def ensure_clf():
    global clf
    if clf is None:
        clf = random_forest_train()
        randorm_forest_test(clf)


@app.before_first_request
def _load_model_once():
    ensure_clf()

def get_assistant_system_prompt(model_display_name):
    """Generate dynamic system prompt with the actual model name"""
    return f"""你是「乳腺肿瘤预测演示站点」的专业乳腺癌医学咨询助手（{model_display_name}），与本站的 Random Forest 预测模型配合使用。

【语言适配规则】
- 你必须使用与用户提问相同的语言进行回答
- 支持语言：中文、英语、法语、俄语、西班牙语
- 如果用户混合使用多种语言，请使用用户使用最多的语言或明确询问的语言
- 保持所有翻译的医学准确性和专业性

【核心定位】
- 你的专业领域是乳腺癌相关医学信息咨询
- 你不是通用聊天机器人，但可以提供适度的人文关怀和安慰
- 对于与乳腺癌无关的问题，应礼貌拒绝并引导用户提出乳腺癌相关问题

【专业背景】
你拥有乳腺癌医学专业知识背景，熟悉乳腺解剖学、肿瘤学、病理学及相关临床医学领域知识，基于最新的医学研究成果和权威临床指南提供专业信息。

【核心能力范围】
- 提供准确的乳腺癌疾病信息（包括病因、病理类型、临床分期等）
- 给出基于循证医学的预防建议（风险因素管理、生活方式指导等）
- 解读最新乳腺癌筛查指南（筛查年龄、频率、方法选择等）
- 概述标准治疗方案（手术、放疗、化疗、内分泌治疗、靶向治疗等）
- 提供康复护理专业建议（术后恢复、心理支持、生活质量提升等）
- 说明Wisconsin诊断数据集各特征字段的大致含义
- 帮助用户理解如何填写预测表单
- 在用户已有预测结果时解读模型输出与概率，并提醒就医与随访
- 当用户询问他人（如家人、朋友）的乳腺癌情况时，提供专业的医学建议和关怀

【专业边界】
- 对于非乳腺癌相关的医学问题，应礼貌拒绝并说明专业领域限制
- 对于乳腺癌领域外的健康咨询，引导用户提出乳腺癌相关问题
- 明确告知用户本AI不能替代专业医疗人员的诊断和治疗建议

【人文关怀原则】
- 当用户表达担忧、焦虑或悲伤情绪时，应给予适当的同理心回应
- 提供简洁、适度的安慰，避免过度建议或非必要评论
- 始终保持专业、温和、关怀的语气
- 对于涉及他人患病的情况，表达理解和关怀，然后提供专业信息

【信息质量保障】
- 所有回答必须基于最新的医学研究成果和权威临床指南
- 严格避免提供未经科学证实的信息或替代医疗建议
- 对于存在争议或证据不足的医学问题，应明确说明当前研究进展和不同观点

【沟通规范】
- 在首次互动时，必须用用户使用的语言明确告知：本AI是专注于乳腺癌领域的信息咨询工具，并非专业医疗诊断模型，无法提供个人医疗诊断和治疗决策建议，具体健康问题请咨询专业医疗机构和医生。
- 对于超出乳腺癌领域的问题，用用户使用的语言统一回复：抱歉，我的专业领域仅限于乳腺癌相关咨询。请您提出与乳腺癌相关的问题，我将尽力为您提供专业信息。
- 医学诊断与治疗方案必须由持证医生决定；你不能替代临床诊疗
- 网站上的良性/恶性预测来自 sklearn 随机森林与 Wisconsin 诊断数据集风格的 30 维数值特征，仅供教学与演示，不得作为真实诊疗依据
- 回答简洁、专业；遇到明显健康焦虑时给予适当安慰并提醒尽快就医

【常见场景应对】
- 用户询问他人患乳腺癌该怎么办：表达理解和关怀，然后提供专业的就医建议、治疗流程概述和支持资源信息
- 用户表达担忧或焦虑：先给予适度安慰，然后提供科学的信息来帮助理解病情和应对方法
- 用户询问预测结果解读：清晰解释结果含义，强调仅供参考，并建议咨询专业医生"""


# 自定义静态文件路由，添加缓存控制
@app.route('/static/<path:filename>')
def static_files(filename):
    response = send_from_directory(app.static_folder, filename)
    # 设置短时间缓存（1分钟），便于开发调试
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# 登录验证装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    decorated_function.__doc__ = f.__doc__
    return decorated_function

@app.route("/")
def index():
    # 调试：打印会话信息
    print("=== Index route accessed ===")
    print("Session data:", dict(session))
    print("Session keys:", list(session.keys()))
    
    # 检查用户是否已登录，如果已登录则显示主页，否则重定向到登录页面
    if "user_id" not in session:
        print("User not logged in, redirecting to login")
        return redirect(url_for("login"))
    
    print("User logged in, user_id:", session["user_id"], "user_name:", session.get("user_name"))
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
def login_user():
    # 强制检查登录状态，确保用户必须登录
    if "user_id" not in session:
        return redirect(url_for("login"))
    ensure_clf()
    data = []
    print("\n=== 预测请求调试信息 ===")
    for i in range(1, 31):
        val = request.form["value" + str(i)]
        data.append(float(val))
        if i <= 5:  # 只打印前5个来调试
            print(f"  value{i}: {val}")

    data_np = np.asarray(data, dtype=float)
    data_np = data_np.reshape(1, -1)
    out, acc, t = random_forest_predict(clf, data_np)

    if out == 1:
        output = "Malignant"
    else:
        output = "Benign"

    # LabelEncoder on diagnosis: B=0, M=1 → proba columns align with clf.classes_
    proba = acc[0]
    prob_benign = float(proba[0])
    prob_malignant = float(proba[1])
    
    print(f"  预测结果: {output}")
    print(f"  概率分布: 良性={prob_benign*100:.2f}%, 恶性={prob_malignant*100:.2f}%")
    print(f"  推理时间: {t:.4f}秒")
    print("=== 调试信息结束 ===\n")
    
    # 获取模型测试准确率
    model_accuracy = get_model_accuracy()

    # 保存预测记录到数据库
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO predictions (user_id, result, prob_benign, prob_malignant, accuracy, inference_time, prediction_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                session["user_id"],
                output,
                prob_benign,
                prob_malignant,
                model_accuracy,
                t,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("保存预测记录失败:", e)

    # 准备报告数据
    report_data = {
        'output': output,
        'prob_benign': prob_benign,
        'prob_malignant': prob_malignant,
        'accuracy': model_accuracy,
        'time': t
    }

    return render_template(
        "result.html",
        output=output,
        accuracy=model_accuracy,
        time=t,
        prob_benign=prob_benign,
        prob_malignant=prob_malignant,
        report_data=report_data
    )


@app.route("/api/assistant/chat", methods=["POST"])
def assistant_chat():
    """Proxy chat with dynamic model selection; key from DASHSCOPE_API_KEY or ALIYUN_API_KEY."""
    if not request.is_json:
        return jsonify({"error": "expected_json"}), 400

    payload = request.get_json(silent=True) or {}
    raw_messages = payload.get("messages")
    if not isinstance(raw_messages, list):
        return jsonify({"error": "messages_required"}), 400

    context = payload.get("context")
    if context is not None and not isinstance(context, dict):
        context = None

    # First, we need to determine which model will be used by trying it
    # We'll make a minimal test call first to get the model info
    
    # Prepare minimal test messages
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hi"}
    ]
    
    from qwen_client import get_model_info
    model_info = get_model_info()
    
    # Now build the real messages with the correct model name in the system prompt
    messages = []
    system = get_assistant_system_prompt(model_info["display_name"])
    if context:
        try:
            system += "\n\n【当前页面上下文】\n" + json.dumps(
                context, ensure_ascii=False, indent=2
            )
        except (TypeError, ValueError):
            pass
    messages.append({"role": "system", "content": system})

    max_turns = 20
    max_len = 6000
    for m in raw_messages[-max_turns:]:
        if not isinstance(m, dict):
            continue
        role = m.get("role", "user")
        content = m.get("content", "")
        if role not in ("user", "assistant"):
            continue
        if not isinstance(content, str):
            content = str(content)
        content = content.strip()[:max_len]
        if not content:
            continue
        messages.append({"role": role, "content": content})

    if len(messages) < 2:
        return jsonify({"error": "no_user_message"}), 400

    if not get_dashscope_api_key():
        return (
            jsonify(
                {
                    "error": "missing_api_key",
                    "hint": "在项目根目录 .env 中设置 DASHSCOPE_API_KEY 或 ALIYUN_API_KEY（通义千问 / DashScope），并重启服务。",
                }
            ),
            503,
        )

    # Now make the real call with the correct system prompt
    reply, err, actual_model_info = qwen_chat(messages)
    if err:
        return jsonify({"error": "upstream", "detail": err}), 502

    response = {"reply": reply}
    if actual_model_info:
        response["model"] = actual_model_info

    return jsonify(response)


@app.route("/login", methods=["GET", "POST"])
def login():
    # 调试：打印登录请求信息
    print("=== Login route accessed ===")
    print("Method:", request.method)
    print("Current session before login:", dict(session))
    print("User-Agent:", request.headers.get('User-Agent', 'Unknown'))
    print("X-Forwarded-For:", request.headers.get('X-Forwarded-For', 'Direct'))
    print("X-Forwarded-Proto:", request.headers.get('X-Forwarded-Proto', 'http'))
    
    # 不要在GET请求时清除session，这样移动端更稳定
    # 只有明确需要重新登录时才清除
    
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")
        
        print("Login attempt with phone:", phone)
        
        # 检查是否是管理员账号（凭据仅从环境变量读取，禁止硬编码）
        ADMIN_PHONE = os.environ.get("ADMIN_PHONE")
        ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
        if ADMIN_PHONE and ADMIN_PASSWORD and phone == ADMIN_PHONE and password == ADMIN_PASSWORD:
            print("管理员登录成功")
            session["user_id"] = 0  # 用0表示管理员ID
            session["user_name"] = "Admin"
            session["user_phone"] = ADMIN_PHONE
            session["is_admin"] = True
            session.permanent = True
            response = redirect(url_for("admin_dashboard"))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            return response
        
        # 普通用户登录
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        conn.close()
        
        if user and user["password"] == hash_password(password):
            print("Login successful for user:", user["name"])
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_phone"] = user["phone"]
            session["is_admin"] = False
            session.permanent = True  # 标记session为永久
            print("Session after login:", dict(session))
            print("Session cookie SAMESITE:", app.config.get('SESSION_COOKIE_SAMESITE'))
            
            # 防止缓存问题
            response = redirect(url_for("index"))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            return response
        else:
            print("Login failed: invalid credentials")
            return render_template("login.html", error="手机号或密码错误")
    
    print("Rendering login page")
    # 添加防止缓存头
    response = make_response(render_template("login.html"))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response


# ========== 验证函数 ==========
def validate_phone_backend(phone):
    """后端手机号验证"""
    import re
    if not phone:
        return False, "手机号不能为空"
    
    phone = phone.strip()
    if len(phone) != 11:
        return False, "手机号必须为11位"
    
    if not phone.isdigit():
        return False, "手机号只能包含数字"
    
    # 号段验证
    valid_segments = (
        r'^13[4-9]', r'^15[0-2]', r'^15[7-9]', r'^18[2-4]', r'^18[7-8]', r'^198',  # 中国移动
        r'^13[0-2]', r'^15[5-6]', r'^18[5-6]', r'^17[5-6]', r'^166',  # 中国联通
        r'^133', r'^153', r'^18[0-1]', r'^189', r'^191', r'^199',  # 中国电信
        r'^17[0-1]', r'^162', r'^165', r'^167'  # 虚拟运营商
    )
    
    if not any(re.match(pattern, phone) for pattern in valid_segments):
        return False, "手机号号段无效"
    
    return True, "手机号格式正确"

def validate_id_card_backend(id_card):
    """后端身份证验证 - ISO 7064:1983 MOD 11-2"""
    import re
    import datetime
    
    if not id_card:
        return False, "身份证号不能为空"
    
    id_card = id_card.strip().upper()
    if len(id_card) != 18:
        return False, "身份证号必须为18位"
    
    # 基础格式验证
    id_regex = r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dX]$'
    if not re.match(id_regex, id_card):
        return False, "身份证格式不正确"
    
    # 验证出生日期
    try:
        birth_year = int(id_card[6:10])
        birth_month = int(id_card[10:12])
        birth_day = int(id_card[12:14])
        
        birth_date = datetime.date(birth_year, birth_month, birth_day)
        today = datetime.date.today()
        
        if birth_date > today:
            return False, "出生日期不能在未来"
        
        if (today - birth_date).days > 150 * 365:
            return False, "出生日期不合理"
            
    except ValueError:
        return False, "出生日期无效"
    
    # ISO 7064:1983 MOD 11-2 校验码计算
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    
    total_sum = 0
    for i in range(17):
        try:
            total_sum += int(id_card[i]) * coefficients[i]
        except ValueError:
            return False, "身份证格式错误"
    
    remainder = total_sum % 11
    expected_check_code = check_codes[remainder]
    actual_check_code = id_card[17]
    
    if actual_check_code != expected_check_code:
        return False, "校验码错误，请检查身份证号"
    
    return True, "身份证号验证通过"

def validate_name_backend(name):
    """后端姓名验证"""
    if not name:
        return False, "姓名不能为空"
    
    name = name.strip()
    if len(name) < 2:
        return False, "姓名至少需要2个字符"
    
    if len(name) > 30:
        return False, "姓名过长，请检查"
    
    if name.isdigit():
        return False, "姓名不能全为数字"
    
    return True, "姓名格式正确"

def validate_age_backend(age):
    """后端年龄验证"""
    if not age:
        return False, "年龄不能为空"
    
    try:
        age_num = int(age)
    except ValueError:
        return False, "年龄必须为数字"
    
    if age_num < 1 or age_num > 120:
        return False, "年龄必须在1-120岁之间"
    
    return True, "年龄格式正确"

def validate_password_backend(password):
    """后端密码验证"""
    if not password:
        return False, "密码不能为空"
    
    if len(password) < 6:
        return False, "密码至少需要6位"
    
    if len(password) > 50:
        return False, "密码过长"
    
    return True, "密码格式正确"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        id_card = request.form.get("id_card")
        phone = request.form.get("phone")
        age = request.form.get("age")
        password = request.form.get("password")
        
        # ========== 后端二次验证 ==========
        
        # 验证姓名
        name_valid, name_msg = validate_name_backend(name)
        if not name_valid:
            return render_template("register.html", error=name_msg)
        
        # 验证身份证
        id_valid, id_msg = validate_id_card_backend(id_card)
        if not id_valid:
            return render_template("register.html", error=id_msg)
        
        # 验证手机号
        phone_valid, phone_msg = validate_phone_backend(phone)
        if not phone_valid:
            return render_template("register.html", error=phone_msg)
        
        # 验证年龄
        age_valid, age_msg = validate_age_backend(age)
        if not age_valid:
            return render_template("register.html", error=age_msg)
        
        # 验证密码
        pwd_valid, pwd_msg = validate_password_backend(password)
        if not pwd_valid:
            return render_template("register.html", error=pwd_msg)
        
        # ========== 数据库验证 ==========
        conn = get_db_connection()
        
        # 检查手机号是否已存在
        existing_user = conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        if existing_user:
            conn.close()
            return render_template("register.html", error="该手机号已注册")
        
        # 检查身份证号是否已存在
        existing_id = conn.execute("SELECT * FROM users WHERE id_card = ?", (id_card,)).fetchone()
        if existing_id:
            conn.close()
            return render_template("register.html", error="该身份证号已注册")
        
        # 插入新用户
        conn.execute(
            "INSERT INTO users (name, id_card, phone, age, password) VALUES (?, ?, ?, ?, ?)",
            (name, id_card, phone, int(age), hash_password(password))
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("user_phone", None)
    session.pop("is_admin", None)
    return redirect(url_for("login"))


# 管理员验证装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or not session.get("is_admin", False):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/admin")
@admin_required
def admin_dashboard():
    """管理员后台 - 显示用户列表"""
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    
    # 获取每个用户的预测记录数
    user_stats = []
    for user in users:
        conn = get_db_connection()
        prediction_count = conn.execute("SELECT COUNT(*) FROM predictions WHERE user_id = ?", (user["id"],)).fetchone()[0]
        conn.close()
        user_stats.append({
            "id": user["id"],
            "name": user["name"],
            "phone": user["phone"],
            "age": user["age"],
            "prediction_count": prediction_count
        })
    
    return render_template("admin_dashboard.html", users=user_stats)


@app.route("/admin/user/<int:user_id>")
@admin_required
def admin_user_detail(user_id):
    """管理员 - 查看用户详情和预测记录"""
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return "用户不存在", 404
    
    predictions = conn.execute(
        "SELECT * FROM predictions WHERE user_id = ? ORDER BY prediction_date DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    
    return render_template("admin_user_detail.html", user=user, predictions=predictions)


@app.route("/api/admin/delete-user/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    """管理员 - 删除用户及其所有数据"""
    try:
        conn = get_db_connection()
        
        # 检查用户是否存在
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        
        if not user:
            conn.close()
            return jsonify({"success": False, "error": "用户不存在"}), 404
        
        # 获取用户信息用于日志
        user_name = user["name"]
        user_phone = user["phone"]
        
        # 删除该用户的所有预测记录
        conn.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
        
        # 删除用户记录
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        print(f"[Admin] 用户已删除: {user_name} (ID: {user_id}, 手机号: {user_phone})")
        
        return jsonify({
            "success": True,
            "message": f"用户 {user_name} 及其所有数据已成功删除",
            "deleted_user_id": user_id,
            "deleted_user_name": user_name
        })
        
    except Exception as e:
        print(f"[Admin] 删除用户失败: {str(e)}")
        return jsonify({"success": False, "error": f"删除失败: {str(e)}"}), 500


@app.route("/api/admin/send-email/<int:user_id>", methods=["POST"])
@admin_required
def admin_send_email(user_id):
    """管理员 - 发送邮件给用户"""
    try:
        data = request.get_json()
        subject = data.get("subject", "")
        content = data.get("content", "")
        
        if not subject or not content:
            return jsonify({"success": False, "error": "邮件主题和内容不能为空"}), 400
        
        # 获取用户信息
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        
        if not user:
            return jsonify({"success": False, "error": "用户不存在"}), 404
        
        # 检查是否有邮箱配置
        email_configured = os.environ.get('SMTP_SERVER') and os.environ.get('SMTP_USER') and os.environ.get('SMTP_PASSWORD')
        
        if not email_configured:
            return jsonify({
                "success": False, 
                "error": "邮件服务未配置。请在 .env 文件中设置 SMTP_SERVER、SMTP_USER、SMTP_PASSWORD 和 SMTP_PORT"
            }), 503
        
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = os.environ.get('SMTP_USER')
        msg['To'] = user.get('email', '') or f"{user['phone']}@placeholder.com"
        msg['Subject'] = subject
        
        # 添加HTML内容
        msg.attach(MIMEText(content, 'html', 'utf-8'))
        
        # 发送邮件
        with smtplib.SMTP(os.environ.get('SMTP_SERVER'), int(os.environ.get('SMTP_PORT', 587))) as server:
            server.starttls()
            server.login(os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASSWORD'))
            server.send_message(msg)
        
        print(f"[Admin] 邮件发送成功: 收件人={user['name']}, 主题={subject}")
        
        return jsonify({
            "success": True,
            "message": f"邮件已成功发送给 {user['name']}",
            "recipient": user['name'],
            "email_subject": subject
        })
        
    except Exception as e:
        print(f"[Admin] 发送邮件失败: {str(e)}")
        return jsonify({"success": False, "error": f"发送失败: {str(e)}"}), 500


@app.route("/api/admin/download-report/<int:user_id>", methods=["GET"])
@admin_required
def admin_download_report(user_id):
    """管理员 - 获取用户报告数据（返回JSON供前端生成HTML）"""
    
    try:
        conn = get_db_connection()
        
        # 获取用户信息
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        
        if not user:
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        # 获取所有预测记录
        predictions = conn.execute(
            """SELECT * FROM predictions 
               WHERE user_id = ? 
               ORDER BY prediction_date DESC""",
            (user_id,)
        ).fetchall()
        
        conn.close()
        
        # 统计数据
        total_predictions = len(predictions)
        benign_count = sum(1 for p in predictions if p['result'] == 'Benign')
        malignant_count = sum(1 for p in predictions if p['result'] == 'Malignant')
        
        # 转换为字典列表
        predictions_list = []
        for pred in predictions:
            predictions_list.append({
                "prediction_date": pred['prediction_date'],
                "result": pred['result'],
                "prob_benign": pred['prob_benign'],
                "prob_malignant": pred['prob_malignant'],
                "accuracy": pred['accuracy'],
                "inference_time": pred['inference_time']
            })
        
        # 返回JSON数据（与预测页面的 /report/generate 接口格式一致）
        return jsonify({
            "success": True,
            "user": {
                "id": user['id'],
                "name": user['name'],
                "phone": user['phone'],
                "age": user['age']
            },
            "predictions": predictions_list,
            "stats": {
                "total": total_predictions,
                "benign": benign_count,
                "malignant": malignant_count
            }
        })
        
    except Exception as e:
        import logging
        logging.error(f"[Admin] Failed to get report data: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to get report data"}), 500


def generate_html_report(user, predictions, stats):
    """生成HTML格式的患者报告 - 返回bytes避免编码问题"""
    
    # 使用BytesIO构建，完全避免编码问题
    import io
    
    output = io.BytesIO()
    
    # 预测记录行
    prediction_rows_parts = []
    for pred in predictions:
        result_class = b"benign" if pred['result'] == 'Benign' else b"malignant"
        result_text = b"\u826f\u6027" if pred['result'] == 'Benign' else b"\u6076\u6027"
        result_icon = b"\u2713" if pred['result'] == 'Benign' else b"\u26a0"
        
        row = b"""
        <tr>
            <td>""" + str(pred['prediction_date']).encode('utf-8') + b"""</td>
            <td class="result-""" + result_class + b"""">""" + result_icon + b""" """ + result_text + b"""</td>
            <td>""" + f"{pred['prob_benign'] * 100:.1f}%".encode('utf-8') + b"""</td>
            <td>""" + f"{pred['prob_malignant'] * 100:.1f}%".encode('utf-8') + b"""</td>
            <td>""" + f"{pred['accuracy'] * 100:.1f}%".encode('utf-8') + b"""</td>
            <td>""" + f"{pred['inference_time']:.4f}".encode('utf-8') + b"""\u79d2</td>
        </tr>
        """
        prediction_rows_parts.append(row)
    
    if not predictions:
        prediction_rows_parts = [b"""
        <tr>
            <td colspan="6" style="text-align: center; padding: 2rem; color: #666;">
                \u6682\u65e0\u9884\u6d4b\u8bb0\u5f55
            </td>
        </tr>
        """]
    
    prediction_rows = b"".join(prediction_rows_parts)
    
    # 构建完整HTML - 使用bytes
    user_name_bytes = str(user['name']).encode('utf-8')
    user_phone_bytes = str(user['phone']).encode('utf-8')
    user_age_bytes = str(user['age']).encode('utf-8')
    user_id_bytes = str(user['id']).encode('utf-8')
    
    timestamp_bytes = datetime.datetime.now().strftime('%Y\u5e74%m\u6708%d\u65e5 %H:%M:%S').encode('utf-8')
    
    total_bytes = str(stats['total']).encode('utf-8')
    benign_bytes = str(stats['benign']).encode('utf-8')
    malignant_bytes = str(stats['malignant']).encode('utf-8')
    
    html_content = b"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>\u60a3\u8005\u8bca\u65ad\u62a5\u544a - """ + user_name_bytes + b"""</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #e91e63 0%, #9c27b0 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        
        .header .subtitle {
            font-size: 1.1rem;
            opacity: 0.95;
        }
        
        .report-date {
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.85;
        }
        
        .content {
            padding: 2rem;
        }
        
        .patient-info {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            border-left: 5px solid #e91e63;
        }
        
        .patient-info h2 {
            color: #e91e63;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }
        
        .info-item {
            display: flex;
            flex-direction: column;
        }
        
        .info-label {
            font-weight: 600;
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }
        
        .info-value {
            font-size: 1.1rem;
            color: #333;
            font-weight: 500;
        }
        
        .stats-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-top: 4px solid #e91e63;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #e91e63;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.95rem;
        }
        
        .predictions-section {
            margin-top: 2rem;
        }
        
        .predictions-section h2 {
            color: #333;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #eee;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-radius: 10px;
            overflow: hidden;
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        td {
            padding: 1rem;
            border-bottom: 1px solid #eee;
            font-size: 0.95rem;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .result-benign {
            color: #4caf50;
            font-weight: 600;
        }
        
        .result-malignant {
            color: #f44336;
            font-weight: 600;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 1.5rem;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            border-top: 1px solid #eee;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
            }
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.75rem;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
            }
            
            table {
                font-size: 0.85rem;
            }
            
            th, td {
                padding: 0.75rem 0.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>&#127973; \u4e73\u817a\u764cAI\u8bca\u65ad\u62a5\u544a</h1>
            <div class="subtitle">\u4e73\u817a\u80bf\u7624\u9884\u6d4b\u6f14\u793a\u7ad9\u70b9 - \u60a3\u8005\u8be6\u7ec6\u62a5\u544a</div>
            <div class="report-date">\u62a5\u544a\u751f\u6210\u65f6\u95f4\uff1a""" + timestamp_bytes + b"""</div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Patient Info -->
            <div class="patient-info">
                <h2>&#128203; \u60a3\u8005\u57fa\u672c\u4fe1\u606f</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">\u59d3\u540d</span>
                        <span class="info-value">""" + user_name_bytes + b"""</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">\u624b\u673a\u53f7</span>
                        <span class="info-value">""" + user_phone_bytes + b"""</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">\u5e74\u9f84</span>
                        <span class="info-value">""" + user_age_bytes + b"""\u5c81</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">\u60a3\u8005ID</span>
                        <span class="info-value">#""" + user_id_bytes + b"""</span>
                    </div>
                </div>
            </div>
            
            <!-- Statistics -->
            <div class="stats-section">
                <div class="stat-card">
                    <div class="stat-value">""" + total_bytes + b"""</div>
                    <div class="stat-label">\u603b\u9884\u6d4b\u6b21\u6570</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #4caf50;">""" + benign_bytes + b"""</div>
                    <div class="stat-label">\u826f\u6027\u7ed3\u679c</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #f44336;">""" + malignant_bytes + b"""</div>
                    <div class="stat-label">\u6076\u6027\u7ed3\u679c</div>
                </div>
            </div>
            
            <!-- Predictions Table -->
            <div class="predictions-section">
                <h2>&#128202; \u9884\u6d4b\u8bb0\u5f55\u8be6\u60c5</h2>
                <table>
                    <thead>
                        <tr>
                            <th>\u9884\u6d4b\u65f6\u95f4</th>
                            <th>\u7ed3\u679c</th>
                            <th>\u826f\u6027\u6982\u7387</th>
                            <th>\u6076\u6027\u6982\u7387</th>
                            <th>\u6a21\u578b\u51c6\u786e\u7387</th>
                            <th>\u63a8\u7406\u8017\u65f6</th>
                        </tr>
                    </thead>
                    <tbody>
                        """ + prediction_rows + b"""
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>&copy; 2024 \u4e73\u817a\u764cAI\u9884\u6d4b\u5e73\u53f0 - \u672c\u62a5\u544a\u7531\u7cfb\u7edf\u81ea\u52a8\u751f\u6210\uff0c\u53ea\u4f9b\u53c2\u8003</p>
            <p style="margin-top: 0.5rem; font-size: 0.85rem;">\u6280\u672f\u652f\u6301\uff1aRandom Forest\u673a\u5668\u5b66\u4e60\u6a21\u578b | AI\u54a8\u8be2\u52a9\u624b</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content


@app.route("/test")
def test():
    return render_template("test.html")


# 多语言关怀消息缓存，避免重复生成
care_messages_cache = {}

@ app.route("/api/care-messages", methods=["GET"])
def care_messages():
    """Generate personalized care messages based on prediction outcome, supporting multiple languages."""
    if "user_id" not in session:
        return jsonify({"error": "login_required"}), 401
    
    outcome = request.args.get("outcome", "").strip()
    if outcome not in ["Benign", "Malignant"]:
        return jsonify({"error": "invalid_outcome"}), 400
    
    if not get_dashscope_api_key():
        return (
            jsonify(
                {
                    "error": "missing_api_key",
                    "hint": "在项目根目录 .env 中设置 DASHSCOPE_API_KEY 或 ALIYUN_API_KEY（通义千问 / DashScope），并重启服务。",
                }
            ),
            503,
        )
    
    # 不使用缓存，每次都生成新内容
    cache_key = f"{outcome}_fresh"
    if cache_key in care_messages_cache:
        care_messages_cache.pop(cache_key, None)
    
    if outcome == "Benign":
        emotional_tone = """
        【情感基调：温暖、舒缓、安心】
        - 传递积极信号，强调结果令人欣慰
        - 鼓励继续保持健康生活方式
        - 提醒定期体检的重要性
        - 表达祝贺与希望
        - 可引用健康、阳光、自然相关的意象
        - 语言风格：轻松、温柔、令人放松
        """
        cultural_themes_zh = '可融入中国传统文化元素如"春风"、"暖阳"、"福气"等意象'
        cultural_themes_en = '可引用西方文化中的"spring morning"、"gentle breeze"、"new beginning"等意象'
        cultural_themes_fr = '可融入法国文化中的"brise légère"、"lumière douce"、"printemps"等意象'
        cultural_themes_ru = '可引用俄罗斯文化中的"мягкий свет"（柔和光芒）、"тёплый ветер"（暖风）等意象'
        cultural_themes_es = '可融入西班牙文化中的"brisa suave"、"luz dorada"、"nueva vida"等意象'
    else:
        emotional_tone = """
        【情感基调：坚定、勇敢、鼓舞】
        - 承认挑战的存在，但强调希望与勇气
        - 传递力量感，表达与患者同在
        - 鼓励积极面对治疗
        - 强调现代医学的进步和康复可能性
        - 可引用坚韧、重生、光明相关的意象
        - 语言风格：坚定、有力、温暖而不软弱
        """
        cultural_themes_zh = '可融入中国传统文化中 "梅花香自苦寒来"、"松柏经霜愈坚"、"破茧成蝶"、"向阳而生" 的意象；引用 "勇士出征"、"与病魔掰手腕" 的战士精神；结合 "正气存内，邪不可干" 的生命智慧，传递 "熬过寒冬，必有春暖花开" 的信念'
        cultural_themes_en = '可引用西方文化中 "phoenix rising from ashes（凤凰涅槃）"、"lighthouse in the storm（风暴中的灯塔）"、"warrior spirit（战士精神）"、"light that outlasts darkness（穿透黑暗的光）" 的意象；强调 "you are stronger than you know（你比自己想象的更强大）"、"every step is a victory（每一步都是胜利）"，传递 "we walk this path with you（我们与你同行）" 的陪伴感'
        cultural_themes_fr = '可融入法国文化中 "iris de l’espoir（希望之鸢尾）"、"force intérieure qui ne se brise pas（不可摧折的内在力量）"、"lumière qui persiste dans lombre（阴影中不灭的光）" 的意象；结合 "solidarité（团结陪伴）" 的文化内核，传递 "jour après jour, la vie reprend ses droits（日复一日，生命终将夺回主动权）" 的信念'
        cultural_themes_ru = '可引用俄罗斯文化中 "берёза, которая гнётся, но не ломается（弯而不折的白桦树）"、"внутренняя сила, которая побеждает всё（战胜一切的内在力量）"、"весна после долгой зимы（漫长寒冬后的春天）" 的意象；强调 "мы с тобой до конца（我们与你并肩到底）"，传递 "мужество рождается в борьбе（勇气在战斗中诞生）" 的力量'
        cultural_themes_es = '可融入西班牙文化中 "girasol que sigue al sol（追随太阳的向日葵）"、"fuerza que florece en la adversidad（逆境中绽放的力量）"、"luz que nunca se apaga（永不熄灭的光）" 的意象；结合 "familia y amigos son tu fortaleza（家人朋友是你的铠甲）" 的文化理念，传递 "cada día es una nueva oportunidad para sanar（每一天都是治愈的新机会）" 的希望'
    
    import time
    timestamp = int(time.time())
    
    prompt = f"""你是【{outcome}】预测结果患者的关怀顾问。请为以下5种语言各生成1条独特的、原创的关怀消息。

【核心要求】
1. 每条消息必须是该语言文化的原创内容，而非简单翻译
2. 每条消息必须体现对应语言国家的文化特色和情感表达方式
3. 每次生成必须产生完全不同的内容（使用时间戳确保随机性：{timestamp}）
4. 消息长度：2-4句话，简洁但具有人文关怀

【情感基调】
{emotional_tone}

【各国文化特色要求】
- 中文（zh）：{cultural_themes_zh}。使用中文特有的温暖表达方式。
- 英文（en）：{cultural_themes_en}。使用英语国家常见的鼓励表达方式。
- 法文（fr）：{cultural_themes_fr}。使用法语特有的优雅、浪漫的表达方式。
- 俄文（ru）：{cultural_themes_ru}。使用俄语特有的深沉、有力的表达方式。
- 西班牙文（es）：{cultural_themes_es}。使用西班牙语特有的热情、温暖的表达方式。

【专业边界】
- 仅提供情感支持和适度鼓励
- 不提供具体医疗建议
- 提醒患者遵循医生建议

【输出格式 - 仅JSON，无其他内容】
{{
  "zh": "中文消息内容（体现中国文化特色）",
  "en": "English message content (reflecting Western cultural characteristics)",
  "fr": "Message en français (avec des expressions françaises authentiques)",
  "ru": "Сообщение на русском языке (с культурными особенностями России)",
  "es": "Mensaje en español (con características culturales españolas)"
}}

【质量标准】
- 每条消息必须独特，不可相似
- 必须符合对应语言的文化表达习惯
- 情感真挚，不虚伪不做作
- 禁止使用机器翻译腔"""

    messages = [
        {"role": "system", "content": "You are a creative, culturally-aware compassionate care advisor. Generate unique, original messages for EACH language that reflect that culture's authentic expressions. Never translate - always create original content. Output ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ]
    
    reply, err, model_info = qwen_chat(messages)
    if err:
        return jsonify({"error": "upstream", "detail": err}), 502
    
    print(f'=== 关怀消息调试信息 ===')
    print(f'模型返回原始回复: {reply}')
    print(f'模型返回类型: {type(reply)}')
    print(f'模型信息: {model_info}')
    
    try:
        messages_dict = reply
        
        # 检查是否是字符串，如果是则尝试解析
        if isinstance(messages_dict, str):
            print(f'尝试解析字符串为JSON...')
            messages_dict = json.loads(messages_dict)
        
        print(f'解析后: {messages_dict}, 类型: {type(messages_dict)}')
        
        # 验证是否是正确的格式
        if isinstance(messages_dict, dict) and all(k in messages_dict for k in ['zh', 'en', 'fr', 'ru', 'es']):
            print(f'验证成功：找到5条消息')
            return jsonify({'messages': messages_dict})
        else:
            print(f'验证失败：格式不正确，尝试提取JSON...')
            # 尝试从原始回复中提取 JSON
            reply_str = str(reply)
            import re
            json_match = re.search(r'\{[\s\S]*\}', reply_str)
            if json_match:
                try:
                    messages_dict = json.loads(json_match.group())
                    if isinstance(messages_dict, dict) and all(k in messages_dict for k in ['zh', 'en', 'fr', 'ru', 'es']):
                        print(f'从文本中提取JSON成功')
                        return jsonify({'messages': messages_dict})
                except Exception as e2:
                    print(f'提取JSON失败: {e2}')
            # 即使格式不对，也要返回我们能提取的内容
            print(f'返回默认格式')
            return jsonify({'messages': {'en': str(reply)[:500]}})
    except (TypeError, ValueError, json.JSONDecodeError) as e:
        print(f'解析关怀消息失败: {e}, 原始回复: {reply}')
        # 尝试提取 JSON 内容（如果被包裹在其他文本中）
        import re
        json_match = re.search(r'\{[\s\S]*\}', str(reply))
        if json_match:
            try:
                messages_dict = json.loads(json_match.group())
                if isinstance(messages_dict, dict) and all(k in messages_dict for k in ['zh', 'en', 'fr', 'ru', 'es']):
                    return jsonify({'messages': messages_dict})
            except Exception as e2:
                print(f'二次提取JSON失败: {e2}')
        return jsonify({'messages': {'en': str(reply)[:500]}})


@app.route("/report/generate", methods=["POST"])
def generate_report():
    """生成报告"""
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # 获取报告数据
    output = request.form.get("output")
    prob_benign = float(request.form.get("prob_benign", 0))
    prob_malignant = float(request.form.get("prob_malignant", 0))
    accuracy = float(request.form.get("accuracy", 0))
    time = float(request.form.get("time", 0))
    
    # 生成报告内容
    report_content = f"""Breast Cancer Prediction Report

Patient Information:
Name: {session.get('user_name', 'N/A')}
Phone: {session.get('user_phone', 'N/A')}

Prediction Result:
Tumor Type: {output}
Probability (Benign): {prob_benign * 100:.2f}%
Probability (Malignant): {prob_malignant * 100:.2f}%

Model Information:
Accuracy: {accuracy * 100:.2f}%
Inference Time: {time:.4f} seconds

Important Note:
This prediction is based on a machine learning model and should not be considered a definitive medical diagnosis. Always consult with a qualified healthcare professional for proper medical advice.
"""
    
    return jsonify({
        "content": report_content,
        "user_name": session.get('user_name', 'N/A'),
        "user_phone": session.get('user_phone', 'N/A'),
        "output": output,
        "prob_benign": prob_benign,
        "prob_malignant": prob_malignant,
        "accuracy": accuracy,
        "time": time
    })


if __name__ == "__main__":
    ensure_clf()
    app.run(debug=True)
