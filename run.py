import tkinter as tk
import os
import sys

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.journal_search import JournalSearchApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("商科外文期刊查询系统")
    app = JournalSearchApp(root)
    root.mainloop() 