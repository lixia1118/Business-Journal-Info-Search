import pandas as pd

# 读取主文件
main_df = pd.read_excel('ABS search/data copy/最新ABS评级.xlsx')
print(f"\n主文件数据量: {len(main_df)} 行")
print(f"其中Print_issn为空的行数: {main_df['Print_issn'].isna().sum()} 行")

# 1. 合并JCR数据
jcr_df = pd.read_csv('ABS search/journal info/JCR2024-UTF8.csv')
jcr_selected = jcr_df[['ISSN', 'Web of Science', 'IF(2024)', 'IF Quartile','Country']]
# 重命名列
jcr_selected = jcr_selected.rename(columns={
    'IF(2024)': 'JCR IF(2024)',
    'IF Quartile': 'JCR分区(2024)'
})
print(f"\nJCR数据合并前:")
print(f"JCR数据量: {len(jcr_selected)} 行")
valid_matches = main_df[main_df['Print_issn'].notna()]['Print_issn'].isin(jcr_selected['ISSN']).sum()
print(f"成功匹配数量: {valid_matches} 行")

# 确保Print_issn为空的行不会被错误匹配
main_df['Print_issn'] = main_df['Print_issn'].fillna('')  # 将NaN替换为空字符串
main_df = pd.merge(main_df, jcr_selected, 
                  left_on='Print_issn', 
                  right_on='ISSN', 
                  how='left')
main_df = main_df.drop('ISSN', axis=1)
main_df['Print_issn'] = main_df['Print_issn'].replace('', pd.NA)  # 将空字符串改回NaN

# 保存JCR合并后的结果
main_df.to_excel('ABS search/data copy/合并JCR后的数据.xlsx', index=False)
print("已保存JCR合并结果")

# 2. 合并FMS数据
fms_df = pd.read_excel('ABS search/journal info/FMS 高质量国际期刊列表.xlsx')
# 清理ISSN中的空格
fms_df['ISSN'] = fms_df['ISSN'].astype(str).str.strip()  # 移除前后空格
fms_selected = fms_df[['ISSN', 'FMS等级']]

print(f"\nFMS数据合并前:")
print(f"FMS数据量: {len(fms_selected)} 行")
valid_matches = main_df[main_df['Print_issn'].notna()]['Print_issn'].isin(fms_selected['ISSN']).sum()
print(f"成功匹配数量: {valid_matches} 行")

# 确保主文件的ISSN也是清理过的
main_df['Print_issn'] = main_df['Print_issn'].astype(str).str.strip()
main_df['Print_issn'] = main_df['Print_issn'].replace('nan', '')

# 合并数据
main_df = pd.merge(main_df, fms_selected,
                  left_on='Print_issn', 
                  right_on='ISSN', 
                  how='left')
main_df = main_df.drop('ISSN', axis=1)
main_df['Print_issn'] = main_df['Print_issn'].replace('', pd.NA)

# 保存FMS合并后的结果
main_df.to_excel('ABS search/data copy/合并JCR+FMS后的数据.xlsx', index=False)
print("已保存FMS合并结果")

# 3. 合并中科院数据
cas_df = pd.read_csv('ABS search/journal info/FQBJCR2025-UTF8.csv')
cas_selected = cas_df[['ISSN', '2025年中科院大类', '2025年中科院大类分区', '是否中科院Top期刊','小类1','小类1分区','小类2','小类2分区']]
# 重命名列
cas_selected = cas_selected.rename(columns={
    '2025年中科院大类': '2025年中科院大类学科'
})
print(f"\n中科院数据合并前:")
print(f"中科院数据量: {len(cas_selected)} 行")
valid_matches = main_df[main_df['Print_issn'].notna()]['Print_issn'].isin(cas_selected['ISSN']).sum()
print(f"成功匹配数量: {valid_matches} 行")

main_df['Print_issn'] = main_df['Print_issn'].fillna('')
main_df = pd.merge(main_df, cas_selected,
                  left_on='Print_issn', 
                  right_on='ISSN', 
                  how='left')
main_df = main_df.drop('ISSN', axis=1)
main_df['Print_issn'] = main_df['Print_issn'].replace('', pd.NA)

# 4. 合并ABDC数据
abdc_df = pd.read_excel('ABS search/journal info/ABDC-JQL-2022-v3-100523.xlsx', sheet_name='2022 JQL')
abdc_selected = abdc_df[['ISSN', 'ISSN Online', 'Year Inception', '2022 rating', '2019 rating', '2016 rating']]
# 清理ISSN中的空格
abdc_selected.loc[:, 'ISSN'] = abdc_selected['ISSN'].astype(str).str.strip()
abdc_selected.loc[:, 'ISSN Online'] = abdc_selected['ISSN Online'].astype(str).str.strip()


# 重命名列
abdc_selected = abdc_selected.rename(columns={
    '2022 rating': 'ABDC等级(2022)',
    '2019 rating': 'ABDC等级(2019)',
    '2016 rating': 'ABDC等级(2016)',
    'Year Inception': 'ABDC创刊年份'
})

print(f"\nABDC数据合并前:")
print(f"ABDC数据量: {len(abdc_selected)} 行")
valid_matches = main_df[main_df['Print_issn'].notna()]['Print_issn'].isin(abdc_selected['ISSN']).sum()
print(f"成功匹配数量: {valid_matches} 行")

# 确保Print_issn为空的行不会被错误匹配
main_df['Print_issn'] = main_df['Print_issn'].fillna('')
main_df = pd.merge(main_df, abdc_selected,
                  left_on='Print_issn',
                  right_on='ISSN',
                  how='left')
main_df = main_df.drop(['ISSN', 'ISSN Online'], axis=1)  # 删除多余的ISSN列
main_df['Print_issn'] = main_df['Print_issn'].replace('', pd.NA)

# 保存最终合并结果
main_df.to_excel('ABS search/data copy/合并全部后的数据.xlsx', index=False)
main_df.to_excel('ABS search/data/合并全部后的数据.xlsx', index=False)
main_df.copy().to_excel('data/合并全部后的数据.xlsx', index=False)
print("已保存最终合并结果")

print(f"\n最终合并后的数据量: {len(main_df)} 行")

# 检查空值情况
print("\n各列的空值统计:")
print(main_df.isnull().sum())
