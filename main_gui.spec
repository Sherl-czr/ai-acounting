# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 添加数据文件（如分类标准.md、记账内容.md等）
datas = [
    ('resources/logo.ico', 'resources'),  # 添加图标文件
    ('prompt.md', '.')
]

# 主程序配置
a = Analysis(
    ['main_gui.py'],  # 主程序入口
    pathex=['.'],  # 项目根目录
    binaries=[],
    datas=datas,  # 数据文件
    hiddenimports=[],  # 如果有隐藏的依赖，可以在这里添加
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[  # 排除不需要的库
        'pandas', 'numpy', 'scipy', 'sqlalchemy', 'tensorflow', 'keras',
        'sklearn', 'statsmodels', 'seaborn', 'bokeh', 'plotly', 'django', 'flask',
        'sqlite3', 'mysql', 'psycopg2', 'pyodbc', 'cx_Oracle', 'pymongo', 'redis',
        'pillow', 'opencv', 'pygame', 'pyglet', 'pyqtwebengine', 'qt', 'tkinter',
        'tornado', 'asyncio', 'gevent', 'twisted', 'zmq', 'paramiko', 'fabric',
        'boto3', 'botocore', 'awscli', 'azure', 'google', 'gcloud', 'openpyxl',
        'xlrd', 'xlwt', 'xlsxwriter', 'pytz', 'dateutil', 'tzdata', 'cryptography',
        'pycrypto', 'pyopenssl', 'rsa', 'paramiko', 'fabric', 'boto3', 'botocore',
        'awscli', 'azure', 'google', 'gcloud', 'openpyxl', 'xlrd', 'xlwt', 'xlsxwriter',
        'pytz', 'dateutil', 'tzdata', 'cryptography', 'pycrypto', 'pyopenssl', 'rsa'
    ],
    
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 打包配置
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 可执行文件配置
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ai记账',  # 可执行文件名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用 UPX 压缩
    console=False,  # 不显示控制台窗口
    icon='resources/logo.ico',  # 设置可执行文件图标
)

# 打包为单个文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ai记账',  # 可执行文件名称
)