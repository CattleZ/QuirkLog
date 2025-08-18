#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 每周定时任务
设置为每周末执行OpenRouter API请求
"""

import schedule
import time
import threading
from datetime import datetime
from openai import OpenAI
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path


class WeeklyTaskManager:
    """每周定时任务管理器"""
    
    def __init__(self, api_key=None, base_url=None, model=None):
        """
        初始化定时任务管理器
        
        Args:
            api_key: OpenRouter API密钥 (优先级: 参数 > settings.xml > 环境变量)
            base_url: API基础URL (优先级: 参数 > settings.xml > 默认值)
            model: AI模型名称 (优先级: 参数 > settings.xml > 默认值)
        """
        # 加载设置
        settings = self.load_settings_from_xml()
        
        # 按优先级设置API密钥
        self.api_key = (
            api_key or 
            settings.get('openrouterApiKey') or 
            os.getenv('OPENROUTER_API_KEY')
        )
        
        # 按优先级设置base_url
        self.base_url = (
            base_url or 
            settings.get('openrouterBaseUrl') or 
            "https://openrouter.ai/api/v1"
        )
        
        # 按优先级设置model
        self.model = (
            model or 
            settings.get('openrouterModel') or 
            "deepseek/deepseek-r1-0528-qwen3-8b:free"
        )
        
        self.client = None
        self.running = False
        self.task_thread = None
        
        # 初始化OpenAI客户端
        if self.api_key:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        else:
            print("⚠️ 警告: 未找到OpenRouter API密钥")
    
    def load_settings_from_xml(self):
        """从settings.xml文件加载AI相关设置"""
        try:
            xml_file = Path('settings.xml')
            if not xml_file.exists():
                return {}
            
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            settings = {}
            
            # 读取AI设置
            ai_section = root.find('ai')
            if ai_section is not None:
                api_key_elem = ai_section.find('openrouterApiKey')
                if api_key_elem is not None and api_key_elem.text:
                    settings['openrouterApiKey'] = api_key_elem.text
                
                base_url_elem = ai_section.find('openrouterBaseUrl')
                if base_url_elem is not None and base_url_elem.text:
                    settings['openrouterBaseUrl'] = base_url_elem.text
                
                model_elem = ai_section.find('openrouterModel')
                if model_elem is not None and model_elem.text:
                    settings['openrouterModel'] = model_elem.text
                
                enabled_elem = ai_section.find('enabled')
                if enabled_elem is not None:
                    settings['aiEnabled'] = enabled_elem.text.lower() == 'true'
            
            return settings
            
        except Exception as e:
            print(f"加载AI设置失败: {e}")
            return {}
    
    def make_api_request(self, prompt="生成一段关于每周总结和下周计划的建议"):
        """
        执行OpenRouter API请求
        
        Args:
            prompt: 发送给AI的提示词
            
        Returns:
            str: AI的回复内容
        """
        if not self.client:
            print("❌ OpenAI客户端未初始化，无法执行API请求")
            return None
        
        try:
            print(f"🤖 开始执行API请求...")
            print(f"📝 提示词: {prompt}")
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://quirklog.app",  # 您的网站URL
                    "X-Title": "QuirkLog Daily Planner",     # 您的网站标题
                },
                extra_body={},
                model=self.model,  # 使用配置的模型
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_content = completion.choices[0].message.content
            print(f"✅ API请求成功")
            return response_content
            
        except Exception as e:
            print(f"❌ API请求失败: {e}")
            return None
    
    def save_weekly_insights(self, content):
        """
        保存每周洞察到文件
        
        Args:
            content: AI生成的内容
        """
        if not content:
            return
        
        try:
            # 创建每周洞察目录
            insights_dir = Path("weekly_insights")
            insights_dir.mkdir(exist_ok=True)
            
            # 生成文件名
            now = datetime.now()
            filename = f"weekly_insight_{now.strftime('%Y-%m-%d')}.json"
            file_path = insights_dir / filename
            
            # 构建保存数据
            insight_data = {
                "date": now.strftime('%Y-%m-%d'),
                "timestamp": now.isoformat(),
                "week_number": now.isocalendar()[1],
                "year": now.year,
                "content": content,
                "source": "OpenRouter AI",
                "model": self.model  # 使用配置的模型
            }
            
            # 保存到JSON文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(insight_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 每周洞察已保存到: {file_path}")
            
        except Exception as e:
            print(f"❌ 保存每周洞察失败: {e}")
    
    def weekly_task(self):
        """每周执行的任务"""
        print("=" * 50)
        print(f"🌟 执行每周定时任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # 生成针对每周总结的提示词
        current_date = datetime.now()
        week_number = current_date.isocalendar()[1]
        
        prompt = f"""
作为一个个人效率提升顾问，请为用户生成本周({current_date.strftime('%Y年第%W周')})的总结建议和下周计划指导。

请包含以下几个方面：
1. 每周回顾的重要性
2. 3-5个自我反思问题
3. 下周目标设定的建议
4. 时间管理技巧
5. 保持动力的方法

请用中文回答，语言要温暖、鼓励性，适合个人成长和自我提升场景。
        """.strip()
        
        # 执行API请求
        response = self.make_api_request(prompt)
        
        if response:
            print("🎯 AI生成的每周洞察:")
            print("-" * 30)
            print(response)
            print("-" * 30)
            
            # 保存洞察
            self.save_weekly_insights(response)
        else:
            print("❌ 未能获取每周洞察")
        
        print("✅ 每周定时任务执行完成")
    
    def setup_schedule(self):
        """设置定时任务计划"""
        # 清除现有计划
        schedule.clear()
        
        # 设置每周六上午9点执行
        schedule.every().saturday.at("09:00").do(self.weekly_task)
        
        # 设置每周日晚上7点执行（额外的周末任务）
        schedule.every().sunday.at("19:00").do(self.weekly_task)
        
        print("⏰ 定时任务已设置:")
        print("   - 每周六 09:00")
        print("   - 每周日 19:00")
    
    def run_scheduler(self):
        """运行定时任务调度器"""
        print("🚀 定时任务调度器已启动...")
        self.running = True
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def start(self):
        """启动定时任务"""
        if self.running:
            print("⚠️ 定时任务已在运行中")
            return
        
        # 设置定时计划
        self.setup_schedule()
        
        # 在后台线程中运行调度器
        self.task_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.task_thread.start()
        
        print("✅ 定时任务已启动")
    
    def stop(self):
        """停止定时任务"""
        self.running = False
        if self.task_thread:
            self.task_thread.join(timeout=5)
        
        print("🛑 定时任务已停止")
    
    def run_task_now(self):
        """立即执行一次任务（用于测试）"""
        print("🧪 立即执行任务（测试模式）")
        self.weekly_task()
    
    def list_scheduled_jobs(self):
        """列出所有计划的任务"""
        print("📅 已计划的任务:")
        for job in schedule.jobs:
            print(f"   - {job}")


def main():
    """主函数"""
    print("🌟 QuirkLog 每周定时任务管理器")
    print("=" * 40)
    
    # 从环境变量或配置文件读取API密钥
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("⚠️ 请设置环境变量 OPENROUTER_API_KEY 或在代码中配置API密钥")
        api_key = input("请输入您的OpenRouter API密钥 (或按Enter跳过): ").strip()
        
        if api_key:
            os.environ['OPENROUTER_API_KEY'] = api_key
    
    # 创建任务管理器
    task_manager = WeeklyTaskManager(api_key=api_key)
    
    try:
        while True:
            print("\n" + "=" * 40)
            print("选择操作:")
            print("1. 启动定时任务")
            print("2. 停止定时任务")
            print("3. 立即执行任务（测试）")
            print("4. 查看计划任务")
            print("5. 退出")
            print("=" * 40)
            
            choice = input("请选择 (1-5): ").strip()
            
            if choice == '1':
                task_manager.start()
            elif choice == '2':
                task_manager.stop()
            elif choice == '3':
                task_manager.run_task_now()
            elif choice == '4':
                task_manager.list_scheduled_jobs()
            elif choice == '5':
                task_manager.stop()
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重试")
    
    except KeyboardInterrupt:
        task_manager.stop()
        print("\n👋 程序已退出")


if __name__ == "__main__":
    main()
