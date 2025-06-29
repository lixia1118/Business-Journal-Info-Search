本项目的原始数据来源于[ShowJCR项目](https://github.com/hitfyd/ShowJCR/tree/master)，但是仅提供**商科外文期刊**[^1]的信息查询，包括：**基本信息**、**英国ABS评级信息**、**澳洲ABDC评级信息**、**JCR分区及影响因子信息**、**中科院分区信息**、**FMS评级信息**等，只需输入期刊名或其ISSN值即可，支持模糊搜索。
[^1]: 此处指代所有ABS评级期刊

更新代码的步骤如下：
1. 在*ABS search/journal info*文件夹中添加新的评级数据文件
2. 运行*merge data.py*以合并所有数据，注意更改字段名称（比如2024可能要改为2025），与新数据的字段要保持一致
3. 运行*data/convert_to_sqlite.py*，将合并后的xlxs文件转换为更轻量的db文件
4. 修改*ABS search/src/journal_search.py*中相应部分的字段名称，与前面保持一致
5. 运行*ABS search/build.py*构建可以直接运行的exe文件（在*dist*文件夹中）
