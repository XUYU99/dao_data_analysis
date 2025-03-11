import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('dune_voter_hold_vote_1000.csv')

# 删除包含 NaN 的整行数据
df.dropna(inplace=True)

# 确保 X 和 y 的数据格式正确
X = df[['uni_vote_count']]
y = df['balance']

# 计算 IQR（四分位距）方法剔除异常值
Q1 = y.quantile(0.25)  # 第一四分位数（25%）
Q3 = y.quantile(0.75)  # 第三四分位数（75%）
IQR = Q3 - Q1  # 四分位距
lower_bound = Q1 - 1.5 * IQR  # 下界
upper_bound = Q3 + 1.5 * IQR  # 上界

# 过滤掉超出上下界的异常值
df_filtered = df[(y >= lower_bound) & (y <= upper_bound)]

# 重新获取 X 和 y
X_filtered = df_filtered[['uni_vote_count']]
y_filtered = df_filtered['balance']

# 绘制剔除异常值后的散点图
plt.figure(figsize=(8, 6))
plt.scatter(X_filtered, y_filtered, alpha=0.6, color='blue', label="Filtered Data Points")
plt.xlabel("Uni Vote Count")
plt.ylabel("Balance")
plt.title("Scatter Plot of Balance vs Uni Vote Count (Filtered)")
plt.legend()
plt.show()

# 显示剔除异常值后的数据规模
print(f"原始数据行数: {df.shape[0]}")
print(f"剔除异常值后的数据行数: {df_filtered.shape[0]}")
