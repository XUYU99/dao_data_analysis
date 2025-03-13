import pandas as pd

# 读取数据
df = pd.read_csv('uniswap_proposal_voter_votes_all.csv')

# 计算每个 proposal_id 的前 10% 投票占比
def calculate_top_10_percent_share(group):
    # 按 votes 降序排序
    group = group.sort_values(by='votes', ascending=False)
    # 计算前 10% 投票者数量
    top_10_count = max(1, int(len(group) * 0.1))  # 至少保留 1 个
    # 计算前 10% 投票总和
    top_10_votes = group.head(top_10_count)['votes'].sum()
    # 计算该提案的总投票数
    total_votes = group['votes'].sum()
    # 计算占比
    return pd.Series({
        'total_votes': total_votes,
        'top_10_votes': top_10_votes,
        'top_10_percent_share': top_10_votes / total_votes if total_votes > 0 else 0
    })

# 按 proposal_id 分组并计算占比
result = df.groupby('proposal_id').apply(calculate_top_10_percent_share).reset_index()

# 判断是否存在寡头（占比超过 50% 视为寡头）
result['is_oligopoly'] = result['top_10_percent_share'] > 0.9

# 显示结果
print(result)