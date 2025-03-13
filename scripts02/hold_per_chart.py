import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 假设数据已保存在 CSV 文件中
df = pd.read_csv('./scripts02/project_vote_data/aave_proposal_voter_votes_all.csv')

# 计算每个 proposal_id 的前 10% 投票占比
def calculate_top_10_percent_share(group):
    group = group.sort_values(by='votes', ascending=False)
    top_10_count = max(1, int(len(group) * 0.1))  # 至少保留 1 个投票者
    top_10_votes = group.head(top_10_count)['votes'].sum()
    total_votes = group['votes'].sum()
    return pd.Series({
        'total_votes': total_votes,
        'top_10_votes': top_10_votes,
        'top_10_percent_share': top_10_votes / total_votes if total_votes > 0 else 0
    })

# 按 proposal_id 分组计算占比
result = df.groupby('proposal_id').apply(calculate_top_10_percent_share).reset_index()
# 判断是否存在寡头（这里设定前10%投票占比超过 90% 为寡头）
result['is_oligopoly'] = result['top_10_percent_share'] > 0.9

# 计算所有 proposal 的平均前10%投票占比
avg_share = result['top_10_percent_share'].mean()

# 绘制图表
plt.figure(figsize=(10, 6))
plt.bar(
    result['proposal_id'].astype(str),
    result['top_10_percent_share'],
    color=['#7D8CA3' if x else '#FFA500' for x in result['is_oligopoly']]
)
# 绘制平均占比参考线（蓝色虚线），并在图例中显示平均占比数值
plt.axhline(y=avg_share, color='gray', linestyle='--', label=f'Average Share = {avg_share:.2f}')
plt.xlabel('Proposal ID')
plt.ylabel('Top 10% Voting Share')
plt.title('Top 10% Voting Share per Proposal ID')
plt.legend()
plt.xticks(fontsize=5)  # 调小横坐标字体大小
plt.tight_layout()
plt.show()
