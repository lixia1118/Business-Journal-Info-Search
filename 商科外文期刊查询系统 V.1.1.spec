# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['f:\\Cursor\\商科外文期刊查询系统\\ABS search\\run.py'],
    pathex=[],
    binaries=[],
    datas=[('f:\\Cursor\\商科外文期刊查询系统\\ABS search\\data/journal_data.db', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'numpy', 'pandas', 'numexpr', 'bottleneck', 'PIL', 'cv2', 'imageio', 'notebook', 'IPython', 'pytest', 'jedi', 'sphinx', 'docutils', 'win32com', 'PyQt5', 'PySide2', 'PyQt6', 'PySide6', 'wx', 'kivy', 'mysql', 'psycopg2', 'pymongo', 'requests', 'urllib3', 'tornado', 'zmq', 'websockets', 'cryptography', 'psutil', 'colorama', 'wcwidth', 'packaging', 'setuptools', 'distutils', 'pkg_resources', 'babel', 'lxml', 'h5py', 'yaml', 'openpyxl', 'xlrd', 'xlwt', 'xlsxwriter'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='商科外文期刊查询系统 V.1.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['f:\\Cursor\\商科外文期刊查询系统\\ABS search\\assets\\icon.ico'],
)
