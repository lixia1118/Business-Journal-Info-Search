本项目的原始数据来源于[ShowJCR项目](https://github.com/hitfyd/ShowJCR/tree/master)，但是仅提供**商科外文期刊**[^1]的信息查询，包括：**基本信息**、**英国ABS评级信息**、**澳洲ABDC评级信息**、**JCR分区及影响因子信息**、**中科院分区信息**、**FMS评级信息**等，只需输入期刊名或其ISSN值即可，支持模糊搜索。
[^1]: 此处指代所有ABS评级期刊

更新数据与代码的步骤如下：
1. 在*ABS search/journal info*文件夹中添加新的评级数据文件（csv格式）
2. 运行*ABS search/merge data.py*以合并所有csv数据，注意更改字段名称（比如2024可能要改为2025），与新数据的字段要保持一致
3. 修改*ABS search/src/journal_search.py*中相应部分的字段名称，与前面保持一致
4. 运行*data/convert_to_sqlite.py*，将合并后的.xlxs文件转换为更轻量的.db文件
5. 分别在*ABS search/build.py*、*ABS search/src/journal_search.py*修改版本名称
6. 运行*ABS search/build.py*即可生成可以直接运行的.exe文件（在*dist*文件夹中）
至此，更新工作结束
