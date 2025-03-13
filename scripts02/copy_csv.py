import pandas as pd

# 读取旧的 CSV 文件
old_file_path = "ui_report_01.csv"
try:
    df = pd.read_csv(old_file_path)
except pd.errors.ParserError:
    print(f"文件 {old_file_path} 格式存在问题，无法解析。")
    # 如果文件损坏，尝试修复或手动检查文件内容
    # 例如，您可以尝试使用其他工具打开并修复文件
    raise

# 对数据进行必要的处理，例如删除空行或空列
df.dropna(how='all', inplace=True)  # 删除全为空值的行
df.dropna(axis=1, how='all', inplace=True)  # 删除全为空值的列

# 保存为新的 CSV 文件
new_file_path = "new_data.csv"
df.to_csv(new_file_path, index=False, encoding='utf-8-sig')

print(f"新的 CSV 文件已保存为 {new_file_path}")
