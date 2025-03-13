import pandas as pd
import os

# 假设查询结果保存在 'query_results.csv' 中
df = pd.read_csv('query_results.csv')

# 创建保存文件的目录
output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

# 按照 'project' 列分组并保存到单独的文件
for project_name, group_data in df.groupby('project'):
    # 处理项目名称，避免非法字符导致文件保存失败
    safe_project_name = ''.join(c for c in project_name if c.isalnum() or c in (' ', '_')).rstrip()
    # 定义输出文件路径
    output_file = os.path.join(output_dir, f'project_{safe_project_name}.csv')
    # 保存分组数据到 CSV 文件
    group_data.to_csv(output_file, index=False)
    print(f"Saved data for project '{project_name}' to '{output_file}'")