import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取查询结果数据
df = pd.read_csv("uniswap_holdweight_votecount.csv")

# 显示前几行数据
print(df.head())

# 计算持币时长（天）与投票次数的相关系数
correlation = df['total_hold_weight'].corr(df['vote_count'])
print("持币时长与投票活跃度的相关系数：", correlation)

# 绘制散点图并添加回归拟合线
plt.figure(figsize=(10, 6))
sns.lmplot(x='total_hold_weight', y='vote_count', data=df, height=6, aspect=1.5)
plt.xlabel("hold-time (天)")
plt.ylabel("vote count")
plt.title("relativity")
plt.show()
