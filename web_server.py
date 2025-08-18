#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的HTTP服务器，用于运行每日计划与总结Web应用程序
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs
from pathlib import Path


class SettingsHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP处理器，支持设置保存功能"""
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/save-settings':
            self.handle_save_settings()
        elif self.path == '/api/save-daily-record':
            self.handle_save_daily_record()
        elif self.path == '/api/test-ai-connection':
            self.handle_test_ai_connection()
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/api/history-files':
            self.handle_get_history_files()
        elif self.path.startswith('/api/load-record/'):
            date = self.path.split('/')[-1]
            self.handle_load_record(date)
        else:
            # 默认的静态文件处理
            super().do_GET()
    
    def handle_save_settings(self):
        """处理保存设置的请求"""
        try:
            # 读取POST数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            settings_data = json.loads(post_data.decode('utf-8'))
            
            # 更新XML文件
            self.update_settings_xml(settings_data)
            
            # 返回成功响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"status": "success", "message": "设置保存成功！"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            # 返回错误响应
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"status": "error", "message": f"保存设置失败: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_save_daily_record(self):
        """处理保存日记记录的请求"""
        try:
            # 读取POST数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            record_data = json.loads(post_data.decode('utf-8'))
            
            # 获取当前设置
            settings = self.load_settings()
            save_directory = settings.get('saveDirectory', './downloads')
            file_naming = settings.get('fileNaming', '每日记录_{date}')
            
            # 创建保存目录
            save_path = Path(save_directory)
            save_path.mkdir(parents=True, exist_ok=True)
            
            # 生成文件名
            date = record_data.get('date', '')
            file_name = file_naming.replace('{date}', date)
            file_path = save_path / f"{file_name}.json"
            
            # 保存文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(record_data, f, ensure_ascii=False, indent=2)
            
            # 返回成功响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "success", 
                "message": f"文件已保存到: {file_path}",
                "filePath": str(file_path)
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            # 返回错误响应
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"status": "error", "message": f"保存日记失败: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_test_ai_connection(self):
        """处理测试AI连接的请求"""
        try:
            # 读取POST数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            test_data = json.loads(post_data.decode('utf-8'))
            api_key = test_data.get('apiKey', '')
            base_url = test_data.get('baseUrl', 'https://openrouter.ai/api/v1')
            model = test_data.get('model', 'deepseek/deepseek-r1-0528-qwen3-8b:free')
            
            # 测试AI连接
            success, message = self.test_openrouter_connection(api_key, base_url, model)
            
            # 返回响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if success:
                response = {"status": "success", "message": message}
            else:
                response = {"status": "error", "message": message}
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            # 返回错误响应
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"status": "error", "message": f"测试连接失败: {str(e)}"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def test_openrouter_connection(self, api_key, base_url, model=None):
        """测试OpenRouter API连接"""
        try:
            from openai import OpenAI
            
            # 如果没有提供模型，使用默认模型
            if not model:
                model = "deepseek/deepseek-r1-0528-qwen3-8b:free"
            
            # 创建客户端
            client = OpenAI(
                base_url=base_url,
                api_key=api_key,
            )
            
            # 发送简单的测试请求
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://quirklog.app",
                    "X-Title": "QuirkLog Daily Planner",
                },
                model=model,  # 使用指定的模型
                messages=[
                    {
                        "role": "user",
                        "content": "Hello! This is a connection test."
                    }
                ],
                max_tokens=10  # 限制token数量，减少费用
            )
            
            if completion.choices and completion.choices[0].message:
                return True, f"API连接测试成功！使用模型: {model}"
            else:
                return False, "API返回了空响应"
                
        except ImportError:
            return False, "未安装openai库，请运行: pip install openai"
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                return False, "API密钥无效或已过期"
            elif "404" in error_msg or "Not Found" in error_msg:
                return False, "API服务地址无效或模型不存在"
            elif "timeout" in error_msg.lower():
                return False, "连接超时，请检查网络"
            else:
                return False, f"连接失败: {error_msg}"
    
    def handle_get_history_files(self):
        """获取历史文件列表"""
        try:
            # 获取当前设置
            settings = self.load_settings()
            save_directory = settings.get('saveDirectory', './downloads')
            file_naming = settings.get('fileNaming', '每日记录_{date}')
            
            save_path = Path(save_directory)
            
            if not save_path.exists():
                # 如果目录不存在，返回空列表
                self.send_json_response({"status": "success", "files": []})
                return
            
            # 扫描目录中的JSON文件
            json_files = []
            for file_path in save_path.glob('*.json'):
                try:
                    # 从文件名解析日期
                    file_name = file_path.stem
                    date = self.extract_date_from_filename(file_name, file_naming)
                    
                    if date:
                        # 获取文件基本信息
                        stat = file_path.stat()
                        json_files.append({
                            'date': date,
                            'filename': file_path.name,
                            'path': str(file_path),
                            'size': stat.st_size,
                            'modified': stat.st_mtime
                        })
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")
                    continue
            
            # 按日期排序
            json_files.sort(key=lambda x: x['date'], reverse=True)
            
            self.send_json_response({
                "status": "success", 
                "files": json_files,
                "saveDirectory": save_directory
            })
            
        except Exception as e:
            self.send_json_response({
                "status": "error", 
                "message": f"获取历史文件失败: {str(e)}"
            })
    
    def handle_load_record(self, date):
        """加载指定日期的记录"""
        try:
            # 获取当前设置
            settings = self.load_settings()
            save_directory = settings.get('saveDirectory', './downloads')
            file_naming = settings.get('fileNaming', '每日记录_{date}')
            
            # 构建文件路径
            file_name = file_naming.replace('{date}', date)
            file_path = Path(save_directory) / f"{file_name}.json"
            
            if not file_path.exists():
                self.send_json_response({
                    "status": "error", 
                    "message": f"文件不存在: {file_path}"
                })
                return
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                record_data = json.load(f)
            
            self.send_json_response({
                "status": "success", 
                "data": record_data,
                "filePath": str(file_path)
            })
            
        except Exception as e:
            self.send_json_response({
                "status": "error", 
                "message": f"加载记录失败: {str(e)}"
            })
    
    def extract_date_from_filename(self, filename, naming_pattern):
        """从文件名中提取日期"""
        try:
            # 移除模式中的 {date} 部分，获取前缀和后缀
            if '{date}' not in naming_pattern:
                return None
            
            prefix, suffix = naming_pattern.split('{date}', 1)
            
            # 从文件名中提取日期部分
            if prefix and not filename.startswith(prefix):
                return None
            if suffix and not filename.endswith(suffix):
                return None
            
            # 提取日期字符串
            start_pos = len(prefix)
            end_pos = len(filename) - len(suffix) if suffix else len(filename)
            date_str = filename[start_pos:end_pos]
            
            # 验证日期格式 (YYYY-MM-DD)
            if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
                # 尝试解析日期以验证有效性
                from datetime import datetime
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            
            return None
            
        except Exception:
            return None
    
    def send_json_response(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def update_settings_xml(self, settings_data):
        """更新settings.xml文件"""
        xml_file = Path('settings.xml')
        
        # 如果XML文件不存在，创建一个默认的
        if not xml_file.exists():
            self.create_default_settings_xml()
        
        # 解析现有XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # 更新基础设置值
        general = root.find('general')
        if general is not None:
            save_dir = general.find('saveDirectory')
            if save_dir is not None:
                save_dir.text = settings_data.get('saveDirectory', './downloads')
            
            auto_save = general.find('autoSave')
            if auto_save is not None:
                auto_save.text = str(settings_data.get('autoSave', True)).lower()
        
        export_section = root.find('export')
        if export_section is not None:
            file_naming = export_section.find('fileNaming')
            if file_naming is not None:
                file_naming.text = settings_data.get('fileNaming', '每日记录_{date}')
        
        # 更新或创建AI设置
        ai_section = root.find('ai')
        if ai_section is None:
            ai_section = ET.SubElement(root, 'ai')
        
        # 更新AI enabled设置
        enabled_elem = ai_section.find('enabled')
        if enabled_elem is None:
            enabled_elem = ET.SubElement(ai_section, 'enabled')
        enabled_elem.text = str(settings_data.get('aiEnabled', False)).lower()
        
        # 更新API密钥（仅在提供时保存）
        api_key = settings_data.get('openrouterApiKey', '')
        if api_key:  # 只有在提供了API密钥时才保存
            api_key_elem = ai_section.find('openrouterApiKey')
            if api_key_elem is None:
                api_key_elem = ET.SubElement(ai_section, 'openrouterApiKey')
            api_key_elem.text = api_key
        
        # 更新Base URL
        base_url_elem = ai_section.find('openrouterBaseUrl')
        if base_url_elem is None:
            base_url_elem = ET.SubElement(ai_section, 'openrouterBaseUrl')
        base_url_elem.text = settings_data.get('openrouterBaseUrl', 'https://openrouter.ai/api/v1')
        
        # 更新模型
        model_elem = ai_section.find('openrouterModel')
        if model_elem is None:
            model_elem = ET.SubElement(ai_section, 'openrouterModel')
        model_elem.text = settings_data.get('openrouterModel', 'deepseek/deepseek-r1-0528-qwen3-8b:free')
        
        # 添加更新时间
        last_updated = root.find('lastUpdated')
        if last_updated is None:
            last_updated = ET.SubElement(root, 'lastUpdated')
        last_updated.text = settings_data.get('updatedAt', '')
        
        # 保存XML文件
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    
    def create_default_settings_xml(self):
        """创建默认的settings.xml文件"""
        root = ET.Element("settings")
        
        general = ET.SubElement(root, "general")
        ET.SubElement(general, "saveDirectory").text = "./downloads"
        ET.SubElement(general, "autoSave").text = "true"
        ET.SubElement(general, "dateFormat").text = "YYYY-MM-DD"
        
        export_section = ET.SubElement(root, "export")
        ET.SubElement(export_section, "includeStatistics").text = "true"
        ET.SubElement(export_section, "includeTimestamp").text = "true"
        ET.SubElement(export_section, "fileNaming").text = "每日记录_{date}"
        
        # 添加AI设置
        ai_section = ET.SubElement(root, "ai")
        ET.SubElement(ai_section, "enabled").text = "false"
        ET.SubElement(ai_section, "openrouterApiKey").text = ""
        ET.SubElement(ai_section, "openrouterBaseUrl").text = "https://openrouter.ai/api/v1"
        ET.SubElement(ai_section, "openrouterModel").text = "deepseek/deepseek-r1-0528-qwen3-8b:free"
        
        ui = ET.SubElement(root, "ui")
        ET.SubElement(ui, "theme").text = "light"
        ET.SubElement(ui, "language").text = "zh-CN"
        
        tree = ET.ElementTree(root)
        tree.write('settings.xml', encoding='utf-8', xml_declaration=True)
    
    def load_settings(self):
        """从settings.xml文件加载设置"""
        try:
            xml_file = Path('settings.xml')
            if not xml_file.exists():
                return {}
            
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            settings = {}
            
            # 读取general设置
            general = root.find('general')
            if general is not None:
                save_dir = general.find('saveDirectory')
                if save_dir is not None:
                    settings['saveDirectory'] = save_dir.text
                
                auto_save = general.find('autoSave')
                if auto_save is not None:
                    settings['autoSave'] = auto_save.text.lower() == 'true'
            
            # 读取export设置
            export_section = root.find('export')
            if export_section is not None:
                file_naming = export_section.find('fileNaming')
                if file_naming is not None:
                    settings['fileNaming'] = file_naming.text
            
            # 读取AI设置
            ai_section = root.find('ai')
            if ai_section is not None:
                enabled = ai_section.find('enabled')
                if enabled is not None:
                    settings['aiEnabled'] = enabled.text.lower() == 'true'
                
                api_key = ai_section.find('openrouterApiKey')
                if api_key is not None and api_key.text:
                    settings['openrouterApiKey'] = api_key.text
                
                base_url = ai_section.find('openrouterBaseUrl')
                if base_url is not None and base_url.text:
                    settings['openrouterBaseUrl'] = base_url.text
                
                model = ai_section.find('openrouterModel')
                if model is not None and model.text:
                    settings['openrouterModel'] = model.text
            
            return settings
            
        except Exception as e:
            print(f"加载设置失败: {e}")
            return {}


def start_server(port=8000):
    """启动HTTP服务器"""
    
    # 确保在正确的目录中
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 检查index.html是否存在
    if not Path('index.html').exists():
        print("❌ 错误: 找不到 index.html 文件")
        print("请确保在正确的目录中运行此脚本")
        return
    
    # 使用自定义处理器
    Handler = SettingsHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"🌐 每日计划与总结Web应用已启动")
            print(f"📍 服务器地址: http://localhost:{port}")
            print(f"📂 服务目录: {script_dir}")
            print("🔄 按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 自动打开浏览器
            try:
                webbrowser.open(f'http://localhost:{port}')
                print("🚀 正在打开浏览器...")
            except Exception as e:
                print(f"⚠️ 无法自动打开浏览器: {e}")
                print(f"请手动打开浏览器并访问: http://localhost:{port}")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 端口 {port} 已被占用")
            print(f"尝试使用其他端口...")
            start_server(port + 1)
        else:
            print(f"❌ 启动服务器失败: {e}")

def main():
    """主函数"""
    port = 8000
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ 无效的端口号，使用默认端口 8000")
            port = 8000
    
    from datetime import datetime
    today = datetime.now().strftime("%Y年%m月%d日")
    print(f"🌟 {today} 计划与总结Web应用启动器")
    print("=" * 40)
    
    start_server(port)

if __name__ == "__main__":
    main()
