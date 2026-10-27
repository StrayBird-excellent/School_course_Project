# 乳腺癌预测系统 / Breast Cancer Prediction

> 学校课程项目（School_course_Project）——基于机器学习与深度学习的乳腺肿瘤良/恶性预测 Web 应用。

本系统使用经典的 Wisconsin 乳腺诊断数据集（30 维数值特征），通过随机森林（Random Forest）模型预测乳腺肿瘤为 **良性（Benign）** 或 **恶性（Malignant）**，并提供带多语言医学咨询助手的 Web 界面。

## 功能特性

- 随机森林模型预测（训练、预测、概率输出、准确率评估）
- 用户注册 / 登录（手机号 + 身份证 + 密码，后端校验）
- 预测记录存储与可视化
- 管理员后台（用户管理、报告导出、邮件通知）
- AI 医学咨询助手（优先调用本地大模型，自动降级到通义千问 / DashScope）
- 多语言关怀消息生成（中 / 英 / 法 / 俄 / 西）
- 响应式 UI（Bootstrap）

## 技术栈

- **后端**：Python 3, Flask
- **机器学习**：scikit-learn（RandomForestClassifier）, NumPy, pandas
- **大模型**：本地 OpenAI 兼容接口（如 Ollama） / 阿里云通义千问 DashScope
- **前端**：HTML / CSS / JavaScript / Bootstrap
- **数据库**：SQLite（用户与预测记录）

## 项目结构

```
app.py                  # Flask 主应用（路由、鉴权、管理后台、AI 助手）
config.py               # 应用配置（密钥 / 数据库 / 安全）
qwen_client.py          # 大模型调用（本地优先，降级通义千问）
implementation.py       # 随机森林训练 / 预测逻辑
random_forest.py        # 随机森林建模示例
create_db.py            # 初始化 SQLite 数据库
start.py                # 启动脚本（开发 / 生产环境）
requirements.txt        # 依赖
Breast Cancer Data.csv  # 训练数据（Wisconsin 诊断数据集，公开数据，无个人身份信息）
templates/              # HTML 模板
static/                 # 前端静态资源（CSS / JS / 图片）
```

> 注意：训练用图像数据集 `BCP_Image_Dataset/`、音乐等二进制资源因体积与授权原因 **未纳入本仓库**，请从课程资源另行获取；Web 应用的预测功能依赖 `Breast Cancer Data.csv`，已随仓库提供。

## 快速开始

1. 克隆仓库并进入目录：

   ```bash
   git clone https://github.com/StrayBird-excellent/School_course_Project.git
   cd School_course_Project
   ```

2. 创建并激活虚拟环境，安装依赖：

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 配置环境变量：复制 `.env.example` 为 `.env` 并填写：

   ```bash
   cp .env.example .env
   ```

   关键变量：
   - `DASHSCOPE_API_KEY`（或 `ALIYUN_API_KEY`）：通义千问 API Key（AI 助手需要）
   - `SECRET_KEY`：Flask 会话密钥（生产环境务必使用强随机值）
   - `ADMIN_PHONE` / `ADMIN_PASSWORD`：管理员账号（不配置则管理员登录关闭）

4. 初始化数据库并启动：

   ```bash
   python create_db.py
   python app.py
   ```

   应用默认运行在 `http://127.0.0.1:5000`。

## 免责声明

本系统仅用于 **教学与演示**，预测结果基于机器学习模型，不构成任何医学诊断或治疗建议。如有健康问题，请咨询专业医疗机构与医生。

## 许可证

本项目以 GNU General Public License v3.0 发布，详见 [LICENSE](LICENSE)。
