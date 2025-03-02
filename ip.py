# Copyright 2025 Omega Labs, ArkLauncher Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import queue
import socket
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, scrolledtext
from tkinter.simpledialog import Dialog

import requests


class IPOptimizer:
    def __init__(self, master):
        self.master = master
        self.master.title("IP优选工具 v1.3")
        self.master.geometry("800x600")

        self.config = {
            'timeout': 2,
            'test_count': 4,
            'cloud_sources': {
                'source_a': 'https://source1.playat.cn/address.txt',
                'source_b': 'https://proxy.bzym.fun/https://source1.playat.cn/address.txt'
            }
        }
        self.create_widgets()
        self.test_queue = queue.Queue()
        self.running = False
        self.results = []

    def create_widgets(self):
        btn_frame = ttk.Frame(self.master)
        btn_frame.pack(pady=20)

        self.main_btn = ttk.Button(btn_frame, text="开始IP优选", style='Big.TButton',
                                   command=self.start_optimization)
        self.main_btn.pack(padx=20, pady=10)

        self.progress = ttk.Progressbar(self.master, orient='horizontal',
                                        mode='determinate', length=400)
        self.progress.pack(pady=5)
        self.log_area = scrolledtext.ScrolledText(self.master,
                                                  height=10,
                                                  state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.status = ttk.Label(self.master, text="就绪", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def start_optimization(self):
        SourceSelector(self.master, self)

    def log(self, message):
        self.log_area.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)
        self.status.config(text=message)

    def start_test(self, source):
        self.log(f"正在从云端获取 {source} 的IP列表...")
        try:
            ip_list = self.fetch_ips_from_cloud(source)
            if not ip_list:
                raise ValueError("获取到的IP列表为空")
        except Exception as e:
            self.log(f"错误: {str(e)}")
            return

        self.log(f"开始测试 {len(ip_list)} 个IP地址")
        self.results = []
        self.running = True
        self.progress.config(maximum=len(ip_list))
        self.progress['value'] = 0

        max_threads = 50
        ip_chunks = [ip_list[i:i + max_threads] for i in range(0, len(ip_list), max_threads)]

        for chunk in ip_chunks:
            threads = []
            for ip in chunk:
                thread = threading.Thread(target=self.test_ip, args=(ip,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        self.show_results()

    def fetch_ips_from_cloud(self, source):
        url = self.config['cloud_sources'].get(source)
        if not url:
            raise ValueError("无效的源服务器")

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data.get('ips', [])
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"连接云端失败: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("无效的响应格式")

    def test_ip(self, ip_port):
        try:
            host, port_str = ip_port.split(':')
            port = int(port_str)
        except (ValueError, IndexError):
            self.test_queue.put(('log', f"无效的IP格式: {ip_port}"))
            return

        timeout = self.config['timeout']
        test_count = self.config['test_count']

        successes = 0
        total_latency = 0

        for _ in range(test_count):
            try:
                start_time = time.time()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(timeout)
                    s.connect((host, port))
                    latency = (time.time() - start_time) * 1000
                    successes += 1
                    total_latency += latency
            except (socket.timeout, ConnectionRefusedError, OSError) as e:
                continue
        loss_rate = ((test_count - successes) / test_count) * 100
        avg_latency = total_latency / successes if successes > 0 else 9999

        self.results.append({
            'ip': f"{host}:{port}",
            'latency': round(avg_latency, 1),
            'loss': round(loss_rate, 1)
        })

        self.test_queue.put(('update', f"{host}:{port}"))
        self.test_queue.put(('log', f"{host} 测试完成: {avg_latency:.1f}ms 丢包 {loss_rate:.1f}%"))

    def update_progress(self):
        while not self.test_queue.empty():
            action, *args = self.test_queue.get()
            if action == 'update':
                self.progress['value'] += 1
            elif action == 'log':
                self.log(args[0])

        if self.progress['value'] < self.progress['maximum']:
            self.master.after(100, self.update_progress)

    def show_results(self):
        valid_results = [r for r in self.results if r['latency'] < 9999]
        if not valid_results:
            messagebox.showwarning("无结果", "没有找到有效的IP地址")
            return

        results_window = tk.Toplevel(self.master)
        ResultsWindow(results_window, valid_results, self)


class SourceSelector(Dialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, "选择测试源")

    def body(self, frame):
        ttk.Label(frame, text="请选择测试源:").grid(row=0, columnspan=2, pady=5)

        self.source_var = tk.StringVar()

        sources = [
            ('源服务器 A', 'source_a'),
            ('源服务器 B', 'source_b')
        ]

        for i, (text, value) in enumerate(sources):
            rb = ttk.Radiobutton(frame, text=text, value=value,
                                 variable=self.source_var)
            rb.grid(row=i + 1, column=0, sticky=tk.W)

            latency_label = ttk.Label(frame, text="正在测量...")
            latency_label.grid(row=i + 1, column=1, padx=10)
            threading.Thread(target=self.test_latency,
                             args=(value, latency_label)).start()

        return frame

    def test_latency(self, source, label):
        url = self.controller.config['cloud_sources'][source]
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            latency = (time.time() - start_time) * 1000
            label.config(text=f"{latency:.1f}ms")
        except:
            label.config(text="超时", foreground="red")

    def apply(self):
        selected = self.source_var.get()
        if selected:
            self.controller.start_test(selected)


class ResultsWindow:
    def __init__(self, master, results, controller):
        self.master = master
        self.controller = controller
        self.results = sorted(results, key=lambda x: x['latency'])

        master.title("优选结果")
        master.geometry("1000x600")
        self.tree = ttk.Treeview(master, columns=('ip', 'latency', 'loss'),
                                 show='headings', selectmode='browse')
        self.tree.heading('ip', text='IP地址', command=lambda: self.sort('ip'))
        self.tree.heading('latency', text='延迟(ms)', command=lambda: self.sort('latency'))
        self.tree.heading('loss', text='丢包率(%)', command=lambda: self.sort('loss'))

        self.tree.column('ip', width=300)
        self.tree.column('latency', width=150)
        self.tree.column('loss', width=150)

        for result in sorted(results, key=lambda x: x['latency']):
            self.tree.insert('', tk.END, values=(
                result['ip'],
                f"{result['latency']}ms",
                f"{result['loss']}%"
            ))

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(master)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        best_ip = self.get_best_ip()
        copy_btn = ttk.Button(control_frame, text=f"复制最优IP\n{best_ip}",
                              style='Big.TButton', command=lambda: self.copy_ip(best_ip))
        copy_btn.pack(pady=20)

        ttk.Button(control_frame, text="关闭窗口",
                   command=master.destroy).pack(pady=10)

    def get_best_ip(self):
        return min(self.results, key=lambda x: x['latency'])['ip']

    def copy_ip(self, ip):
        self.controller.master.clipboard_clear()
        self.controller.master.clipboard_append(ip)
        self.controller.status.config(text=f"已复制IP: {ip}")

    def sort(self, column):
        reverse = False
        if self.tree.heading(column)['text'].startswith('↑'):
            reverse = True
        self.results.sort(key=lambda x: x[column], reverse=reverse)

        for col in ['ip', 'latency', 'loss']:
            self.tree.heading(col, text=col.capitalize())
        self.tree.heading(column, text=f"{column.capitalize()} {'↓' if reverse else '↑'}")
        self.tree.delete(*self.tree.get_children())
        for result in self.results:
            self.tree.insert('', tk.END, values=(
                result['ip'],
                result['latency'],
                result['loss']
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = IPOptimizer(root)
    root.mainloop()
