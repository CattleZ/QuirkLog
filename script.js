// 每日计划与总结 - JavaScript 功能

class DailyPlanner {
    constructor() {
        this.plans = [];
        this.loadData();
        this.initEventListeners();
        this.updatePlanTable();
        this.updateCompletionStats();
        this.loadTodayReflection();
        
        // 确保在初始化时加载今天的完成情况数据
        setTimeout(() => this.loadCompletionData(), 200);
    }

    initEventListeners() {
        // 计划表单提交
        document.getElementById('plan-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addPlan();
        });

        // 反思输入框变化时自动保存
        this.setupReflectionAutoSave();

        // 加载数据
        this.loadData();
    }

    setupReflectionAutoSave() {
        // 为所有反思输入框添加自动保存功能
        const reflectionInputs = document.querySelectorAll('.progress-input, .improvement-input, .gratitude-input');
        reflectionInputs.forEach(input => {
            // 移除之前的事件监听器
            input.removeEventListener('blur', this.saveReflectionHandler);
            input.removeEventListener('input', this.inputReflectionHandler);
            
            // 添加新的事件监听器
            this.saveReflectionHandler = () => this.saveReflectionData();
            this.inputReflectionHandler = () => {
                clearTimeout(this.saveTimeout);
                this.saveTimeout = setTimeout(() => {
                    this.saveReflectionData();
                }, 1000);
            };
            
            input.addEventListener('blur', this.saveReflectionHandler);
            input.addEventListener('input', this.inputReflectionHandler);
        });
    }

    saveReflectionData() {
        const today = new Date().toISOString().split('T')[0];
        const reflectionData = {
            date: today,
            progress: this.getInputValues('.progress-input'),
            improvements: this.getInputValues('.improvement-input'),
            gratitude: this.getInputValues('.gratitude-input'),
            lastUpdated: new Date().toISOString()
        };
        
        localStorage.setItem(`reflection_${today}`, JSON.stringify(reflectionData));
    }

    getInputValues(selector) {
        const values = [];
        document.querySelectorAll(selector).forEach(input => {
            values.push(input.value);
        });
        return values;
    }

    loadTodayReflection() {
        const today = new Date().toISOString().split('T')[0];
        const reflectionData = localStorage.getItem(`reflection_${today}`);
        
        if (reflectionData) {
            try {
                const data = JSON.parse(reflectionData);
                this.loadReflectionSection('progress', data.progress || []);
                this.loadReflectionSection('improvement', data.improvements || []);
                this.loadReflectionSection('gratitude', data.gratitude || []);
            } catch (e) {
                console.error('加载反思数据失败:', e);
            }
        }
        
        // 加载每日思考
        this.loadDailyThoughts();
    }

    loadDailyThoughts() {
        const today = new Date().toISOString().split('T')[0];
        const savedThoughts = localStorage.getItem(`daily-thoughts-${today}`);
        const textarea = document.getElementById('daily-thoughts');
        
        if (savedThoughts && textarea) {
            textarea.value = savedThoughts;
        }
    }

    loadReflectionSection(type, values) {
        const groupId = `${type}-group`;
        const group = document.getElementById(groupId);
        
        // 清空现有行
        group.innerHTML = '';
        
        // 确保至少有一行
        const valuesToLoad = values.length > 0 ? values : [''];
        
        valuesToLoad.forEach((value, index) => {
            const row = document.createElement('div');
            row.className = 'input-row';
            
            let placeholder = '';
            let inputClass = '';
            
            switch(type) {
                case 'progress':
                    placeholder = '输入进步之处...';
                    inputClass = 'progress-input';
                    break;
                case 'improvement':
                    placeholder = '输入改进点...';
                    inputClass = 'improvement-input';
                    break;
                case 'gratitude':
                    placeholder = '感动/感恩的瞬间...';
                    inputClass = 'gratitude-input';
                    break;
            }
            
            row.innerHTML = `
                <input type="text" class="${inputClass}" placeholder="${placeholder}" value="${value}" data-index="${index}">
                <div class="row-controls">
                    <button type="button" class="btn btn-sm btn-success" onclick="addInputRow('${type}')">+</button>
                    <button type="button" class="btn btn-sm btn-danger" onclick="removeInputRow(this, '${type}')">-</button>
                </div>
            `;
            
            group.appendChild(row);
        });
        
        // 重新设置自动保存
        this.setupReflectionAutoSave();
    }

    setInputValues(selector, values) {
        const inputs = document.querySelectorAll(selector);
        inputs.forEach((input, index) => {
            if (values[index] !== undefined) {
                input.value = values[index];
            }
        });
    }

    addPlan() {
        const form = document.getElementById('plan-form');
        const formData = new FormData(form);
        
        const plan = {
            id: Date.now(),
            event: formData.get('event'),
            importance: formData.get('importance'),
            urgency: formData.get('urgency'),
            startTime: formData.get('start_time'), // 修复字段名不一致
            duration: formData.get('duration'),
            completed: false,
            timestamp: new Date().toISOString()
        };

        this.plans.push(plan);
        this.updatePlanTable();
        this.updateCompletionStats();
        this.saveData();
        
        // 清空表单
        form.reset();
        document.getElementById('start_time').value = '07:00';
        document.getElementById('duration').value = '1小时';
        
        this.showMessage('✅ 计划添加成功！', 'success');
    }

    updatePlanTable() {
        const tbody = document.getElementById('plans-tbody');
        tbody.innerHTML = '';

        this.plans.forEach(plan => {
            const row = document.createElement('tr');
            const statusClass = plan.completed ? 'status-completed' : 'status-pending';
            const statusText = plan.completed ? '✅已完成' : '⏳进行中';
            
            row.innerHTML = `
                <td>${plan.event}</td>
                <td><span class="badge badge-${this.getImportanceBadgeClass(plan.importance)}">${plan.importance}</span></td>
                <td><span class="badge badge-${this.getUrgencyBadgeClass(plan.urgency)}">${plan.urgency}</span></td>
                <td>${plan.startTime || plan.start_time || '未设置'}</td>
                <td>${plan.duration}</td>
                <td class="${statusClass}">${statusText}</td>
                <td>
                    <button onclick="planner.toggleComplete(${plan.id})" class="btn btn-sm ${plan.completed ? 'btn-warning' : 'btn-success'}">
                        ${plan.completed ? '取消完成' : '标记完成'}
                    </button>
                    <button onclick="planner.deletePlan(${plan.id})" class="btn btn-sm btn-danger">删除</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    getImportanceBadgeClass(importance) {
        const map = {
            '十分重要': 'danger',
            '重要': 'warning', 
            '一般重要': 'info',
            '不重要': 'secondary'
        };
        return map[importance] || 'secondary';
    }

    getUrgencyBadgeClass(urgency) {
        const map = {
            '十分紧急': 'danger',
            '紧急': 'warning',
            '不紧急': 'success'
        };
        return map[urgency] || 'secondary';
    }

    toggleComplete(planId) {
        const plan = this.plans.find(p => p.id === planId);
        if (plan) {
            plan.completed = !plan.completed;
            this.updatePlanTable();
            this.updateCompletionStats();
            this.saveData();
            
            const message = plan.completed ? 
                `✅ "${plan.event}" 已标记为完成！` : 
                `⏳ "${plan.event}" 已标记为未完成`;
            this.showMessage(message, 'success');
        }
    }

    deletePlan(planId) {
        if (confirm('确定要删除这个计划吗？')) {
            const index = this.plans.findIndex(p => p.id === planId);
            if (index !== -1) {
                const deletedPlan = this.plans.splice(index, 1)[0];
                this.updatePlanTable();
                this.updateCompletionStats();
                this.saveData();
                this.showMessage(`🗑️ "${deletedPlan.event}" 已删除`, 'info');
            }
        }
    }

    updateCompletionStats() {
        const total = this.plans.length;
        const completed = this.plans.filter(p => p.completed).length;
        const pending = total - completed;
        const completionRate = total > 0 ? ((completed / total) * 100).toFixed(1) : 0;

        const statsContainer = document.getElementById('completion-stats');
        statsContainer.innerHTML = `
            <div class="stat-item">
                <span class="stat-number">${total}</span>
                <span class="stat-label">总计划</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${completed}</span>
                <span class="stat-label">已完成</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${pending}</span>
                <span class="stat-label">未完成</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${completionRate}%</span>
                <span class="stat-label">完成率</span>
            </div>
        `;

        // 更新完成情况表格
        this.updateCompletionTable();
    }

    updateCompletionTable() {
        const tbody = document.getElementById('completion-tbody');
        tbody.innerHTML = '';

        const pendingPlans = this.plans.filter(p => !p.completed);

        if (pendingPlans.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="3" style="text-align: center; color: #666;">🎉 所有计划都已完成！</td>
            `;
            tbody.appendChild(row);
            return;
        }

        pendingPlans.forEach((plan, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${plan.event}</td>
                <td><input type="text" placeholder="输入未完成原因..." class="form-control incomplete-reason" data-plan-id="${plan.id}"></td>
                <td><input type="text" placeholder="调整策略..." class="form-control adjustment-strategy" data-plan-id="${plan.id}"></td>
            `;
            tbody.appendChild(row);
        });

        // 为输入框添加事件监听器以自动保存
        this.setupCompletionInputListeners();
        
        // 加载已保存的完成情况数据
        setTimeout(() => this.loadCompletionData(), 100);
    }

    setupCompletionInputListeners() {
        // 为未完成原因和调整策略输入框添加事件监听器
        const reasonInputs = document.querySelectorAll('.incomplete-reason');
        const adjustmentInputs = document.querySelectorAll('.adjustment-strategy');
        
        [...reasonInputs, ...adjustmentInputs].forEach(input => {
            input.addEventListener('blur', () => this.saveCompletionData());
            input.addEventListener('input', () => {
                clearTimeout(this.completionSaveTimeout);
                this.completionSaveTimeout = setTimeout(() => {
                    this.saveCompletionData();
                }, 1000);
            });
        });
    }

    saveCompletionData() {
        const today = new Date().toISOString().split('T')[0];
        const completionData = {};
        
        // 收集未完成原因
        document.querySelectorAll('.incomplete-reason').forEach(input => {
            const planId = input.getAttribute('data-plan-id');
            if (input.value.trim()) {
                if (!completionData[planId]) completionData[planId] = {};
                completionData[planId].incompleteReason = input.value.trim();
            }
        });
        
        // 收集调整策略
        document.querySelectorAll('.adjustment-strategy').forEach(input => {
            const planId = input.getAttribute('data-plan-id');
            if (input.value.trim()) {
                if (!completionData[planId]) completionData[planId] = {};
                completionData[planId].adjustmentStrategy = input.value.trim();
            }
        });
        
        localStorage.setItem(`completion_data_${today}`, JSON.stringify(completionData));
    }

    loadCompletionData() {
        const today = new Date().toISOString().split('T')[0];
        const completionData = localStorage.getItem(`completion_data_${today}`);
        
        if (completionData) {
            try {
                const data = JSON.parse(completionData);
                
                // 加载未完成原因
                document.querySelectorAll('.incomplete-reason').forEach(input => {
                    const planId = input.getAttribute('data-plan-id');
                    if (data[planId] && data[planId].incompleteReason) {
                        input.value = data[planId].incompleteReason;
                    }
                });
                
                // 加载调整策略
                document.querySelectorAll('.adjustment-strategy').forEach(input => {
                    const planId = input.getAttribute('data-plan-id');
                    if (data[planId] && data[planId].adjustmentStrategy) {
                        input.value = data[planId].adjustmentStrategy;
                    }
                });
            } catch (e) {
                console.error('加载完成情况数据失败:', e);
            }
        }
    }

    saveData() {
        // 现在使用统一的保存逻辑，但保持兼容性
        const data = {
            plans: this.plans,
            savedAt: new Date().toISOString()
        };
        localStorage.setItem('plans', JSON.stringify(this.plans));
        localStorage.setItem('dailyPlannerData', JSON.stringify(data));
    }

    loadData() {
        const data = localStorage.getItem('dailyPlannerData');
        if (data) {
            try {
                const parsed = JSON.parse(data);
                this.plans = parsed.plans || [];
                
                // 数据迁移：确保所有计划都有正确的字段名
                this.plans = this.plans.map(plan => {
                    if (plan.start_time && !plan.startTime) {
                        plan.startTime = plan.start_time;
                        delete plan.start_time; // 删除旧字段
                    }
                    return plan;
                });
            } catch (e) {
                console.error('加载数据失败:', e);
                this.plans = [];
            }
        }
    }

    exportData() {
        const data = {
            exportDate: new Date().toISOString(),
            plans: this.plans,
            statistics: {
                total: this.plans.length,
                completed: this.plans.filter(p => p.completed).length,
                completionRate: this.plans.length > 0 ? 
                    ((this.plans.filter(p => p.completed).length / this.plans.length) * 100).toFixed(1) : 0
            }
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `daily_plans_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        
        this.showMessage('📥 数据导出成功！', 'success');
    }

    clearAll() {
        if (confirm('确定要清空所有计划吗？此操作不可恢复！')) {
            this.plans = [];
            this.updatePlanTable();
            this.updateCompletionStats();
            this.saveData();
            this.showMessage('🗑️ 所有计划已清空', 'warning');
        }
    }

    saveSummary() {
        // 这个方法现在由统一的保存逻辑处理
        this.saveAllData();
    }

    exportSummary() {
        // 这个方法现在由统一的导出逻辑处理
        this.exportToPDF();
    }

    // 统一保存所有数据
    saveAllData() {
        const today = new Date().toISOString().split('T')[0];
        
        // 验证日期信息
        if (!this.validateDateInfo(today)) {
            return;
        }
        
        // 收集计划数据
        const plansData = this.plans.map(plan => ({
            id: plan.id,
            event: plan.event,
            importance: plan.importance,
            urgency: plan.urgency,
            startTime: plan.startTime,
            duration: plan.duration,
            completed: plan.completed || false
        }));

        // 收集反思数据
        const progress = [];
        document.querySelectorAll('.progress-input').forEach(input => {
            if (input.value.trim()) {
                progress.push(input.value.trim());
            }
        });

        const improvements = [];
        document.querySelectorAll('.improvement-input').forEach(input => {
            if (input.value.trim()) {
                improvements.push(input.value.trim());
            }
        });

        const gratitude = [];
        document.querySelectorAll('.gratitude-input').forEach(input => {
            if (input.value.trim()) {
                gratitude.push(input.value.trim());
            }
        });

        const dailyThoughts = document.getElementById('daily-thoughts').value;

        // 收集完成情况数据（未完成原因和调整策略）
        const completionDetails = {};
        document.querySelectorAll('.incomplete-reason').forEach(input => {
            const planId = input.getAttribute('data-plan-id');
            if (input.value.trim()) {
                if (!completionDetails[planId]) completionDetails[planId] = {};
                completionDetails[planId].incompleteReason = input.value.trim();
            }
        });
        
        document.querySelectorAll('.adjustment-strategy').forEach(input => {
            const planId = input.getAttribute('data-plan-id');
            if (input.value.trim()) {
                if (!completionDetails[planId]) completionDetails[planId] = {};
                completionDetails[planId].adjustmentStrategy = input.value.trim();
            }
        });

        // 构建完整的日记数据，确保包含完整的日期信息
        const dateObj = new Date();
        const dailyRecord = {
            date: today,
            dateInfo: {
                year: dateObj.getFullYear(),
                month: dateObj.getMonth() + 1,
                day: dateObj.getDate(),
                weekday: dateObj.getDay(),
                weekdayName: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][dateObj.getDay()],
                fullDateString: dateObj.toLocaleDateString('zh-CN', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    weekday: 'long'
                })
            },
            plans: plansData,
            reflection: {
                progress: progress,
                improvements: improvements,
                gratitude: gratitude,
                dailyThoughts: dailyThoughts
            },
            completionDetails: completionDetails,
            statistics: {
                totalPlans: plansData.length,
                completedPlans: plansData.filter(p => p.completed).length,
                completionRate: plansData.length > 0 ? 
                    ((plansData.filter(p => p.completed).length / plansData.length) * 100).toFixed(1) : 0
            },
            savedAt: new Date().toISOString(),
            version: "1.0"
        };

        // 验证数据完整性
        if (!this.validateRecordData(dailyRecord)) {
            return;
        }

        // 保存到localStorage
        localStorage.setItem(`daily-record-${today}`, JSON.stringify(dailyRecord));
        
        // 同时更新计划数据
        localStorage.setItem('plans', JSON.stringify(this.plans));
        
        // 生成文件名
        const fileName = getFormattedFileName(today);
        
        // 检查是否应该保存到服务器指定路径
        if (currentSettings.autoSave && currentSettings.saveDirectory) {
            this.saveToServerPath(dailyRecord, fileName);
        } else {
            // 传统的浏览器下载方式
            this.downloadAsFile(dailyRecord, fileName);
        }
        
        this.showMessage(`💾 保存成功！`, 'success');
        
        // 保存完成情况数据到localStorage
        this.saveCompletionData();
        
        // 更新侧边栏树状结构
        updateRecordTreeAfterSave();
    }
    
    // 保存到服务器指定路径
    saveToServerPath(dailyRecord, fileName) {
        fetch('/api/save-daily-record', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dailyRecord)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('✅ 文件已保存到指定路径:', data.filePath);
                this.showMessage(`💾 文件已保存到: ${data.filePath}`, 'success');
            } else {
                console.error('❌ 服务器保存失败:', data.message);
                this.showMessage('⚠️ 服务器保存失败，尝试下载到本地', 'warning');
                this.downloadAsFile(dailyRecord, fileName);
            }
        })
        .catch(error => {
            console.error('❌ 网络错误:', error);
            this.showMessage('⚠️ 网络错误，尝试下载到本地', 'warning');
            this.downloadAsFile(dailyRecord, fileName);
        });
    }
    
    // 传统的浏览器下载方式
    downloadAsFile(dailyRecord, fileName) {
        const blob = new Blob([JSON.stringify(dailyRecord, null, 2)], { 
            type: 'application/json;charset=utf-8' 
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${fileName}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    // 验证日期信息
    validateDateInfo(dateString) {
        if (!dateString) {
            this.showMessage('❌ 日期信息缺失，无法保存！', 'error');
            return false;
        }

        // 验证日期格式
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(dateString)) {
            this.showMessage('❌ 日期格式不正确，无法保存！', 'error');
            return false;
        }

        // 验证日期是否有效
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            this.showMessage('❌ 无效的日期，无法保存！', 'error');
            return false;
        }

        // 检查是否为未来日期（可选限制）
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        date.setHours(0, 0, 0, 0);
        
        if (date > today) {
            if (!confirm('⚠️ 您正在保存未来日期的记录，确定继续吗？')) {
                return false;
            }
        }

        return true;
    }

    // 验证记录数据完整性
    validateRecordData(record) {
        // 检查必需的日期信息
        if (!record.dateInfo || !record.dateInfo.year || !record.dateInfo.month || !record.dateInfo.day) {
            this.showMessage('❌ 记录缺少完整的年月日信息，无法保存！', 'error');
            return false;
        }

        // 检查年份范围
        const currentYear = new Date().getFullYear();
        if (record.dateInfo.year < 2020 || record.dateInfo.year > currentYear + 1) {
            this.showMessage('❌ 年份信息异常，无法保存！', 'error');
            return false;
        }

        // 检查月份范围
        if (record.dateInfo.month < 1 || record.dateInfo.month > 12) {
            this.showMessage('❌ 月份信息异常，无法保存！', 'error');
            return false;
        }

        // 检查日期范围
        if (record.dateInfo.day < 1 || record.dateInfo.day > 31) {
            this.showMessage('❌ 日期信息异常，无法保存！', 'error');
            return false;
        }

        // 检查数据结构完整性
        if (!record.plans || !record.reflection || !record.statistics) {
            this.showMessage('❌ 记录数据结构不完整，无法保存！', 'error');
            return false;
        }

        return true;
    }

    // 导出为PDF
    exportToPDF() {
        const today = new Date().toISOString().split('T')[0];
        const dateOptions = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric', 
            weekday: 'long' 
        };
        const dateString = new Date().toLocaleDateString('zh-CN', dateOptions);
        
        // 收集所有数据
        const progress = [];
        document.querySelectorAll('.progress-input').forEach(input => {
            if (input.value.trim()) {
                progress.push(input.value.trim());
            }
        });

        const improvements = [];
        document.querySelectorAll('.improvement-input').forEach(input => {
            if (input.value.trim()) {
                improvements.push(input.value.trim());
            }
        });

        const gratitude = [];
        document.querySelectorAll('.gratitude-input').forEach(input => {
            if (input.value.trim()) {
                gratitude.push(input.value.trim());
            }
        });

        const dailyThoughts = document.getElementById('daily-thoughts').value;

        // 收集完成情况数据
        const completionDetails = {};
        document.querySelectorAll('.incomplete-reason').forEach(input => {
            const planId = input.getAttribute('data-plan-id');
            if (input.value.trim()) {
                if (!completionDetails[planId]) completionDetails[planId] = {};
                completionDetails[planId].incompleteReason = input.value.trim();
            }
        });
        
        document.querySelectorAll('.adjustment-strategy').forEach(input => {
            const planId = input.getAttribute('data-plan-id');
            if (input.value.trim()) {
                if (!completionDetails[planId]) completionDetails[planId] = {};
                completionDetails[planId].adjustmentStrategy = input.value.trim();
            }
        });

        // 构建PDF内容
        let pdfContent = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>每日记录 - ${dateString}</title>
    <style>
        body { font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; line-height: 1.6; margin: 40px; color: #333; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        h3 { color: #7f8c8d; }
        .plans-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .plans-table th, .plans-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        .plans-table th { background-color: #f8f9fa; font-weight: bold; }
        .completed { background-color: #d4edda; }
        .incomplete { background-color: #f8d7da; }
        .reflection-item { margin: 10px 0; padding: 8px; background: #f8f9fa; border-left: 4px solid #3498db; }
        .thoughts-content { background: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 8px; margin: 15px 0; }
        .stats { background: #e8f4fd; padding: 15px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>🌞 ${dateString} 每日记录</h1>
    
    <div class="stats">
        <h3>📊 统计信息</h3>
        <p>总计划数: ${this.plans.length} | 已完成: ${this.plans.filter(p => p.completed).length} | 完成率: ${this.plans.length > 0 ? ((this.plans.filter(p => p.completed).length / this.plans.length) * 100).toFixed(1) : 0}%</p>
    </div>

    <h2>📋 今日计划</h2>
    <table class="plans-table">
        <thead>
            <tr>
                <th>计划事件</th>
                <th>重要等级</th>
                <th>紧急程度</th>
                <th>开始时间</th>
                <th>计划时长</th>
                <th>完成状态</th>
            </tr>
        </thead>
        <tbody>
            ${this.plans.map(plan => `
                <tr class="${plan.completed ? 'completed' : 'incomplete'}">
                    <td>${plan.event}</td>
                    <td>${plan.importance}</td>
                    <td>${plan.urgency}</td>
                    <td>${plan.startTime || plan.start_time || '未设置'}</td>
                    <td>${plan.duration}</td>
                    <td>${plan.completed ? '✅ 已完成' : '❌ 未完成'}</td>
                </tr>
            `).join('')}
        </tbody>
    </table>

    <h2>📝 计划完成情况分析</h2>
    ${this.plans.filter(p => !p.completed).length > 0 ? `
    <table class="plans-table">
        <thead>
            <tr>
                <th>未完成计划</th>
                <th>未完成原因</th>
                <th>需要调整</th>
            </tr>
        </thead>
        <tbody>
            ${this.plans.filter(p => !p.completed).map(plan => {
                const details = completionDetails[plan.id] || {};
                return `
                <tr class="incomplete">
                    <td>${plan.event}</td>
                    <td>${details.incompleteReason || '未填写'}</td>
                    <td>${details.adjustmentStrategy || '未填写'}</td>
                </tr>
                `;
            }).join('')}
        </tbody>
    </table>
    ` : '<p style="color: #28a745; font-weight: bold;">🎉 恭喜！所有计划都已完成！</p>'}

    <h2>🤔 感悟反思</h2>
    
    <h3>👉 相比昨天的进步之处:</h3>
    ${progress.length > 0 ? progress.map(item => `<div class="reflection-item">${item}</div>`).join('') : '<p>暂无记录</p>'}
    
    <h3>😊 那些事还可以做的更好:</h3>
    ${improvements.length > 0 ? improvements.map(item => `<div class="reflection-item">${item}</div>`).join('') : '<p>暂无记录</p>'}
    
    <h3>❤️ 最感动/感恩的三个瞬间:</h3>
    ${gratitude.length > 0 ? gratitude.map(item => `<div class="reflection-item">${item}</div>`).join('') : '<p>暂无记录</p>'}
    
    <h3>☕️ 每日思考:</h3>
    <div class="thoughts-content">
        ${dailyThoughts ? dailyThoughts.replace(/\n/g, '<br>') : '暂无记录'}
    </div>
    
    <hr style="margin: 40px 0;">
    <p style="text-align: center; color: #7f8c8d; font-size: 12px;">
        生成时间: ${new Date().toLocaleString('zh-CN')} | 每日计划与总结系统
    </p>
</body>
</html>`;

        // 创建新窗口并打印
        const printWindow = window.open('', '_blank');
        printWindow.document.write(pdfContent);
        printWindow.document.close();
        
        // 等待内容加载完成后打印
        printWindow.onload = function() {
            setTimeout(() => {
                printWindow.print();
                printWindow.close();
            }, 500);
        };
        
        this.showMessage('📄 PDF导出窗口已打开，请在打印对话框中选择"保存为PDF"', 'info');
    }

    // 清空所有数据
    clearAllData() {
        if (!confirm('⚠️ 确定要清空今日所有记录吗？此操作不可恢复！')) {
            return;
        }
        
        // 清空计划
        this.plans = [];
        this.updatePlanTable();
        
        // 清空反思输入
        document.querySelectorAll('.progress-input, .improvement-input, .gratitude-input').forEach(input => {
            input.value = '';
        });
        
        // 清空每日思考
        document.getElementById('daily-thoughts').value = '';
        
        // 重置为默认的单行输入
        this.resetReflectionSections();
        
        // 清除localStorage中的今日数据
        const today = new Date().toISOString().split('T')[0];
        localStorage.removeItem('plans');
        localStorage.removeItem(`daily-record-${today}`);
        localStorage.removeItem(`reflection_${today}`);
        localStorage.removeItem(`daily-thoughts-${today}`);
        
        this.showMessage('保存成功！', 'warning');
    }

    resetReflectionSections() {
        // 重置进步之处
        const progressGroup = document.getElementById('progress-group');
        progressGroup.innerHTML = `
            <div class="input-row">
                <input type="text" class="progress-input" placeholder="输入进步之处..." data-index="0">
                <div class="row-controls">
                    <button type="button" class="btn btn-sm btn-success" onclick="addInputRow('progress')">+</button>
                    <button type="button" class="btn btn-sm btn-danger" onclick="removeInputRow(this, 'progress')">-</button>
                </div>
            </div>
        `;
        
        // 重置改进点
        const improvementGroup = document.getElementById('improvement-group');
        improvementGroup.innerHTML = `
            <div class="input-row">
                <input type="text" class="improvement-input" placeholder="输入改进点..." data-index="0">
                <div class="row-controls">
                    <button type="button" class="btn btn-sm btn-success" onclick="addInputRow('improvement')">+</button>
                    <button type="button" class="btn btn-sm btn-danger" onclick="removeInputRow(this, 'improvement')">-</button>
                </div>
            </div>
        `;
        
        // 重置感恩瞬间
        const gratitudeGroup = document.getElementById('gratitude-group');
        gratitudeGroup.innerHTML = `
            <div class="input-row">
                <input type="text" class="gratitude-input" placeholder="感动/感恩的瞬间..." data-index="0">
                <div class="row-controls">
                    <button type="button" class="btn btn-sm btn-success" onclick="addInputRow('gratitude')">+</button>
                    <button type="button" class="btn btn-sm btn-danger" onclick="removeInputRow(this, 'gratitude')">-</button>
                </div>
            </div>
        `;
        
        // 重新设置自动保存
        this.setupReflectionAutoSave();
    }

    showMessage(message, type = 'info') {
        // 创建消息提示
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type}`;
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease;
        `;

        // 设置背景颜色
        const colors = {
            success: '#28a745',
            warning: '#ffc107',
            danger: '#dc3545',
            info: '#17a2b8'
        };
        messageDiv.style.backgroundColor = colors[type] || colors.info;
        
        messageDiv.textContent = message;
        document.body.appendChild(messageDiv);

        // 3秒后自动移除
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    messageDiv.remove();
                }, 300);
            }
        }, 3000);
    }
}

// 标签页切换功能
function openTab(evt, tabName) {
    // 隐藏所有标签页内容
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }

    // 移除所有标签按钮的激活状态
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    // 显示选中的标签页内容
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');
}

// 全局函数，供HTML调用
function saveData() {
    planner.saveData();
    planner.showMessage('💾 数据已保存！', 'success');
}

function exportData() {
    planner.exportData();
}

function clearAll() {
    planner.clearAll();
}

function saveSummary() {
    planner.saveSummary();
}

function exportSummary() {
    planner.exportSummary();
}

// 新增的统一操作函数
function saveAllData() {
    planner.saveAllData();
}

function exportToPDF() {
    planner.exportToPDF();
}

function clearAllData() {
    planner.clearAllData();
}

// 动态添加输入行
function addInputRow(type) {
    const groupId = `${type}-group`;
    const group = document.getElementById(groupId);
    const existingRows = group.querySelectorAll('.input-row');
    const newIndex = existingRows.length;
    
    const newRow = document.createElement('div');
    newRow.className = 'input-row';
    
    let placeholder = '';
    let inputClass = '';
    
    switch(type) {
        case 'progress':
            placeholder = '输入进步之处...';
            inputClass = 'progress-input';
            break;
        case 'improvement':
            placeholder = '输入改进点...';
            inputClass = 'improvement-input';
            break;
        case 'gratitude':
            placeholder = '感动/感恩的瞬间...';
            inputClass = 'gratitude-input';
            break;
    }
    
    newRow.innerHTML = `
        <input type="text" class="${inputClass}" placeholder="${placeholder}" data-index="${newIndex}">
        <div class="row-controls">
            <button type="button" class="btn btn-sm btn-success" onclick="addInputRow('${type}')">+</button>
            <button type="button" class="btn btn-sm btn-danger" onclick="removeInputRow(this, '${type}')">-</button>
        </div>
    `;
    
    group.appendChild(newRow);
    
    // 重新设置自动保存
    planner.setupReflectionAutoSave();
}

// 动态删除输入行
function removeInputRow(button, type) {
    const groupId = `${type}-group`;
    const group = document.getElementById(groupId);
    const rows = group.querySelectorAll('.input-row');
    
    // 至少保留一行
    if (rows.length <= 1) {
        planner.showMessage('⚠️ 至少需要保留一行！', 'warning');
        return;
    }
    
    const row = button.closest('.input-row');
    row.remove();
    
    // 重新索引剩余的输入框
    const remainingRows = group.querySelectorAll('.input-row');
    remainingRows.forEach((row, index) => {
        const input = row.querySelector('input');
        input.setAttribute('data-index', index);
    });
    
    // 保存更改
    planner.saveReflectionData();
}

// CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    
    .badge-danger { background-color: #dc3545; }
    .badge-warning { background-color: #ffc107; color: #212529; }
    .badge-info { background-color: #17a2b8; }
    .badge-success { background-color: #28a745; }
    .badge-secondary { background-color: #6c757d; }
    
    .form-control {
        width: 100%;
        padding: 8px;
        border: 1px solid #ced4da;
        border-radius: 4px;
        font-size: 14px;
    }
    
    .form-control:focus {
        outline: none;
        border-color: #28a745;
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.1);
    }
`;
document.head.appendChild(style);

// 初始化应用
let planner;
document.addEventListener('DOMContentLoaded', () => {
    // 清理缓存
    clearPageCache();
    
    // 更新标题为当前日期
    updateTitle();
    
    planner = new DailyPlanner();
});

// 清理页面缓存
function clearPageCache(forceCleanToday = false) {
    const today = new Date().toISOString().split('T')[0];
    const lastClearDate = localStorage.getItem('lastCacheClearDate');
    
    // 如果是新的一天或者从未清理过，或者强制清理，则进行缓存清理
    if (!lastClearDate || lastClearDate !== today || forceCleanToday) {
        console.log('🧹 正在清理页面缓存...');
        
        // 清理可能过时的临时数据
        const keysToCheck = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key) {
                keysToCheck.push(key);
            }
        }
        
        let cleanedCount = 0;
        keysToCheck.forEach(key => {
            // 清理过期的每日数据（保留最近7天）
            if (key.includes('reflection_') || key.includes('daily-thoughts-') || key.includes('completion_data_')) {
                const dateMatch = key.match(/(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    const keyDate = new Date(dateMatch[1]);
                    const daysDiff = (new Date(today) - keyDate) / (1000 * 60 * 60 * 24);
                    
                    // 删除7天前的临时数据
                    if (daysDiff > 7) {
                        localStorage.removeItem(key);
                        cleanedCount++;
                    }
                }
            }
            
            // 清理每日记录数据（保留最近7天）
            if (key.startsWith('daily-record-')) {
                const dateMatch = key.match(/daily-record-(\d{4}-\d{2}-\d{2})/);
                if (dateMatch) {
                    const keyDate = new Date(dateMatch[1]);
                    const daysDiff = (new Date(today) - keyDate) / (1000 * 60 * 60 * 24);
                    
                    // 删除7天前的每日记录
                    if (daysDiff > 7) {
                        localStorage.removeItem(key);
                        cleanedCount++;
                    }
                }
            }
            
            // 清理可能损坏的数据
            if (key.startsWith('temp_') || key.startsWith('cache_')) {
                localStorage.removeItem(key);
                cleanedCount++;
            }
        });
        
        // 检查今日数据是否过期（如果不是今天的数据，清理计划数据）
        const dailyPlannerData = localStorage.getItem('dailyPlannerData');
        if (dailyPlannerData) {
            try {
                const parsed = JSON.parse(dailyPlannerData);
                if (parsed.savedAt) {
                    const savedDate = new Date(parsed.savedAt).toISOString().split('T')[0];
                    if (savedDate !== today) {
                        console.log(`🗑️ 清理非今日的计划数据 (${savedDate})`);
                        localStorage.removeItem('dailyPlannerData');
                        localStorage.removeItem('plans');
                        cleanedCount += 2;
                    } else if (forceCleanToday) {
                        console.log('🗑️ 强制清理今日的计划数据');
                        localStorage.removeItem('dailyPlannerData');
                        localStorage.removeItem('plans');
                        cleanedCount += 2;
                    }
                }
            } catch (e) {
                console.log('🗑️ 清理损坏的计划数据');
                localStorage.removeItem('dailyPlannerData');
                localStorage.removeItem('plans');
                cleanedCount += 2;
            }
        }
        
        // 如果强制清理，也清理今日的其他数据
        if (forceCleanToday) {
            localStorage.removeItem(`daily-record-${today}`);
            localStorage.removeItem(`reflection_${today}`);
            localStorage.removeItem(`daily-thoughts-${today}`);
            localStorage.removeItem(`completion_data_${today}`);
            cleanedCount += 4;
        }
        
        // 清理浏览器缓存（如果可能）
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(registrations => {
                registrations.forEach(registration => {
                    registration.update();
                });
            });
        }
        
        // 记录清理日期
        localStorage.setItem('lastCacheClearDate', today);
        
        if (cleanedCount > 0) {
            console.log(`✅ 已清理 ${cleanedCount} 项过期缓存数据`);
        }
        
        console.log('🎉 缓存清理完成');
    }
    
    // 强制刷新页面数据（清理内存中的旧数据）
    if (window.planner) {
        window.planner = null;
    }
}

// 检测页面刷新/重新加载
function detectPageRefresh() {
    // 检测是否为刷新操作
    if (performance.navigation && performance.navigation.type === 1) {
        console.log('🔄 检测到页面刷新，清理缓存');
        clearPageCache();
    }
    
    // 现代浏览器的检测方式
    if (performance.getEntriesByType && performance.getEntriesByType('navigation').length > 0) {
        const navEntry = performance.getEntriesByType('navigation')[0];
        if (navEntry.type === 'reload') {
            console.log('🔄 检测到页面重载，清理缓存');
            clearPageCache();
        }
    }
}

// 在页面加载前检测刷新
detectPageRefresh();

// 更新标题为当前日期
function updateTitle() {
    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        weekday: 'long' 
    };
    const dateString = now.toLocaleDateString('zh-CN', options);
    
    // 更新页面标题
    document.getElementById('main-title').textContent = `🌞 ${dateString} 计划与总结`;
    
    // 更新浏览器标签页标题
    document.title = `🌞 ${dateString} - 每日计划与总结`;
}

// Markdown编辑器功能
let currentEditorMode = 'edit';

function switchEditorTab(mode) {
    currentEditorMode = mode;
    const editTab = document.querySelector('.editor-tab:first-child');
    const previewTab = document.querySelector('.editor-tab:last-child');
    const textarea = document.getElementById('daily-thoughts');
    const preview = document.getElementById('markdown-preview');
    
    if (mode === 'edit') {
        editTab.classList.add('active');
        previewTab.classList.remove('active');
        textarea.style.display = 'block';
        preview.style.display = 'none';
    } else {
        editTab.classList.remove('active');
        previewTab.classList.add('active');
        textarea.style.display = 'none';
        preview.style.display = 'block';
        
        // 更新预览内容
        const markdownText = textarea.value;
        preview.innerHTML = parseMarkdown(markdownText);
    }
}

function parseMarkdown(text) {
    if (!text) return '<p class="empty-placeholder">还没有内容，开始记录您的每日思考吧...</p>';
    
    // 简单的Markdown解析器
    let html = text;
    
    // 标题
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // 粗体和斜体
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // 代码
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // 引用
    html = html.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');
    
    // 列表
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^(\d+)\. (.*$)/gim, '<li>$1. $2</li>');
    
    // 包装列表项
    html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
    
    // 段落
    html = html.split('\n\n').map(paragraph => {
        if (paragraph.trim() && 
            !paragraph.includes('<h') && 
            !paragraph.includes('<li>') && 
            !paragraph.includes('<blockquote>') &&
            !paragraph.includes('<ul>')) {
            return `<p>${paragraph.trim()}</p>`;
        }
        return paragraph;
    }).join('\n\n');
    
    // 换行
    html = html.replace(/\n/g, '<br>');
    
    return html;
}

// 自动保存每日思考
function setupDailyThoughtsAutoSave() {
    const textarea = document.getElementById('daily-thoughts');
    if (textarea) {
        textarea.addEventListener('input', () => {
            clearTimeout(window.thoughtsTimeout);
            window.thoughtsTimeout = setTimeout(() => {
                saveDailyThoughts();
            }, 1000);
        });
        
        textarea.addEventListener('blur', () => {
            saveDailyThoughts();
        });
        
        // 加载已保存的内容
        loadDailyThoughts();
    }
}

function saveDailyThoughts() {
    const textarea = document.getElementById('daily-thoughts');
    const today = new Date().toISOString().split('T')[0];
    const thoughts = textarea.value;
    
    localStorage.setItem(`daily-thoughts-${today}`, thoughts);
}

function loadDailyThoughts() {
    const textarea = document.getElementById('daily-thoughts');
    const today = new Date().toISOString().split('T')[0];
    const savedThoughts = localStorage.getItem(`daily-thoughts-${today}`);
    
    if (savedThoughts) {
        textarea.value = savedThoughts;
    }
}

// 在DOMContentLoaded事件中初始化每日思考功能
document.addEventListener('DOMContentLoaded', () => {
    // 延迟执行，确保DOM完全加载
    setTimeout(() => {
        setupDailyThoughtsAutoSave();
        loadSettings();
        setupSettingsEventListeners();
        loadRecordTree();
    }, 100);
});

// 侧边栏功能
let isSidebarOpen = false;
let recordTree = {};

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    isSidebarOpen = !isSidebarOpen;
    
    if (isSidebarOpen) {
        sidebar.classList.add('active');
        loadRecordTree();
    } else {
        sidebar.classList.remove('active');
    }
}

function loadRecordTree() {
    // 从localStorage和服务器文件系统加载所有历史记录
    const allRecords = getAllStoredRecords();
    
    // 同时尝试从服务器加载历史文件
    loadHistoryFromServer().then(serverRecords => {
        // 合并本地和服务器记录
        const mergedRecords = mergeRecords(allRecords, serverRecords);
        recordTree = buildTreeStructure(mergedRecords);
        renderRecordTree();
    }).catch(error => {
        console.log('从服务器加载历史记录失败，使用本地记录:', error);
        recordTree = buildTreeStructure(allRecords);
        renderRecordTree();
    });
}

function loadHistoryFromServer() {
    return fetch('/api/history-files')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log(`📂 发现 ${data.files.length} 个历史文件，保存目录: ${data.saveDirectory}`);
                
                // 为服务器文件创建基本记录结构，用于显示在侧边栏
                return data.files.map(file => ({
                    date: file.date,
                    data: {
                        // 为了在侧边栏显示，创建基本的数据结构
                        plans: [], // 空数组，实际数据在点击时加载
                        dateInfo: {
                            year: parseInt(file.date.split('-')[0]),
                            month: parseInt(file.date.split('-')[1]),
                            day: parseInt(file.date.split('-')[2]),
                            weekdayName: new Date(file.date).toLocaleDateString('zh-CN', { weekday: 'long' })
                        }
                    },
                    source: 'server',
                    filename: file.filename,
                    path: file.path,
                    size: file.size,
                    modified: new Date(file.modified * 1000),
                    lazyLoad: true // 标记为延迟加载
                }));
            } else {
                throw new Error(data.message || '获取历史文件失败');
            }
        });
}

function mergeRecords(localRecords, serverRecords) {
    const merged = new Map();
    
    // 添加本地记录
    localRecords.forEach(record => {
        merged.set(record.date, {
            ...record,
            source: 'local'
        });
    });
    
    // 添加服务器记录（优先级更高，因为可能更新）
    serverRecords.forEach(record => {
        const existing = merged.get(record.date);
        if (!existing || (existing.source === 'local' && record.modified > new Date(existing.data?.savedAt || 0))) {
            merged.set(record.date, record);
        }
    });
    
    return Array.from(merged.values());
}

function getAllStoredRecords() {
    const records = [];
    
    // 遍历localStorage中的所有项目
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('daily-record-')) {
            try {
                const record = JSON.parse(localStorage.getItem(key));
                records.push({
                    date: key.replace('daily-record-', ''),
                    data: record
                });
            } catch (e) {
                console.error('解析记录失败:', key, e);
            }
        }
    }
    
    return records.sort((a, b) => new Date(b.date) - new Date(a.date));
}

function buildTreeStructure(records) {
    const tree = {};
    
    records.forEach(record => {
        let year, month, day;
        
        // 优先使用记录中的dateInfo，否则从date字符串解析
        if (record.data.dateInfo) {
            year = record.data.dateInfo.year;
            month = record.data.dateInfo.month;
            day = record.data.dateInfo.day;
        } else {
            // 兼容旧格式，从date字符串解析
            const date = new Date(record.date);
            if (isNaN(date.getTime())) {
                console.warn(`无效的日期格式: ${record.date}`);
                return; // 跳过无效记录
            }
            year = date.getFullYear();
            month = date.getMonth() + 1;
            day = date.getDate();
        }
        
        // 验证年月日信息
        if (!year || !month || !day) {
            console.warn(`记录缺少完整的年月日信息: ${record.date}`);
            return; // 跳过不完整的记录
        }
        
        // 初始化年份
        if (!tree[year]) {
            tree[year] = {
                count: 0,
                months: {}
            };
        }
        
        // 初始化月份
        if (!tree[year].months[month]) {
            tree[year].months[month] = {
                count: 0,
                days: {}
            };
        }
        
        // 添加日期
        tree[year].months[month].days[day] = {
            date: record.date,
            data: record.data,
            source: record.source || 'local',
            filename: record.filename || null,
            path: record.path || null,
            size: record.size || null,
            modified: record.modified || null,
            lazyLoad: record.lazyLoad || false,
            dateInfo: (record.data && record.data.dateInfo) || {
                year: year,
                month: month,
                day: day,
                weekdayName: new Date(record.date).toLocaleDateString('zh-CN', { weekday: 'long' })
            },
            planCount: (record.data && record.data.plans) ? record.data.plans.length : (record.lazyLoad ? '?' : 0),
            completedCount: (record.data && record.data.plans) ? record.data.plans.filter(p => p.completed).length : (record.lazyLoad ? '?' : 0)
        };
        
        // 更新计数
        tree[year].count++;
        tree[year].months[month].count++;
    });
    
    return tree;
}

function renderRecordTree() {
    const treeContainer = document.getElementById('record-tree');
    
    if (Object.keys(recordTree).length === 0) {
        treeContainer.innerHTML = `
            <div class="tree-loading">
                <p>暂无历史记录</p>
                <small>保存数据后将显示记录结构</small>
            </div>
        `;
        return;
    }
    
    let treeHTML = '';
    
    // 按年份降序排列
    const years = Object.keys(recordTree).sort((a, b) => b - a);
    
    years.forEach(year => {
        const yearData = recordTree[year];
        treeHTML += `
            <div class="tree-node tree-level-1">
                <div class="tree-item" onclick="toggleTreeNode(this)">
                    <span class="tree-icon">▶</span>
                    <span class="tree-label">${year}年</span>
                    <span class="tree-count">${yearData.count}</span>
                </div>
                <div class="tree-children">
        `;
        
        // 按月份降序排列
        const months = Object.keys(yearData.months).sort((a, b) => b - a);
        
        months.forEach(month => {
            const monthData = yearData.months[month];
            const monthName = `${month}月`;
            
            treeHTML += `
                <div class="tree-node tree-level-2">
                    <div class="tree-item" onclick="toggleTreeNode(this)">
                        <span class="tree-icon">▶</span>
                        <span class="tree-label">${monthName}</span>
                        <span class="tree-count">${monthData.count}</span>
                    </div>
                    <div class="tree-children">
            `;
            
            // 按日期降序排列
            const days = Object.keys(monthData.days).sort((a, b) => b - a);
            
            days.forEach(day => {
                const dayData = monthData.days[day];
                const completionRate = dayData.planCount > 0 ? 
                    Math.round((dayData.completedCount / dayData.planCount) * 100) : 0;
                
                // 构建日期显示标签
                const weekdayName = dayData.dateInfo ? dayData.dateInfo.weekdayName : '';
                const dayLabel = weekdayName ? `${day}日 (${weekdayName})` : `${day}日`;
                
                // 来源图标和提示信息
                const sourceIcon = dayData.source === 'server' ? '🗄️' : '💾';
                const sourceText = dayData.source === 'server' ? '服务器文件' : '本地存储';
                const fileInfo = dayData.filename ? `\n文件: ${dayData.filename}` : '';
                const sizeInfo = dayData.size ? `\n大小: ${(dayData.size / 1024).toFixed(1)}KB` : '';
                const tooltipText = `点击加载 ${dayData.date} 的记录\n来源: ${sourceText}${fileInfo}${sizeInfo}\n完成率: ${completionRate}% (${dayData.completedCount}/${dayData.planCount})`;
                
                treeHTML += `
                    <div class="tree-node tree-level-3">
                        <div class="tree-item record-item-${dayData.source}" onclick="loadRecord('${dayData.date}')" data-date="${dayData.date}" title="${tooltipText}">
                            <span class="tree-icon">${sourceIcon}</span>
                            <span class="tree-label">${dayLabel}</span>
                            <span class="tree-count" title="完成率: ${completionRate}% (${dayData.completedCount}/${dayData.planCount})">${dayData.completedCount}/${dayData.planCount}</span>
                        </div>
                    </div>
                `;
            });
            
            treeHTML += `
                    </div>
                </div>
            `;
        });
        
        treeHTML += `
                </div>
            </div>
        `;
    });
    
    treeContainer.innerHTML = treeHTML;
}

function toggleTreeNode(element) {
    const icon = element.querySelector('.tree-icon');
    const children = element.parentNode.querySelector('.tree-children');
    
    if (children) {
        const isExpanded = children.classList.contains('expanded');
        
        if (isExpanded) {
            children.classList.remove('expanded');
            icon.classList.remove('expanded');
            icon.textContent = '▶';
        } else {
            children.classList.add('expanded');
            icon.classList.add('expanded');
            icon.textContent = '▼';
        }
    }
}

function loadRecord(date) {
    try {
        // 首先检查记录树中是否有这个日期的信息
        const dayData = findRecordInTree(date);
        
        if (dayData && dayData.source === 'server' && dayData.lazyLoad) {
            // 这是一个服务器文件，需要从服务器加载
            loadRecordFromServer(date);
        } else {
            // 尝试从localStorage加载
            let recordData = localStorage.getItem(`daily-record-${date}`);
            
            if (recordData) {
                // 从本地加载
                loadRecordFromData(date, JSON.parse(recordData), 'local');
            } else {
                // 本地没有，尝试从服务器加载
                loadRecordFromServer(date);
            }
        }
    } catch (error) {
        console.error('加载记录时出错:', error);
        planner.showMessage('❌ 加载记录失败', 'error');
    }
}

function findRecordInTree(date) {
    const [year, month, day] = date.split('-');
    const yearNum = parseInt(year);
    const monthNum = parseInt(month);
    const dayNum = parseInt(day);
    
    if (recordTree[yearNum] && 
        recordTree[yearNum].months[monthNum] && 
        recordTree[yearNum].months[monthNum].days[dayNum]) {
        return recordTree[yearNum].months[monthNum].days[dayNum];
    }
    
    return null;
}

function loadRecordFromServer(date) {
    // 显示加载提示
    planner.showMessage('📄 正在从服务器加载记录...', 'info');
    
    fetch(`/api/load-record/${date}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                loadRecordFromData(date, data.data, 'server', data.filePath);
            } else {
                planner.showMessage(`❌ ${data.message}`, 'error');
            }
        })
        .catch(error => {
            console.error('从服务器加载记录失败:', error);
            planner.showMessage('❌ 从服务器加载记录失败', 'error');
        });
}

function loadRecordFromData(date, record, source = 'local', filePath = null) {
    try {
        // 验证记录的完整性，特别是日期信息
        if (!validateRecordIntegrity(record, date)) {
            return;
        }
        
        // 显示记录的详细信息
        const dateInfo = record.dateInfo;
        const displayDate = dateInfo ? 
            `${dateInfo.fullDateString || date}` : date;
        
        const sourceText = source === 'server' ? '服务器文件' : '本地存储';
        const pathText = filePath ? `\n📁 路径: ${filePath}` : '';
        
        // 确认是否要加载历史记录
        if (confirm(`🔄 确定要加载以下记录吗？\n\n🌞 ${displayDate}\n📊 来源: ${sourceText}${pathText}\n📋 计划: ${record.plans?.length || 0} 项\n✅ 完成: ${record.statistics?.completedPlans || 0} 项\n\n⚠️ 当前未保存的内容将会丢失。`)) {
            // 数据迁移：确保所有计划都有正确的字段名
            const migratedPlans = (record.plans || []).map(plan => {
                if (plan.start_time && !plan.startTime) {
                    plan.startTime = plan.start_time;
                    delete plan.start_time; // 删除旧字段
                }
                return plan;
            });
            
            // 加载计划数据
            planner.plans = migratedPlans;
            planner.updatePlanTable();
            
            // 加载反思数据
            if (record.reflection) {
                planner.loadReflectionSection('progress', record.reflection.progress || []);
                planner.loadReflectionSection('improvement', record.reflection.improvements || []);
                planner.loadReflectionSection('gratitude', record.reflection.gratitude || []);
                
                // 加载每日思考
                const thoughtsTextarea = document.getElementById('daily-thoughts');
                if (thoughtsTextarea) {
                    thoughtsTextarea.value = record.reflection.dailyThoughts || '';
                }
            }
            
            // 加载完成情况数据
            if (record.completionDetails) {
                // 先保存到localStorage用于后续加载
                localStorage.setItem(`completion_data_${date}`, JSON.stringify(record.completionDetails));
            }
            
            // 更新完成情况统计和表格
            planner.updateCompletionStats();
            
            // 高亮选中的记录
            document.querySelectorAll('.tree-level-3 .tree-item').forEach(item => {
                item.classList.remove('active');
            });
            const targetItem = document.querySelector(`[data-date="${date}"]`);
            if (targetItem) {
                targetItem.classList.add('active');
            }
            
            const successMsg = source === 'server' ? 
                `📄 已从服务器加载 ${displayDate} 的记录` : 
                `🌞 已加载 ${displayDate} 的记录`;
            planner.showMessage(successMsg, 'success');
            
            // 可选：关闭侧边栏
            toggleSidebar();
        }
    } catch (e) {
        console.error('加载记录失败:', e);
        planner.showMessage('❌ 加载记录失败：数据格式错误', 'error');
    }
}

// 验证记录完整性
function validateRecordIntegrity(record, expectedDate) {
    // 检查基本结构
    if (!record || typeof record !== 'object') {
        planner.showMessage('❌ 记录数据格式错误', 'error');
        return false;
    }
    
    // 检查日期匹配
    if (record.date && record.date !== expectedDate) {
        planner.showMessage('❌ 记录日期不匹配', 'error');
        return false;
    }
    
    // 检查是否包含必要的日期信息
    if (record.dateInfo) {
        const { year, month, day } = record.dateInfo;
        if (!year || !month || !day) {
            planner.showMessage('❌ 记录缺少完整的年月日信息', 'error');
            return false;
        }
        
        // 验证日期信息的合理性
        if (year < 2020 || year > new Date().getFullYear() + 1) {
            planner.showMessage('❌ 记录中的年份信息异常', 'error');
            return false;
        }
        
        if (month < 1 || month > 12) {
            planner.showMessage('❌ 记录中的月份信息异常', 'error');
            return false;
        }
        
        if (day < 1 || day > 31) {
            planner.showMessage('❌ 记录中的日期信息异常', 'error');
            return false;
        }
    }
    
    // 检查数据结构完整性
    if (!record.plans || !Array.isArray(record.plans)) {
        console.warn('记录中缺少计划数据，使用空数组');
        record.plans = [];
    }
    
    if (!record.reflection || typeof record.reflection !== 'object') {
        console.warn('记录中缺少反思数据，使用空对象');
        record.reflection = {
            progress: [],
            improvements: [],
            gratitude: [],
            dailyThoughts: ''
        };
    }
    
    return true;
}

// 更新保存功能以刷新树状结构
function updateRecordTreeAfterSave() {
    if (isSidebarOpen) {
        setTimeout(() => {
            loadRecordTree();
        }, 500);
    }
}

// 设置面板功能
let isSettingsPanelOpen = false;
let currentSettings = {
    saveDirectory: './downloads',
    autoSave: true,
    fileNaming: '每日记录_{date}',
    customNaming: '',
    // AI功能设置
    aiEnabled: false,
    openrouterApiKey: '',
    openrouterBaseUrl: 'https://openrouter.ai/api/v1',
    openrouterModel: 'deepseek/deepseek-r1-0528-qwen3-8b:free'
};

function toggleSettings() {
    const panel = document.getElementById('settings-panel');
    const overlay = document.getElementById('settings-overlay');
    
    isSettingsPanelOpen = !isSettingsPanelOpen;
    
    if (isSettingsPanelOpen) {
        panel.classList.add('active');
        overlay.classList.add('active');
        loadSettingsToUI();
    } else {
        panel.classList.remove('active');
        overlay.classList.remove('active');
    }
}

function setupSettingsEventListeners() {
    // 文件命名格式选择
    const fileNamingSelect = document.getElementById('file-naming');
    const customNamingInput = document.getElementById('custom-naming');
    
    fileNamingSelect.addEventListener('change', (e) => {
        if (e.target.value === 'custom') {
            customNamingInput.style.display = 'block';
            customNamingInput.focus();
        } else {
            customNamingInput.style.display = 'none';
        }
    });
    
    // AI模型选择
    const modelSelect = document.getElementById('openrouter-model');
    const customModelInput = document.getElementById('custom-model');
    
    modelSelect.addEventListener('change', (e) => {
        if (e.target.value === 'custom') {
            customModelInput.style.display = 'block';
            customModelInput.focus();
        } else {
            customModelInput.style.display = 'none';
        }
    });
    
    // ESC键关闭设置面板
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isSettingsPanelOpen) {
            toggleSettings();
        }
    });
}

function loadSettings() {
    try {
        // 从localStorage加载设置
        const savedSettings = localStorage.getItem('dailyPlannerSettings');
        if (savedSettings) {
            currentSettings = { ...currentSettings, ...JSON.parse(savedSettings) };
        }
        
        // 同时尝试从服务器加载最新设置
        loadSettingsFromServer();
    } catch (e) {
        console.error('加载设置失败:', e);
    }
}

function loadSettingsFromServer() {
    // 尝试从服务器获取最新的XML设置
    // 这里我们可以通过读取XML文件的内容来同步设置
    // 由于安全限制，直接读取文件可能不可行，但可以通过API获取
    fetch('/settings.xml')
        .then(response => response.text())
        .then(xmlText => {
            try {
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
                
                const saveDirectory = xmlDoc.querySelector('saveDirectory')?.textContent;
                const autoSave = xmlDoc.querySelector('autoSave')?.textContent === 'true';
                const fileNaming = xmlDoc.querySelector('fileNaming')?.textContent;
                
                // 读取AI设置
                const aiEnabled = xmlDoc.querySelector('ai enabled')?.textContent === 'true';
                const openrouterApiKey = xmlDoc.querySelector('ai openrouterApiKey')?.textContent;
                const openrouterBaseUrl = xmlDoc.querySelector('ai openrouterBaseUrl')?.textContent;
                const openrouterModel = xmlDoc.querySelector('ai openrouterModel')?.textContent;
                
                if (saveDirectory || fileNaming || aiEnabled !== undefined) {
                    const serverSettings = {
                        saveDirectory: saveDirectory || currentSettings.saveDirectory,
                        autoSave: autoSave !== undefined ? autoSave : currentSettings.autoSave,
                        fileNaming: fileNaming || currentSettings.fileNaming,
                        // AI设置
                        aiEnabled: aiEnabled !== undefined ? aiEnabled : currentSettings.aiEnabled,
                        openrouterApiKey: openrouterApiKey || currentSettings.openrouterApiKey,
                        openrouterBaseUrl: openrouterBaseUrl || currentSettings.openrouterBaseUrl,
                        openrouterModel: openrouterModel || currentSettings.openrouterModel
                    };
                    
                    // 合并服务器设置
                    currentSettings = { ...currentSettings, ...serverSettings };
                    
                    // 也更新localStorage
                    localStorage.setItem('dailyPlannerSettings', JSON.stringify(currentSettings));
                    
                    console.log('✅ 已从服务器同步设置');
                }
            } catch (e) {
                console.log('ℹ️ 无法解析XML设置文件，使用本地设置');
            }
        })
        .catch(error => {
            console.log('ℹ️ 无法从服务器加载设置，使用本地设置');
        });
}

function loadSettingsToUI() {
    document.getElementById('save-directory').value = currentSettings.saveDirectory || './downloads';
    document.getElementById('auto-save').checked = currentSettings.autoSave !== false;
    document.getElementById('file-naming').value = currentSettings.fileNaming || '每日记录_{date}';
    
    // 加载AI设置
    document.getElementById('ai-enabled').checked = currentSettings.aiEnabled || false;
    document.getElementById('openrouter-api-key').value = currentSettings.openrouterApiKey || '';
    document.getElementById('openrouter-base-url').value = currentSettings.openrouterBaseUrl || 'https://openrouter.ai/api/v1';
    document.getElementById('openrouter-model').value = currentSettings.openrouterModel || 'deepseek/deepseek-r1-0528-qwen3-8b:free';
    
    // 处理自定义模型
    const modelSelect = document.getElementById('openrouter-model');
    const customModelInput = document.getElementById('custom-model');
    const predefinedModels = [
        'deepseek/deepseek-r1-0528-qwen3-8b:free',
        'openai/gpt-3.5-turbo',
        'openai/gpt-4o-mini',
        'anthropic/claude-3-haiku',
        'google/gemini-flash-1.5',
        'meta-llama/llama-3.1-8b-instruct:free',
        'microsoft/wizardlm-2-8x22b'
    ];
    
    if (!predefinedModels.includes(currentSettings.openrouterModel)) {
        modelSelect.value = 'custom';
        customModelInput.style.display = 'block';
        customModelInput.value = currentSettings.openrouterModel || '';
    }
    
    if (currentSettings.fileNaming === 'custom' || 
        !['每日记录_{date}', 'daily_record_{date}', '{date}_记录'].includes(currentSettings.fileNaming)) {
        document.getElementById('file-naming').value = 'custom';
        document.getElementById('custom-naming').style.display = 'block';
        document.getElementById('custom-naming').value = currentSettings.customNaming || currentSettings.fileNaming;
    }
}

function saveSettings() {
    const saveDirectory = document.getElementById('save-directory').value.trim();
    const autoSave = document.getElementById('auto-save').checked;
    const fileNaming = document.getElementById('file-naming').value;
    const customNaming = document.getElementById('custom-naming').value.trim();
    
    // AI设置
    const aiEnabled = document.getElementById('ai-enabled').checked;
    const openrouterApiKey = document.getElementById('openrouter-api-key').value.trim();
    const openrouterBaseUrl = document.getElementById('openrouter-base-url').value.trim();
    const openrouterModel = document.getElementById('openrouter-model').value;
    const customModel = document.getElementById('custom-model').value.trim();
    
    // 验证保存路径
    if (!saveDirectory) {
        alert('⚠️ 请设置保存路径');
        return;
    }
    
    // 验证API设置
    if (aiEnabled && !openrouterApiKey) {
        alert('⚠️ 启用AI功能时必须提供API密钥');
        return;
    }
    
    if (aiEnabled && !openrouterBaseUrl) {
        alert('⚠️ 启用AI功能时必须提供API服务地址');
        return;
    }
    
    // 确定最终的模型名称
    const finalModel = openrouterModel === 'custom' ? customModel : openrouterModel;
    
    if (aiEnabled && !finalModel) {
        alert('⚠️ 启用AI功能时必须选择或输入模型名称');
        return;
    }
    
    // 构建设置对象
    const newSettings = {
        saveDirectory: saveDirectory,
        autoSave: autoSave,
        fileNaming: fileNaming === 'custom' ? customNaming : fileNaming,
        customNaming: customNaming,
        // AI设置
        aiEnabled: aiEnabled,
        openrouterApiKey: openrouterApiKey,
        openrouterBaseUrl: openrouterBaseUrl,
        openrouterModel: finalModel,
        updatedAt: new Date().toISOString()
    };
    
    // 保存到localStorage
    localStorage.setItem('dailyPlannerSettings', JSON.stringify(newSettings));
    currentSettings = newSettings;
    
    // 发送到服务器保存XML文件
    saveSettingsToServer(newSettings);
    
    // 显示成功消息
    showSettingsMessage('保存成功！', 'success');
    
    // 2秒后关闭面板
    setTimeout(() => {
        toggleSettings();
    }, 1500);
}

function saveSettingsToServer(settings) {
    // 发送设置到服务器
    fetch('/api/save-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('✅ 设置已保存到XML文件');
        } else {
            console.error('❌ 保存XML文件失败:', data.message);
            showSettingsMessage('⚠️ XML文件保存失败，但本地设置已保存', 'warning');
        }
    })
    .catch(error => {
        console.error('❌ 网络错误:', error);
        showSettingsMessage('⚠️ 网络错误，但本地设置已保存', 'warning');
    });
}

function resetSettings() {
    if (!confirm('🔄 确定要重置所有设置为默认值吗？')) {
        return;
    }
    
    const defaultSettings = {
        saveDirectory: './downloads',
        autoSave: true,
        fileNaming: '每日记录_{date}',
        customNaming: '',
        // AI默认设置
        aiEnabled: false,
        openrouterApiKey: '',
        openrouterBaseUrl: 'https://openrouter.ai/api/v1',
        openrouterModel: 'deepseek/deepseek-r1-0528-qwen3-8b:free'
    };
    
    localStorage.setItem('dailyPlannerSettings', JSON.stringify(defaultSettings));
    currentSettings = defaultSettings;
    
    loadSettingsToUI();
    showSettingsMessage('🔄 设置已重置为默认值', 'info');
}

function toggleApiKeyVisibility() {
    const apiKeyInput = document.getElementById('openrouter-api-key');
    const toggleBtn = document.querySelector('.toggle-btn');
    
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
        toggleBtn.textContent = '🙈';
        toggleBtn.title = '隐藏API密钥';
    } else {
        apiKeyInput.type = 'password';
        toggleBtn.textContent = '👁️';
        toggleBtn.title = '显示API密钥';
    }
}

function testAiConnection() {
    const aiEnabled = document.getElementById('ai-enabled').checked;
    const apiKey = document.getElementById('openrouter-api-key').value.trim();
    const baseUrl = document.getElementById('openrouter-base-url').value.trim();
    const modelSelect = document.getElementById('openrouter-model').value;
    const customModel = document.getElementById('custom-model').value.trim();
    
    if (!aiEnabled) {
        showSettingsMessage('⚠️ 请先启用AI功能', 'warning');
        return;
    }
    
    if (!apiKey) {
        showSettingsMessage('⚠️ 请输入API密钥', 'warning');
        return;
    }
    
    if (!baseUrl) {
        showSettingsMessage('⚠️ 请输入API服务地址', 'warning');
        return;
    }
    
    const finalModel = modelSelect === 'custom' ? customModel : modelSelect;
    if (!finalModel) {
        showSettingsMessage('⚠️ 请选择或输入模型名称', 'warning');
        return;
    }
    
    // 显示测试中状态
    showSettingsMessage('🧪 正在测试AI连接...', 'info');
    
    // 发送测试请求到后端
    fetch('/api/test-ai-connection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            apiKey: apiKey,
            baseUrl: baseUrl,
            model: finalModel
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showSettingsMessage('✅ AI连接测试成功！', 'success');
        } else {
            showSettingsMessage(`❌ AI连接测试失败: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        console.error('测试AI连接时发生错误:', error);
        showSettingsMessage('❌ 网络错误，无法测试AI连接', 'error');
    });
}

function selectDirectory() {
    // 由于浏览器安全限制，无法直接打开文件夹选择器
    // 提供一些常用路径建议
    const commonPaths = [
        './downloads',
        './Documents/DailyRecords',
        './Desktop/每日记录',
        '~/Downloads',
        '~/Documents'
    ];
    
    const pathList = commonPaths.map(path => `• ${path}`).join('\n');
    const userInput = prompt(`📁 常用路径参考：\n\n${pathList}\n\n请输入您希望的保存路径：`, currentSettings.saveDirectory);
    
    if (userInput !== null) {
        document.getElementById('save-directory').value = userInput.trim();
    }
}

function updateSettingsXML(settings) {
    // 由于浏览器限制，无法直接写入文件系统
    // 这里我们创建一个XML内容并提供下载
    const xmlContent = `<?xml version="1.0" encoding="UTF-8"?>
<settings>
    <general>
        <saveDirectory>${settings.saveDirectory}</saveDirectory>
        <autoSave>${settings.autoSave}</autoSave>
        <dateFormat>YYYY-MM-DD</dateFormat>
    </general>
    <export>
        <includeStatistics>true</includeStatistics>
        <includeTimestamp>true</includeTimestamp>
        <fileNaming>${settings.fileNaming}</fileNaming>
    </export>
    <ui>
        <theme>light</theme>
        <language>zh-CN</language>
    </ui>
    <lastUpdated>${settings.updatedAt}</lastUpdated>
</settings>`;
    
    // 可选：自动下载更新的XML文件
    // const blob = new Blob([xmlContent], { type: 'application/xml' });
    // const url = URL.createObjectURL(blob);
    // const a = document.createElement('a');
    // a.href = url;
    // a.download = 'settings.xml';
    // a.click();
    // URL.revokeObjectURL(url);
}

function showSettingsMessage(message, type = 'info') {
    // 在设置面板中显示消息
    const existingMessage = document.querySelector('.settings-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `settings-message settings-message-${type}`;
    messageDiv.style.cssText = `
        position: absolute;
        top: 70px;
        left: 1.5rem;
        right: 1.5rem;
        padding: 0.75rem;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        z-index: 10;
        animation: slideDown 0.3s ease;
    `;
    
    switch(type) {
        case 'success':
            messageDiv.style.background = '#d4edda';
            messageDiv.style.color = '#155724';
            messageDiv.style.border = '1px solid #c3e6cb';
            break;
        case 'error':
            messageDiv.style.background = '#f8d7da';
            messageDiv.style.color = '#721c24';
            messageDiv.style.border = '1px solid #f5c6cb';
            break;
        case 'warning':
            messageDiv.style.background = '#fff3cd';
            messageDiv.style.color = '#856404';
            messageDiv.style.border = '1px solid #ffeaa7';
            break;
        default:
            messageDiv.style.background = '#e2e3e5';
            messageDiv.style.color = '#383d41';
            messageDiv.style.border = '1px solid #d6d8db';
    }
    
    messageDiv.textContent = message;
    document.getElementById('settings-panel').appendChild(messageDiv);
    
    // 3秒后自动消失
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 3000);
}

// 更新保存功能以使用设置的路径和命名格式
function getFormattedFileName(date) {
    const template = currentSettings.fileNaming || '每日记录_{date}';
    return template.replace('{date}', date);
}

// 页面卸载时的清理
window.addEventListener('beforeunload', () => {
    // 清理内存中的数据
    if (window.planner) {
        window.planner = null;
    }
});

// 页面隐藏时清理
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // 页面被隐藏时清理临时数据
        console.log('📄 页面被隐藏，清理临时数据');
    } else {
        // 页面重新可见时检查缓存
        console.log('👀 页面重新可见，检查缓存状态');
        const today = new Date().toISOString().split('T')[0];
        const lastClearDate = localStorage.getItem('lastCacheClearDate');
        
        if (!lastClearDate || lastClearDate !== today) {
            clearPageCache();
            // 重新初始化数据
            if (window.planner) {
                window.planner.updateCompletionStats();
            }
        }
    }
});

// 强制禁用某些浏览器缓存
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', event => {
        if (event.data && event.data.type === 'CACHE_UPDATED') {
            console.log('🔄 Service Worker 缓存已更新');
            // 可以在这里添加页面刷新逻辑
            // location.reload();
        }
    });
}

// 添加键盘快捷键强制刷新缓存
document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+R 或 Cmd+Shift+R 强制清理缓存并刷新
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'R') {
        e.preventDefault();
        console.log('⚡ 强制清理缓存并刷新');
        
        // 询问用户是否要清理今日数据
        const clearToday = confirm('是否要清理今日的所有数据？\n\n点击"确定"将清理所有数据（包括今日计划）\n点击"取消"将保留今日数据，只清理过期数据');
        
        if (clearToday) {
            // 清理所有localStorage数据（除了重要设置）
            const keysToKeep = ['settings', 'user-preferences'];
            const allKeys = Object.keys(localStorage);
            
            allKeys.forEach(key => {
                if (!keysToKeep.some(keepKey => key.includes(keepKey))) {
                    localStorage.removeItem(key);
                }
            });
        } else {
            // 只清理过期数据，保留今日数据
            clearPageCache(false);
        }
        
        // 强制刷新页面
        location.reload(true);
    }
});

// 添加开发者调试功能
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🛠️ 开发模式：添加调试功能');
    
    // 添加全局清理函数供调试使用
    window.forceClearCache = () => {
        clearPageCache(false);
        console.log('🧹 手动清理缓存完成（保留今日数据）');
    };
    
    window.forceClearAll = () => {
        clearPageCache(true);
        console.log('🧹 手动清理所有缓存完成（包括今日数据）');
    };
    
    // 添加全局数据检查函数
    window.checkLocalStorage = () => {
        console.log('📊 当前 localStorage 数据：');
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key);
            console.log(`${key}:`, value.length > 100 ? `${value.substring(0, 100)}...` : value);
        }
    };
    
    // 检查特定的数据项
    window.checkPlanData = () => {
        console.log('📋 计划数据检查：');
        console.log('dailyPlannerData:', localStorage.getItem('dailyPlannerData'));
        console.log('plans:', localStorage.getItem('plans'));
        
        const today = new Date().toISOString().split('T')[0];
        console.log(`daily-record-${today}:`, localStorage.getItem(`daily-record-${today}`));
    };
    
    console.log('💡 调试提示：');
    console.log('- 使用 forceClearCache() 清理缓存（保留今日数据）');
    console.log('- 使用 forceClearAll() 清理所有缓存（包括今日数据）');
    console.log('- 使用 checkLocalStorage() 查看当前存储数据');
    console.log('- 使用 checkPlanData() 查看计划相关数据');
    console.log('- 使用 Ctrl+Shift+R 强制清理缓存并刷新（会询问是否清理今日数据）');
}
