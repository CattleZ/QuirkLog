#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日计划与总结表单应用程序 - 命令行版本
适用于没有GUI环境的情况
"""

import json
import os
from datetime import datetime

class DailyPlannerCLI:
    def __init__(self):
        self.plans = []
        self.data_file = "daily_data.json"
        self.load_data()
        
    def display_menu(self):
        today = datetime.now().strftime("%Y年%m月%d日 (%A)")
        print("\n" + "="*50)
        print(f"🌞 {today} 计划与总结")
        print("="*50)
        print("1. 📝 添加新计划")
        print("2. 📋 查看所有计划")
        print("3. ✅ 标记计划完成")
        print("4. 🗑️  删除计划")
        print("5. 📊 查看完成情况")
        print("6. 🤔 今日总结反思")
        print("7. 💾 保存数据")
        print("8. 🔄 重新加载数据")
        print("0. 🚪 退出程序")
        print("="*50)
        
    def add_plan(self):
        print("\n📝 添加新计划")
        print("-" * 30)
        
        event = input("计划事件: ").strip()
        if not event:
            print("❌ 计划事件不能为空！")
            return
            
        print("\n重要等级选择:")
        print("1. 十分重要")
        print("2. 重要") 
        print("3. 一般重要")
        print("4. 不重要")
        
        importance_choice = input("请选择重要等级 (1-4) [默认2]: ").strip() or "2"
        importance_map = {
            "1": "十分重要",
            "2": "重要",
            "3": "一般重要", 
            "4": "不重要"
        }
        importance = importance_map.get(importance_choice, "重要")
        
        print("\n紧急程度选择:")
        print("1. 十分紧急")
        print("2. 紧急")
        print("3. 不紧急")
        
        urgency_choice = input("请选择紧急程度 (1-3) [默认2]: ").strip() or "2"
        urgency_map = {
            "1": "十分紧急",
            "2": "紧急", 
            "3": "不紧急"
        }
        urgency = urgency_map.get(urgency_choice, "紧急")
        
        start_time = input("开始时间 [默认7:00]: ").strip() or "7:00"
        duration = input("计划时长 [默认1小时]: ").strip() or "1小时"
        
        plan = {
            "id": len(self.plans) + 1,
            "event": event,
            "importance": importance,
            "urgency": urgency,
            "start_time": start_time,
            "duration": duration,
            "completed": False,
            "timestamp": datetime.now().isoformat()
        }
        
        self.plans.append(plan)
        print(f"\n✅ 计划 '{event}' 已添加成功！")
        
    def view_plans(self):
        if not self.plans:
            print("\n📋 暂无计划")
            return
            
        print("\n📋 今日计划列表")
        print("-" * 80)
        print(f"{'ID':<3} {'计划事件':<20} {'重要等级':<10} {'紧急程度':<10} {'开始时间':<8} {'时长':<8} {'状态':<8}")
        print("-" * 80)
        
        for plan in self.plans:
            status = "✅完成" if plan["completed"] else "⏳进行中"
            print(f"{plan['id']:<3} {plan['event'][:18]:<20} {plan['importance']:<10} "
                  f"{plan['urgency']:<10} {plan['start_time']:<8} {plan['duration']:<8} {status:<8}")
        
    def mark_completed(self):
        if not self.plans:
            print("\n❌ 暂无计划可标记")
            return
            
        self.view_plans()
        try:
            plan_id = int(input("\n请输入要标记完成的计划ID: "))
            plan = next((p for p in self.plans if p["id"] == plan_id), None)
            
            if plan:
                if plan["completed"]:
                    print(f"✅ 计划 '{plan['event']}' 已经完成了！")
                else:
                    plan["completed"] = True
                    print(f"✅ 计划 '{plan['event']}' 已标记为完成！")
            else:
                print("❌ 找不到指定ID的计划")
        except ValueError:
            print("❌ 请输入有效的数字ID")
            
    def delete_plan(self):
        if not self.plans:
            print("\n❌ 暂无计划可删除")
            return
            
        self.view_plans()
        try:
            plan_id = int(input("\n请输入要删除的计划ID: "))
            plan = next((p for p in self.plans if p["id"] == plan_id), None)
            
            if plan:
                confirm = input(f"确定要删除计划 '{plan['event']}' 吗？(y/N): ").strip().lower()
                if confirm == 'y':
                    self.plans.remove(plan)
                    print(f"🗑️ 计划 '{plan['event']}' 已删除")
                else:
                    print("🚫 删除操作已取消")
            else:
                print("❌ 找不到指定ID的计划")
        except ValueError:
            print("❌ 请输入有效的数字ID")
            
    def view_completion_status(self):
        if not self.plans:
            print("\n📊 暂无计划统计")
            return
            
        completed_plans = [p for p in self.plans if p["completed"]]
        uncompleted_plans = [p for p in self.plans if not p["completed"]]
        
        total = len(self.plans)
        completed_count = len(completed_plans)
        completion_rate = (completed_count / total * 100) if total > 0 else 0
        
        print("\n📊 计划完成情况统计")
        print("-" * 40)
        print(f"总计划数: {total}")
        print(f"已完成: {completed_count}")
        print(f"未完成: {len(uncompleted_plans)}")
        print(f"完成率: {completion_rate:.1f}%")
        
        if completed_plans:
            print("\n✅ 已完成的计划:")
            for plan in completed_plans:
                print(f"  • {plan['event']}")
                
        if uncompleted_plans:
            print("\n⏳ 未完成的计划:")
            for plan in uncompleted_plans:
                print(f"  • {plan['event']}")
                
    def daily_reflection(self):
        print("\n🤔 今日总结反思")
        print("-" * 40)
        
        # 感悟反思
        print("\n👉 相比昨天的进步之处:")
        progress_things = []
        for i in range(3):
            thing = input(f"  {i+1}. ").strip()
            if thing:
                progress_things.append(thing)
                
        print("\n😊 那些事还可以做的更好:")
        improvements = []
        for i in range(3):
            improvement = input(f"  {i+1}. ").strip()
            if improvement:
                improvements.append(improvement)
                
        print("\n❤️ 最感动/感恩的三个瞬间:")
        gratitude = []
        for i in range(3):
            grateful = input(f"  {i+1}. ").strip()
            if grateful:
                gratitude.append(grateful)
        
        # 保存总结
        summary_data = {
            "date": datetime.now().date().isoformat(),
            "progress": progress_things,
            "improvements": improvements,
            "gratitude": gratitude,
            "completion_stats": {
                "total_plans": len(self.plans),
                "completed": len([p for p in self.plans if p["completed"]]),
                "completion_rate": len([p for p in self.plans if p["completed"]]) / len(self.plans) * 100 if self.plans else 0
            }
        }
        
        summary_file = f"summary_{datetime.now().date().isoformat()}.json"
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 总结已保存到 {summary_file}")
        except Exception as e:
            print(f"❌ 保存总结失败: {str(e)}")
            
    def save_data(self):
        try:
            data = {
                "plans": self.plans,
                "saved_at": datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 数据已保存到 {self.data_file}")
        except Exception as e:
            print(f"❌ 保存数据失败: {str(e)}")
            
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.plans = data.get("plans", [])
                print(f"📂 数据已从 {self.data_file} 加载")
            except Exception as e:
                print(f"❌ 加载数据失败: {str(e)}")
        else:
            print("📂 未找到数据文件，将创建新的数据文件")
            
    def run(self):
        print("🎉 欢迎使用每日计划与总结系统！")
        
        while True:
            self.display_menu()
            choice = input("\n请选择操作 (0-8): ").strip()
            
            if choice == "1":
                self.add_plan()
            elif choice == "2":
                self.view_plans()
            elif choice == "3":
                self.mark_completed()
            elif choice == "4":
                self.delete_plan()
            elif choice == "5":
                self.view_completion_status()
            elif choice == "6":
                self.daily_reflection()
            elif choice == "7":
                self.save_data()
            elif choice == "8":
                self.load_data()
            elif choice == "0":
                print("\n👋 感谢使用每日计划与总结系统！")
                self.save_data()
                break
            else:
                print("❌ 无效选择，请重新输入")
                
            input("\n按回车键继续...")

def main():
    app = DailyPlannerCLI()
    app.run()

if __name__ == "__main__":
    main()
