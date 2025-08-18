# QuirkLog 定时任务配置文件
# 请将此文件重命名为 config.py 并填入您的配置信息

# OpenRouter API 配置
OPENROUTER_API_KEY = "your_api_key_here"  # 请替换为您的实际API密钥
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# 网站信息（用于OpenRouter统计）
SITE_URL = "https://quirklog.app"
SITE_NAME = "QuirkLog Daily Planner"

# AI模型配置
AI_MODEL = "deepseek/deepseek-r1-0528-qwen3-8b:free"

# 定时任务配置
SCHEDULE_CONFIG = {
    "saturday": "09:00",  # 每周六上午9点
    "sunday": "19:00",    # 每周日晚上7点
}

# 数据保存配置
DATA_DIR = "weekly_insights"  # 每周洞察保存目录
