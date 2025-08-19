#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuirkLog 每周定时任务
设置为每周一上午10点执行，总结上一周的内容
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
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
        """从settings.xml文件加载AI相关设置和保存路径"""
        try:
            xml_file = Path('settings.xml')
            if not xml_file.exists():
                return {}
            
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            settings = {}
            
            # 读取文件设置（保存路径）
            general_section = root.find('general')
            if general_section is not None:
                save_dir_elem = general_section.find('saveDirectory')
                if save_dir_elem is not None and save_dir_elem.text:
                    settings['saveDirectory'] = save_dir_elem.text
            
            # 读取导出设置（文件命名）
            export_section = root.find('export')
            if export_section is not None:
                file_naming_elem = export_section.find('fileNaming')
                if file_naming_elem is not None and file_naming_elem.text:
                    settings['fileNaming'] = file_naming_elem.text
            
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
            print(f"加载设置失败: {e}")
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
            print("🤖 开始执行API请求...")
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
            print("✅ API请求成功")
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
    
    def get_last_week_date_range(self):
        """获取上一周的日期范围 (周一到周日)"""
        today = datetime.now()
        # 计算上周一
        last_monday = today - timedelta(days=today.weekday() + 7)
        # 计算上周日
        last_sunday = last_monday + timedelta(days=6)
        return last_monday, last_sunday
    
    def get_possible_filenames(self, date_str, settings):
        """根据设置生成可能的文件名格式"""
        possible_files = []
        
        # 从设置中获取文件命名格式
        file_naming = settings.get('fileNaming', '每日记录_{date}')
        
        # 根据文件命名模板生成文件名
        if '{date}' in file_naming:
            formatted_name = file_naming.replace('{date}', date_str)
            possible_files.append(f"{formatted_name}.json")
        
        # 添加系统支持的标准格式
        standard_formats = [
            '每日记录_{date}',
            'daily_record_{date}', 
            '{date}_记录'
        ]
        
        for format_template in standard_formats:
            if format_template != file_naming:  # 避免重复
                formatted_name = format_template.replace('{date}', date_str)
                possible_files.append(f"{formatted_name}.json")
        
        # 添加兼容性格式（localStorage中使用的格式）
        possible_files.extend([
            f"daily-record-{date_str}.json",
            f"{date_str}.json"
        ])
        
        return possible_files
    
    def load_daily_data(self, date, data_directory):
        """加载指定日期的每日数据"""
        date_str = date.strftime('%Y-%m-%d')
        settings = self.load_settings_from_xml()
        
        # 获取所有可能的文件名
        possible_files = self.get_possible_filenames(date_str, settings)
        
        for filename in possible_files:
            file_path = Path(data_directory) / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f"✅ 找到数据文件: {filename}")
                        return json.load(f)
                except Exception as e:
                    print(f"⚠️ 读取文件 {filename} 失败: {e}")
                    continue
                    
        return {}
    
    def collect_last_week_data(self):
        """收集上一周的数据"""
        # 获取设置
        settings = self.load_settings_from_xml()
        data_directory = settings.get('saveDirectory', './downloads')
        
        # 获取上一周日期范围
        start_date, end_date = self.get_last_week_date_range()
        
        print(f"📊 正在收集上一周数据 ({start_date.strftime('%Y-%m-%d')} 至 "
              f"{end_date.strftime('%Y-%m-%d')})...")
        
        # 加载一周数据
        weekly_data = []
        current_date = start_date
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        while current_date <= end_date:
            daily_data = self.load_daily_data(current_date, data_directory)
            daily_data['date'] = current_date.strftime('%Y-%m-%d')
            daily_data['weekday_cn'] = weekdays[current_date.weekday()]
            weekly_data.append(daily_data)
            current_date += timedelta(days=1)
        
        # 统计有效数据天数
        valid_days = len([d for d in weekly_data if d.get('plans')])
        print(f"✅ 找到 {valid_days} 天的有效数据")
        
        return self.format_data_for_ai(weekly_data, start_date, end_date)
    
    def format_data_for_ai(self, weekly_data, start_date, end_date):
        """将一周数据格式化为适合AI分析的文本"""
        
        formatted_text = f"""# 每周数据汇总 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})

## 本周每日详细数据

"""
        
        for i, daily_data in enumerate(weekly_data):
            date = daily_data.get('date', '未知日期')
            weekday = daily_data.get('weekday_cn', '未知')
            
            formatted_text += f"### {weekday} {date}\n\n"
            
            # 计划数据
            plans = daily_data.get('plans', [])
            if plans:
                formatted_text += "#### 📋 今日计划\n"
                for j, plan in enumerate(plans, 1):
                    status = "✅已完成" if plan.get('completed', False) else "❌未完成"
                    importance = plan.get('importance', '未设置')
                    urgency = plan.get('urgency', '未设置')
                    start_time = plan.get('startTime', plan.get('start_time', '未设置'))
                    duration = plan.get('duration', '未设置')
                    
                    formatted_text += f"{j}. **{plan.get('event', '未知事件')}** {status}\n"
                    formatted_text += f"   - 重要等级: {importance}\n"
                    formatted_text += f"   - 紧急程度: {urgency}\n"
                    formatted_text += f"   - 开始时间: {start_time}\n"
                    formatted_text += f"   - 计划时长: {duration}\n\n"
                
                # 统计信息
                total_plans = len(plans)
                completed_plans = sum(1 for plan in plans if plan.get('completed', False))
                completion_rate = (completed_plans / total_plans * 100) if total_plans > 0 else 0
                
                formatted_text += f"**当日统计**: {completed_plans}/{total_plans} 项完成，完成率 {completion_rate:.1f}%\n\n"
            else:
                formatted_text += "#### 📋 今日计划\n当日无计划记录\n\n"
            
            # 反思数据
            reflection = daily_data.get('reflection', {})
            
            # 进步之处
            progress_items = reflection.get('progress', [])
            if progress_items:
                formatted_text += "#### 👍 今日进步\n"
                for item in progress_items:
                    if item.strip():
                        formatted_text += f"- {item.strip()}\n"
                formatted_text += "\n"
            
            # 改进建议
            improvement_items = reflection.get('improvements', [])
            if improvement_items:
                formatted_text += "#### 😊 改进之处\n"
                for item in improvement_items:
                    if item.strip():
                        formatted_text += f"- {item.strip()}\n"
                formatted_text += "\n"
            
            # 感恩时刻
            gratitude_items = reflection.get('gratitude', [])
            if gratitude_items:
                formatted_text += "#### ❤️ 感恩时刻\n"
                for item in gratitude_items:
                    if item.strip():
                        formatted_text += f"- {item.strip()}\n"
                formatted_text += "\n"
            
            # 每日思考
            daily_thoughts = reflection.get('dailyThoughts', '').strip()
            if daily_thoughts:
                formatted_text += "#### 💭 每日思考\n"
                formatted_text += f"{daily_thoughts}\n\n"
            
            formatted_text += "---\n\n"
        
        # 周汇总统计
        total_plans = sum(len(daily.get('plans', [])) for daily in weekly_data)
        total_completed = sum(sum(1 for plan in daily.get('plans', []) 
                                if plan.get('completed', False)) 
                            for daily in weekly_data)
        overall_completion = (total_completed / total_plans * 100) if total_plans > 0 else 0
        
        formatted_text += f"""## 📊 本周整体统计

- **总计划数**: {total_plans} 项
- **已完成**: {total_completed} 项  
- **整体完成率**: {overall_completion:.1f}%
- **有数据天数**: {len([d for d in weekly_data if d.get('plans')])} 天

---

"""
        return formatted_text
    
    def load_template(self):
        """加载周总结模板"""
        try:
            template_path = Path("weekly_summary_template.md")
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                print("⚠️ 未找到 weekly_summary_template.md 文件，使用默认模板")
                return self.get_default_template()
        except Exception as e:
            print(f"❌ 加载模板失败: {e}")
            return self.get_default_template()
    
    def get_default_template(self):
        """获取默认模板"""
        return """
你是一位专业的个人效率教练和生活导师，擅长分析个人成长数据，提供深度洞察和实用建议。

## 任务说明
基于用户提供的一周每日计划和反思数据，生成一份深度、温暖、实用的每周总结报告。

请分析以下数据并生成个性化的周总结报告：
- 统计分析完成情况和趋势
- 识别成长轨迹和问题模式  
- 提供温暖鼓励的改进建议
- 给出下周的具体优化建议

请用温暖鼓励的语调，提供有深度的洞察和实用的建议。
"""
    
    def weekly_task(self):
        """每周执行的任务 - 总结上一周的内容"""
        print("=" * 50)
        print(f"🌟 执行每周总结任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        try:
            # 1. 收集上一周的数据
            weekly_data = self.collect_last_week_data()
            
            if not weekly_data.strip():
                print("❌ 未找到上一周的有效数据，跳过总结")
                return
            
            # 2. 加载模板
            template = self.load_template()
            
            # 3. 构建完整的提示词
            prompt = template + "\n\n" + weekly_data + "\n\n请基于以上数据和要求，生成个性化的每周总结报告。"
            
            # 4. 执行API请求
            response = self.make_api_request(prompt)
            
            if response:
                print("🎯 AI生成的每周总结:")
                print("-" * 30)
                print(response)
                print("-" * 30)
                
                # 5. 保存总结报告
                self.save_weekly_insights(response)
            else:
                print("❌ 未能获取每周总结")
                
        except Exception as e:
            print(f"❌ 执行每周任务失败: {e}")
        
        print("✅ 每周总结任务执行完成")
    
    def setup_schedule(self):
        """设置定时任务计划"""
        # 清除现有计划
        schedule.clear()
        
        # 设置每周一上午10点执行（总结上一周）
        schedule.every().monday.at("10:00").do(self.weekly_task)
        
        print("⏰ 定时任务已设置:")
        print("   - 每周一 10:00 (总结上一周)")
        
    def run_scheduler(self):
        """运行定时任务调度器"""
        print("🚀 每周总结定时任务调度器已启动...")
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
        self.task_thread = threading.Thread(
            target=self.run_scheduler, daemon=True)
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
