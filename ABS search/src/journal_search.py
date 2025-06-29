import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys
import sqlite3

def resource_path(relative_path):
    """ 获取资源的绝对路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class JournalSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("商科外文期刊查询系统 V.1.2")
        
        # 设置窗口最小尺寸
        self.root.minsize(500, 800)  # 设置最小宽度为800，最小高度为600
        
        # 主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建内容框架
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(content_frame, 
                               text="商科外文期刊查询系统 V.1.2", 
                               font=("Microsoft YaHei", 20, "bold"))
        title_label.pack(pady=(0,5))
        
        # 搜索框和选项
        search_frame = ttk.Frame(content_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="期刊名/ISSN:", font=('Microsoft YaHei', 10)).pack(side=tk.LEFT)
        
        # 创建搜索输入框
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, 
                                     textvariable=self.search_var, 
                                     width=20,
                                     style='Larger.TEntry')
        self.search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # 绑定回车键搜索
        self.search_entry.bind('<Return>', lambda event: self.search())
        
        # 添加清空按钮
        clear_button = ttk.Button(search_frame, 
                                  text="清空", 
                                  command=self.clear_search,
                                  style='Custom.TButton',
                                  width=6)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 添加精确搜索选项
        self.exact_match_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(search_frame, text="精确匹配", 
                         variable=self.exact_match_var,
                         style='Custom.TCheckbutton').pack(side=tk.LEFT, padx=5)
        
        # 搜索按钮
        search_button = ttk.Button(search_frame, text="搜索", 
                                   command=self.search,
                                   style='Custom.TButton')
        search_button.pack(side=tk.LEFT, padx=5)
        
        # 创建底部按钮框架
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(fill=tk.X, pady=5, side=tk.BOTTOM)
        
        # 左侧按钮框架
        left_button_frame = ttk.Frame(bottom_frame)
        left_button_frame.pack(side=tk.LEFT)
        
        # UTD 24期刊按钮
        utd_button = ttk.Button(left_button_frame, 
                               text="UTD 24期刊", 
                               command=self.show_utd_journals,
                               style='Custom.TButton')
        utd_button.pack(side=tk.LEFT, padx=5)
        
        # FT 50期刊按钮
        ft_button = ttk.Button(left_button_frame, 
                               text="FT 50期刊", 
                               command=self.show_ft_journals,
                               style='Custom.TButton')
        ft_button.pack(side=tk.LEFT, padx=5)
        
        # 右侧按钮框架
        right_button_frame = ttk.Frame(bottom_frame)
        right_button_frame.pack(side=tk.RIGHT)
        
        # 基本说明按钮
        help_button = ttk.Button(right_button_frame, 
                                 text="基本说明", 
                                 command=self.show_instructions,
                                 style='Custom.TButton')
        help_button.pack(side=tk.RIGHT, padx=5)
        
        # 联系作者按钮
        contact_button = ttk.Button(right_button_frame, 
                                   text="联系作者", 
                                   command=self.contact_author,
                                   style='Custom.TButton')
        contact_button.pack(side=tk.RIGHT, padx=5)
        
        # 创建自定义样式
        style = ttk.Style()
        style.configure('Custom.TCheckbutton', font=('Microsoft YaHei', 10))
        style.configure('Custom.TButton', font=('Microsoft YaHei', 10), padding=5)
        style.configure('Larger.TEntry', padding=(5, 8))
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(content_frame, text="查询结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Text框架
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        y_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Text组件
        self.result_text = tk.Text(text_frame,
                                  wrap=tk.WORD,
                                  font=('Microsoft YaHei', 10),
                                  yscrollcommand=y_scrollbar.set,
                                  xscrollcommand=x_scrollbar.set,
                                  padx=10,
                                  pady=5)
        
        # 设置只读模式
        self.result_text.bind("<Key>", lambda e: "break" if e.keysym not in ("c", "C", "Control_L", "Control_R") else "")
        
        # 配置滚动条
        y_scrollbar.config(command=self.result_text.yview)
        x_scrollbar.config(command=self.result_text.xview)
        
        # 配置标签样式
        self.result_text.tag_configure("title", font=('Microsoft YaHei', 14, 'bold'), foreground='#1a237e')
        self.result_text.tag_configure("subtitle", font=('Microsoft YaHei', 11, 'bold'), foreground='#303f9f')
        self.result_text.tag_configure("content", font=('Microsoft YaHei', 10))
        self.result_text.tag_configure("highlight_yes", foreground='#d32f2f', font=('Microsoft YaHei', 10, 'bold'))
        self.result_text.tag_configure("highlight_label", foreground='#1976d2', font=('Microsoft YaHei', 10, 'bold'))
        self.result_text.tag_configure("top_journal", foreground='#d32f2f', font=('Microsoft YaHei', 10, 'bold'))
        self.result_text.tag_configure("section", font=('Microsoft YaHei', 11, 'bold'), foreground='#283593')
        self.result_text.tag_configure("divider", foreground='#9e9e9e')
        
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 连接数据库
        try:
            db_path = resource_path(os.path.join("data", "journal_data.db"))
            if not os.path.exists(db_path):
                messagebox.showerror("错误", f"找不到数据库文件: {db_path}\n请确保文件存在于所在目录下")
                return
            
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            
        except Exception as e:
            messagebox.showerror("错误", f"加载数据时出错:\n{str(e)}\n\n请确保Excel文件格式正确且未被其他程序用")
            return

    def search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("警告", "请输入期刊名称或ISSN")
            return
        
        # 清除现有结果
        self.result_text.delete('1.0', tk.END)
        
        try:
            # 根据搜索选项构建SQL查询
            if self.exact_match_var.get():
                # 精确匹配 - 使用 COLLATE NOCASE 实现不区分大小写的精确匹配
                sql = """
                SELECT * FROM journals 
                WHERE Journal COLLATE NOCASE = ? 
                OR Print_issn COLLATE NOCASE = ? 
                OR E_issn COLLATE NOCASE = ?
                """
                params = (query, query, query)
            else:
                # 模糊匹配
                query = f"%{query}%"
                sql = """
                SELECT * FROM journals 
                WHERE Journal LIKE ? COLLATE NOCASE 
                OR Print_issn LIKE ? COLLATE NOCASE 
                OR E_issn LIKE ? COLLATE NOCASE
                """
                params = (query, query, query)
            
            # 执行查询
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            
            if results:
                # 获取列名
                columns = [description[0] for description in self.cursor.description]
                
                # 显示结果
                for row in results:
                    journal = dict(zip(columns, row))
                    
                    # 期刊标题
                    self.result_text.insert(tk.END, "\n")
                    self.result_text.insert(tk.END, "  " + journal['Journal'] + "\n", "title")
                    self.result_text.insert(tk.END, "\n")
                    
                    # 基本信息块
                    self.result_text.insert(tk.END, "  基本信息\n", "section")
                    self.result_text.insert(tk.END, "  _______________\n\n", "divider")
                    
                    # 计算最长的标签宽度（包括冒号）
                    label_width = 12
                    
                    # 按新顺序显示信息
                    self.result_text.insert(tk.END, "      Web of Science: " + " " * (label_width - 13) + f"{journal['Web of Science']}\n", "content")
                    self.result_text.insert(tk.END, "      出版商:        " + " " * (label_width - 8) + f"{journal['Publisher']}\n", "content")
                    
                    # 修改创刊年份的显示逻辑，添加错误处理
                    founding_year = journal.get('ABDC创刊年份', 'N/A')
                    if founding_year is None or founding_year == '':
                        founding_year = 'N/A'
                    self.result_text.insert(tk.END, "      创刊年份:      " + " " * (label_width - 10) + f"{founding_year}\n", "content")
                    
                    self.result_text.insert(tk.END, "      国家/地区:     " + " " * (label_width - 10) + f"{journal['Country']}\n", "content")
                    self.result_text.insert(tk.END, "      纸质ISSN:      " + " " * (label_width - 10) + f"{journal['Print_issn']}\n", "content")
                    self.result_text.insert(tk.END, "      电子ISSN:      " + " " * (label_width - 10) + f"{journal['E_issn']}\n", "content")
                    
                    self.result_text.insert(tk.END, "\n")
                    
                    # UTD和FT信息也使用两列
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "UTD 24: ", "highlight_label")
                    utd_value = str(journal['UTD24']).strip()
                    is_utd = utd_value == '1' or utd_value.lower() == 'true'
                    self.result_text.insert(tk.END, f"{'是' if is_utd else '否':<30}", 
                                           "highlight_yes" if is_utd else "content")
                    
                    self.result_text.insert(tk.END, "FT 50: ", "highlight_label")
                    ft_value = str(journal['FT50']).strip()
                    is_ft = ft_value == '1' or ft_value.lower() == 'true'
                    self.result_text.insert(tk.END, f"{'是' if is_ft else '否'}\n",
                                           "highlight_yes" if is_ft else "content")
                    
                    self.result_text.insert(tk.END, "\n")
                    
                    # ABS/AJG评级信息块
                    self.result_text.insert(tk.END, "  英国ABS/AJG评级\n", "section")
                    self.result_text.insert(tk.END, "  _______________\n\n", "divider")
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "2024年: ", "content")
                    self.result_text.insert(tk.END, f"{journal['AJG_2024']:<20}", "content")
                    self.result_text.insert(tk.END, "2021年: ", "content")
                    self.result_text.insert(tk.END, f"{journal['AJG_2021']:<20}", "content")
                    self.result_text.insert(tk.END, "2018年: ", "content")
                    self.result_text.insert(tk.END, f"{journal['AJG_2018']}\n\n", "content")
                    

                    
                    # JCR评级信息块
                    self.result_text.insert(tk.END, "  2024年JCR评级\n", "section")
                    self.result_text.insert(tk.END, "  _______________\n\n", "divider")
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "影响因子: ", "content")
                    self.result_text.insert(tk.END, f"{journal['JCR IF(2024)']:<20}", "content")
                    self.result_text.insert(tk.END, "JCR分区: ", "content")
                    self.result_text.insert(tk.END, f"{journal['JCR分区(2024)']}\n\n", "content")
                    
                    # 中科院评级信息块
                    self.result_text.insert(tk.END, "  2025年中科院评级\n", "section")
                    self.result_text.insert(tk.END, "  _______________\n\n", "divider")
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "大类学科: ", "content")
                    self.result_text.insert(tk.END, f"{journal['2025年中科院大类学科']:<20}", "content")
                    self.result_text.insert(tk.END, "大类分区: ", "content")
                    self.result_text.insert(tk.END, f"{journal['2025年中科院大类分区']:<20}", "content")
                    self.result_text.insert(tk.END, "是否中科院Top期刊: ", "highlight_label")
                    is_top = journal['是否中科院Top期刊']
                    if is_top and is_top.strip().lower() in ['是', 'yes', 'true', '1']:
                        self.result_text.insert(tk.END, "是\n", "highlight_yes")
                    else:
                        self.result_text.insert(tk.END, "否\n", "content")
                    
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "小类1: ", "content")
                    self.result_text.insert(tk.END, f"{journal['小类1']:<20}", "content")
                    self.result_text.insert(tk.END, "小类1分区: ", "content")
                    self.result_text.insert(tk.END, f"{journal['小类1分区']:<20}", "content")
                    self.result_text.insert(tk.END, "\n      ")
                    self.result_text.insert(tk.END, "小类2: ", "content")
                    self.result_text.insert(tk.END, f"{journal['小类2']:<20}", "content")
                    self.result_text.insert(tk.END, "小类2分区: ", "content")
                    self.result_text.insert(tk.END, f"{journal['小类2分区']}\n\n", "content")

                    # ABDC评级信息块
                    self.result_text.insert(tk.END, "  澳洲ABDC评级\n", "section")
                    self.result_text.insert(tk.END, "  _______________\n\n", "divider")
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "2022年: ", "content")
                    self.result_text.insert(tk.END, f"{journal['ABDC等级(2022)']:<20}", "content")
                    self.result_text.insert(tk.END, "2019年: ", "content")
                    self.result_text.insert(tk.END, f"{journal['ABDC等级(2019)']:<20}", "content")
                    self.result_text.insert(tk.END, "2016年: ", "content")
                    self.result_text.insert(tk.END, f"{journal['ABDC等级(2016)']}\n\n", "content")

                    # 其他评级信息块
                    self.result_text.insert(tk.END, "  其他评级\n", "section")
                    self.result_text.insert(tk.END, "  _______________\n\n", "divider")
                    self.result_text.insert(tk.END, "      ")
                    self.result_text.insert(tk.END, "FMS高质量国际期刊等级: ", "content")
                    self.result_text.insert(tk.END, f"{journal['FMS等级']}\n\n", "content")
                    
                    self.result_text.insert(tk.END, "\n")
            else:
                self.result_text.insert(tk.END, '未找到匹配的期刊，请取消勾选"精确匹配"后重试。')
                
        except Exception as e:
            messagebox.showerror("错误", f"搜索时出错:\n{str(e)}")

    def clear_search(self):
        """清空搜索框结果"""
        self.search_var.set("")
        self.search_entry.focus_set()
        self.result_text.delete('1.0', tk.END)

    def show_instructions(self, event=None):
        """显示基本说明对话框"""
        instruction_window = tk.Toplevel(self.root)
        instruction_window.title("基本说明")
        instruction_window.geometry("500x300")
        
        # 设置模态
        instruction_window.transient(self.root)
        instruction_window.grab_set()
        
        # 创建框架来容纳文本框和滚动条
        text_frame = ttk.Frame(instruction_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建文本框
        text = tk.Text(text_frame, 
                       wrap=tk.WORD,
                       font=('Microsoft YaHei', 10),
                       padx=10,
                       pady=10,
                       yscrollcommand=scrollbar.set)
        text.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        scrollbar.config(command=text.yview)
        
        # 添加说明文本
        instructions = """商科外文期刊查询系统使用说明：

1. 支持精确匹配(默认)和模糊匹配，可输入期刊名或者ISSN

2. 查询信息包括：
   • 期刊基本信息
   • 英国ABS/AJG评级
   • 澳洲ABDC评级
   • JCR评级信息
   • 中科院评级信息
   • 其他评级信息（如FMS高质量国际期刊等级）

3. "N/A"表示该项数据暂无

4. 搜索结果支持复制

如有问题或有学习交流需求，请联系作者。
"""
        text.insert('1.0', instructions)
        text.config(state='disabled')  # 设置为只读
        
        # 添加确定按钮
        ok_button = ttk.Button(instruction_window, 
                              text="确定", 
                              command=instruction_window.destroy)
        ok_button.pack(pady=10)
        
        # 居中显示窗口
        instruction_window.update_idletasks()
        width = instruction_window.winfo_width()
        height = instruction_window.winfo_height()
        x = (instruction_window.winfo_screenwidth() // 2) - (width // 2)
        y = (instruction_window.winfo_screenheight() // 2) - (height // 2)
        instruction_window.geometry(f'{width}x{height}+{x}+{y}')

    def contact_author(self, event=None):
        """打开默认邮件客户端"""
        import webbrowser
        webbrowser.open('mailto:xiali1118@foxmail.com')

    def show_utd_journals(self, event=None):
        """显示所有UTD 24期刊"""
        self.result_text.delete('1.0', tk.END)
        
        # UTD 24期刊列表
        utd_journals = [
            "Academy of Management Journal",
            "Academy of Management Review",
            "Accounting Review",
            "Administrative Science Quarterly",
            "INFORMS Journal on Computing",
            "Information Systems Research",
            "Journal of Accounting Research",
            "Journal of Accounting and Economics",
            "Journal of Consumer Research",
            "Journal of Finance",
            "Journal of Financial Economics",
            "Journal of International Business Studies",
            "Journal of Marketing",
            "Journal of Marketing Research",
            "Journal of Operations Management",
            "MIS Quarterly: Management Information Systems",
            "Management Science",
            "Manufacturing and Service Operations Management",
            "Marketing Science",
            "Operations Research",
            "Organization Science",
            "Production and Operations Management",
            "Review of Financial Studies",
            "Strategic Management Journal"
        ]
        
        self.result_text.insert(tk.END, f"UTD 24期刊列表（共{len(utd_journals)}本）：\n\n", "title")
        
        for journal_name in utd_journals:
            # 插入期刊名称
            self.result_text.insert(tk.END, "• ")
            start_index = self.result_text.index("end-1c linestart")
            self.result_text.insert(tk.END, f"{journal_name}\n")
            end_index = self.result_text.index("end-1c")
            
            # 为整行添加标签
            tag_name = f"link_{journal_name}"
            self.result_text.tag_add(tag_name, start_index, end_index)
            self.result_text.tag_configure(tag_name, 
                                         foreground='#0066cc',
                                         font=('Microsoft YaHei', 10, 'underline'))
            
            # 直接绑定事件处理函数
            self.result_text.tag_bind(tag_name, '<Button-1>', 
                                    lambda e, j=journal_name: self.search_journal(j))
            self.result_text.tag_bind(tag_name, '<Enter>', 
                                    lambda e: self.result_text.config(cursor='hand2'))
            self.result_text.tag_bind(tag_name, '<Leave>', 
                                    lambda e: self.result_text.config(cursor=''))

    def show_ft_journals(self, event=None):
        """显示所有FT 50期刊"""
        self.result_text.delete('1.0', tk.END)
        
        # FT 50期刊列表
        ft_journals = [
            "Academy of Management Journal",
            "Academy of Management Review",
            "Accounting Review",
            "Accounting, Organizations and Society",
            "Administrative Science Quarterly",
            "American Economic Review",
            "Contemporary Accounting Research",
            "Econometrica",
            "Entrepreneurship Theory and Practice",
            "Harvard Business Review",
            "Human Relations",
            "Human Resource Management Journal (UK)",
            "Information Systems Research",
            "Journal of Accounting Research",
            "Journal of Accounting and Economics",
            "Journal of Applied Psychology",
            "Journal of Business Ethics",
            "Journal of Business Venturing",
            "Journal of Consumer Psychology",
            "Journal of Consumer Research",
            "Journal of Finance",
            "Journal of Financial Economics",
            "Journal of Financial and Quantitative Analysis",
            "Journal of International Business Studies",
            "Journal of Management",
            "Journal of Management Information Systems",
            "Journal of Management Studies",
            "Journal of Marketing",
            "Journal of Marketing Research",
            "Journal of Operations Management",
            "Journal of Political Economy",
            "Journal of the Academy of Marketing Science",
            "MIS Quarterly: Management Information Systems",
            "MIT Sloan Management Review",
            "Management Science",
            "Manufacturing and Service Operations Management",
            "Marketing Science",
            "Operations Research",
            "Organization Science",
            "Organization Studies",
            "Organizational Behavior and Human Decision Processes",
            "Production and Operations Management",
            "Quarterly Journal of Economics",
            "Research Policy",
            "Review of Accounting Studies",
            "Review of Economic Studies",
            "Review of Finance",
            "Review of Financial Studies",
            "Strategic Entrepreneurship Journal",
            "Strategic Management Journal"
        ]
        
        self.result_text.insert(tk.END, f"FT 50期刊列表（共{len(ft_journals)}本）：\n\n", "title")
        
        for journal_name in ft_journals:
            # 插入期刊名称
            self.result_text.insert(tk.END, "• ")
            start_index = self.result_text.index("end-1c linestart")
            self.result_text.insert(tk.END, f"{journal_name}\n")
            end_index = self.result_text.index("end-1c")
            
            # 为整行添加标签
            tag_name = f"link_ft_{journal_name}"
            self.result_text.tag_add(tag_name, start_index, end_index)
            self.result_text.tag_configure(tag_name, 
                                         foreground='#0066cc',
                                         font=('Microsoft YaHei', 10, 'underline'))
            
            # 直接绑定事件处理函数
            self.result_text.tag_bind(tag_name, '<Button-1>', 
                                    lambda e, j=journal_name: self.search_journal(j))
            self.result_text.tag_bind(tag_name, '<Enter>', 
                                    lambda e: self.result_text.config(cursor='hand2'))
            self.result_text.tag_bind(tag_name, '<Leave>', 
                                    lambda e: self.result_text.config(cursor=''))

    def search_journal(self, journal_name):
        """根据期刊名称执行搜索"""
        self.search_var.set(journal_name)
        self.exact_match_var.set(True)  # 设置为精确匹配
        self.search()

if __name__ == "__main__":
    root = tk.Tk()
    app = JournalSearchApp(root)
    root.mainloop() 