import pandas as pd
import sqlite3
import os
import shutil

def convert_excel_to_sqlite():
    # 确保data目录存在
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # 确保ABS search/data目录存在
    abs_search_data_dir = 'ABS search/data'
    if not os.path.exists(abs_search_data_dir):
        os.makedirs(abs_search_data_dir)
    
    # 读取Excel文件
    print("正在读取Excel文件...")
    df = pd.read_excel('data/合并全部后的数据.xlsx', dtype={
        'AJG_2024': str,
        'AJG_2021': str,
        'AJG_2018': str,
        'AJG_2014': str,
        'AJG_2010': str,
        '2025年中科院大类分区': str,
        '小类1分区': float,
        '小类2分区': float,
        'UTD24': str,
        'FT50': str
    })
    
    # 处理数据
    print("正在处理数据...")
    # 处理小类1分区和小类2分区
    for col in ['小类1分区', '小类2分区']:
        df[col] = df[col].apply(lambda x: str(int(x)) if pd.notnull(x) and x != 'N/A' else 'N/A')
    
    # 处理AJG评级
    ajg_columns = ['AJG_2024', 'AJG_2021', 'AJG_2018', 'AJG_2014', 'AJG_2010']
    for col in ajg_columns:
        df[col] = df[col].fillna('0')
        df[col] = df[col].replace('0', 'N/A')
    
    # 处理中科院大类分区
    df['2025年中科院大类分区'] = df['2025年中科院大类分区'].fillna('0')
    df['2025年中科院大类分区'] = df['2025年中科院大类分区'].replace('0', 'N/A')
    
    # 处理UTD24和FT50
    def convert_to_int_flag(x):
        if pd.isna(x) or str(x).strip() == '' or str(x).strip().lower() == 'nan':
            return '0'
        try:
            val = float(str(x).strip())
            return '1' if val >= 1 else '0'
        except:
            return '0'
    
    print("正在处理UTD24和FT50...")
    df['UTD24'] = df['UTD24'].apply(convert_to_int_flag)
    df['FT50'] = df['FT50'].apply(convert_to_int_flag)
    
    # 将其他所有的nan替换为N/A
    df = df.fillna('N/A')
    
    # 创建SQLite数据库 - 主位置
    print("正在创建SQLite数据库...")
    db_path = 'data/journal_data.db'
    conn = sqlite3.connect(db_path)
    
    # 将数据写入SQLite
    print("正在写入数据...")
    df.to_sql('journals', conn, if_exists='replace', index=False)
    
    # 创建索引以提高搜索性能
    print("正在创建索引...")
    cursor = conn.cursor()
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_journal ON journals(Journal)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_print_issn ON journals(Print_issn)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_e_issn ON journals(E_issn)')
    
    # 关闭连接
    conn.close()
    
    # 复制数据库文件到ABS search/data目录
    print("正在复制数据库文件到ABS search/data目录...")
    abs_search_db_path = os.path.join(abs_search_data_dir, 'journal_data.db')
    shutil.copy2(db_path, abs_search_db_path)
    
    print(f"转换完成！数据库文件已保存至:")
    print(f"  主位置: {db_path}")
    print(f"  复制位置: {abs_search_db_path}")
    
    # 显示文件大小
    db_size = os.path.getsize(db_path) / (1024 * 1024)  # 转换为MB
    print(f"数据库文件大小: {db_size:.2f} MB")
    
    # 验证复制是否成功
    if os.path.exists(abs_search_db_path):
        abs_search_db_size = os.path.getsize(abs_search_db_path) / (1024 * 1024)
        print(f"复制位置文件大小: {abs_search_db_size:.2f} MB")
        if abs(db_size - abs_search_db_size) < 0.01:  # 允许1KB的误差
            print("✓ 数据库文件复制成功！")
        else:
            print("⚠ 警告：复制文件大小不匹配")
    else:
        print("✗ 错误：复制失败")

if __name__ == "__main__":
    convert_excel_to_sqlite() 