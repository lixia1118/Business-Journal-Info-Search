import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(current_dir, 'run.py'),  # 使用完整路径
    '--name=商科外文期刊查询系统 V.1.0',  # 生成的exe文件名
    '--windowed',  # 不显示控制台窗口
    '--onefile',  # 打包成单个文件
    '--clean',  # 清理临时文件
    f'--add-data={os.path.join(current_dir, "data/journal_data.db")};data',  # 添加SQLite数据库文件
    f'--icon={os.path.join(current_dir, "assets/icon.ico")}',  # 使用完整路径
    '--noconfirm',  # 不询问确认
    # 科学计算和数据分析相关
    '--exclude-module=matplotlib',
    '--exclude-module=scipy',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=numexpr',
    '--exclude-module=bottleneck',
    # 图像处理相关
    '--exclude-module=PIL',
    '--exclude-module=cv2',
    '--exclude-module=imageio',
    # IDE和开发工具相关
    '--exclude-module=notebook',
    '--exclude-module=IPython',
    '--exclude-module=pytest',
    '--exclude-module=jedi',
    '--exclude-module=sphinx',
    '--exclude-module=docutils',
    # GUI相关
    '--exclude-module=win32com',
    '--exclude-module=PyQt5',
    '--exclude-module=PySide2',
    '--exclude-module=PyQt6',
    '--exclude-module=PySide6',
    '--exclude-module=wx',
    '--exclude-module=kivy',
    # 数据库相关（除了sqlite3）
    '--exclude-module=mysql',
    '--exclude-module=psycopg2',
    '--exclude-module=pymongo',
    # 网络和Web相关
    '--exclude-module=requests',
    '--exclude-module=urllib3',
    '--exclude-module=tornado',
    '--exclude-module=zmq',
    '--exclude-module=websockets',
    # 其他工具和库
    '--exclude-module=cryptography',
    '--exclude-module=psutil',
    '--exclude-module=colorama',
    '--exclude-module=wcwidth',
    '--exclude-module=packaging',
    '--exclude-module=setuptools',
    '--exclude-module=distutils',
    '--exclude-module=pkg_resources',
    '--exclude-module=babel',
    '--exclude-module=lxml',
    '--exclude-module=h5py',
    '--exclude-module=yaml',
    '--exclude-module=openpyxl',
    '--exclude-module=xlrd',
    '--exclude-module=xlwt',
    '--exclude-module=xlsxwriter',
]) 

print(os.getcwd()) 