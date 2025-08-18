#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日计划与总结表单应用程序
使用tkinter创建GUI界面，支持每日计划制定和总结反思
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class DailyPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("每日计划与总结")
        self.root.geometry("1000x800")
        
        # 数据存储
        self.plans = []
        self.data_file = "daily_data.json"
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.load_data()
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主窗口的网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="每日计划与总结", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 创建笔记本控件（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # 今日计划标签页
        self.plan_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.plan_frame, text="👉今日计划")
        
        # 今日总结标签页
        self.summary_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.summary_frame, text="👉今日总结反思")
        
        # 创建今日计划界面
        self.create_plan_interface()
        
        # 创建总结界面
        self.create_summary_interface()
        
    def create_plan_interface(self):
        # 计划输入区域
        input_frame = ttk.LabelFrame(self.plan_frame, text="添加新计划", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.plan_frame.columnconfigure(0, weight=1)
        
        # 计划事件
        ttk.Label(input_frame, text="计划事件:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.plan_event_var = tk.StringVar()
        plan_event_entry = ttk.Entry(input_frame, textvariable=self.plan_event_var, width=30)
        plan_event_entry.grid(row=0, column=1, padx=(0, 10))
        
        # 重要等级
        ttk.Label(input_frame, text="重要等级:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.importance_var = tk.StringVar()
        importance_combo = ttk.Combobox(input_frame, textvariable=self.importance_var, 
                                      values=["十分重要", "重要", "一般重要", "不重要"], width=12)
        importance_combo.grid(row=0, column=3, padx=(0, 10))
        importance_combo.set("重要")
        
        # 紧急程度
        ttk.Label(input_frame, text="紧急程度:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.urgency_var = tk.StringVar()
        urgency_combo = ttk.Combobox(input_frame, textvariable=self.urgency_var,
                                   values=["十分紧急", "紧急", "不紧急"], width=12)
        urgency_combo.grid(row=0, column=5, padx=(0, 10))
        urgency_combo.set("紧急")
        
        # 第二行
        # 开始时间
        ttk.Label(input_frame, text="开始时间:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.start_time_var = tk.StringVar()
        start_time_entry = ttk.Entry(input_frame, textvariable=self.start_time_var, width=10)
        start_time_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.start_time_var.set("7:00")
        
        # 计划时长
        ttk.Label(input_frame, text="计划时长:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.duration_var = tk.StringVar()
        duration_entry = ttk.Entry(input_frame, textvariable=self.duration_var, width=10)
        duration_entry.grid(row=1, column=3, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.duration_var.set("1小时")
        
        # 添加按钮
        add_button = ttk.Button(input_frame, text="添加计划", command=self.add_plan)
        add_button.grid(row=1, column=4, pady=(10, 0))
        
        # 计划列表
        list_frame = ttk.LabelFrame(self.plan_frame, text="今日计划列表", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.plan_frame.rowconfigure(1, weight=1)
        
        # 创建树形控件显示计划
        columns = ("计划事件", "重要等级", "紧急程度", "开始时间", "计划时长", "完成状态")
        self.plan_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        # 设置列标题
        for col in columns:
            self.plan_tree.heading(col, text=col)
            self.plan_tree.column(col, width=120)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.plan_tree.yview)
        self.plan_tree.configure(yscrollcommand=scrollbar.set)
        
        self.plan_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 操作按钮
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="标记完成", command=self.mark_completed).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="删除计划", command=self.delete_plan).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="保存数据", command=self.save_data).pack(side=tk.LEFT)
        
    def create_summary_interface(self):
        # 计划完成情况
        completion_frame = ttk.LabelFrame(self.summary_frame, text="计划完成情况", padding="10")
        completion_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.summary_frame.columnconfigure(0, weight=1)
        
        # 创建完成情况表格
        comp_columns = ("已完成", "未完成", "未完成原因", "需要调整")
        self.completion_tree = ttk.Treeview(completion_frame, columns=comp_columns, show="headings", height=6)
        
        for col in comp_columns:
            self.completion_tree.heading(col, text=col)
            self.completion_tree.column(col, width=200)
        
        self.completion_tree.grid(row=0, column=0, sticky=(tk.W, tk.E))
        completion_frame.columnconfigure(0, weight=1)
        
        # 感情反思
        emotion_frame = ttk.LabelFrame(self.summary_frame, text="感情反思", padding="10")
        emotion_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.summary_frame.rowconfigure(1, weight=1)
        
        # 情绪复选框
        ttk.Label(emotion_frame, text="👉值得开心的事情之最:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.emotion_vars = {}
        emotions = ["情绪保护一般值、能等一次略容", "其他情绪选项1", "其他情绪选项2"]
        
        for i, emotion in enumerate(emotions):
            var = tk.BooleanVar()
            self.emotion_vars[emotion] = var
            ttk.Checkbutton(emotion_frame, text=emotion, variable=var).grid(row=i+1, column=0, sticky=tk.W, pady=2)
        
        # 更是想去对以往的更好
        ttk.Label(emotion_frame, text="😊 更是想去对以往的更好:").grid(row=len(emotions)+2, column=0, sticky=tk.W, pady=(20, 10))
        
        improvement_items = ["不动声色，更好的自己复合()", "", ""]
        self.improvement_vars = {}
        
        for i, item in enumerate(improvement_items):
            var = tk.StringVar()
            self.improvement_vars[f"improvement_{i}"] = var
            ttk.Entry(emotion_frame, textvariable=var, width=50).grid(row=len(emotions)+3+i, column=0, sticky=tk.W, pady=2)
            if item:
                var.set(item)
        
        # 最想对谁感恩三个问题
        ttk.Label(emotion_frame, text="❤️ 最想对谁感恩三个问题:").grid(row=len(emotions)+6, column=0, sticky=tk.W, pady=(20, 10))
        
        gratitude_items = ["保持慢慢的心，生活就美好好", "", ""]
        self.gratitude_vars = {}
        
        for i, item in enumerate(gratitude_items):
            var = tk.StringVar()
            self.gratitude_vars[f"gratitude_{i}"] = var
            ttk.Entry(emotion_frame, textvariable=var, width=50).grid(row=len(emotions)+7+i, column=0, sticky=tk.W, pady=2)
            if item:
                var.set(item)
        
        # 保存总结按钮
        save_summary_button = ttk.Button(emotion_frame, text="保存总结", command=self.save_summary)
        save_summary_button.grid(row=len(emotions)+10, column=0, pady=(20, 0))
        
    def add_plan(self):
        event = self.plan_event_var.get().strip()
        if not event:
            messagebox.showwarning("警告", "请输入计划事件")
            return
            
        plan = {
            "event": event,
            "importance": self.importance_var.get(),
            "urgency": self.urgency_var.get(),
            "start_time": self.start_time_var.get(),
            "duration": self.duration_var.get(),
            "completed": False,
            "timestamp": datetime.now().isoformat()
        }
        
        self.plans.append(plan)
        self.update_plan_tree()
        
        # 清空输入框
        self.plan_event_var.set("")
        self.start_time_var.set("7:00")
        self.duration_var.set("1小时")
        
    def update_plan_tree(self):
        # 清空树形控件
        for item in self.plan_tree.get_children():
            self.plan_tree.delete(item)
            
        # 添加计划到树形控件
        for plan in self.plans:
            status = "✅已完成" if plan["completed"] else "⏳进行中"
            self.plan_tree.insert("", tk.END, values=(
                plan["event"],
                plan["importance"],
                plan["urgency"],
                plan["start_time"],
                plan["duration"],
                status
            ))
            
    def mark_completed(self):
        selection = self.plan_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要标记完成的计划")
            return
            
        item = selection[0]
        index = self.plan_tree.index(item)
        self.plans[index]["completed"] = True
        self.update_plan_tree()
        self.update_completion_summary()
        
    def delete_plan(self):
        selection = self.plan_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的计划")
            return
            
        if messagebox.askyesno("确认", "确定要删除选中的计划吗？"):
            item = selection[0]
            index = self.plan_tree.index(item)
            del self.plans[index]
            self.update_plan_tree()
            self.update_completion_summary()
            
    def update_completion_summary(self):
        # 清空完成情况表格
        for item in self.completion_tree.get_children():
            self.completion_tree.delete(item)
            
        completed_plans = [p for p in self.plans if p["completed"]]
        uncompleted_plans = [p for p in self.plans if not p["completed"]]
        
        # 添加完成情况统计
        for plan in completed_plans:
            self.completion_tree.insert("", tk.END, values=(
                plan["event"], "", "", ""
            ))
            
        for plan in uncompleted_plans:
            self.completion_tree.insert("", tk.END, values=(
                "", plan["event"], "待填写原因", "明日再试/调整策略"
            ))
            
    def save_data(self):
        try:
            data = {
                "plans": self.plans,
                "saved_at": datetime.now().isoformat()
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("成功", "数据已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败：{str(e)}")
            
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.plans = data.get("plans", [])
                    self.update_plan_tree()
                    self.update_completion_summary()
            except Exception as e:
                print(f"加载数据失败：{str(e)}")
                
    def save_summary(self):
        summary_data = {
            "emotions": {k: v.get() for k, v in self.emotion_vars.items()},
            "improvements": {k: v.get() for k, v in self.improvement_vars.items()},
            "gratitude": {k: v.get() for k, v in self.gratitude_vars.items()},
            "date": datetime.now().date().isoformat()
        }
        
        # 保存到文件
        summary_file = f"summary_{datetime.now().date().isoformat()}.json"
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("成功", f"总结已保存到 {summary_file}")
        except Exception as e:
            messagebox.showerror("错误", f"保存总结失败：{str(e)}")

def main():
    root = tk.Tk()
    app = DailyPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
