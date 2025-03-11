import pandas as pd

# 读取CSV文件
file_path = "dune_voter_hold_vote_all.csv"
data = pd.read_csv(file_path)

# 确保列名正确，并按 dao_balance（治理代币持有量）排序
data_sorted = data.sort_values(by="dao_balance", ascending=False)

# 计算总的UNI代币数量
total_balance = data_sorted['dao_balance'].sum()
print(f"总的UNI代币数量: {total_balance:.2f}%")
# 计算前10%地址的数量
top_10_percent_count = int(len(data_sorted) * 0.1)
print(f"前10%地址的数量: {top_10_percent_count:.2f}%")

# 获取前10%地址的总持仓
top_10_balance = data_sorted.iloc[:top_10_percent_count]['dao_balance'].sum()
print(f"前10%地址的总持仓: {top_10_balance:.2f}%")
# 计算前10%地址的投票权重占比
top_10_percent_share = (top_10_balance / total_balance) * 100

# 打印结果
print(f"前10%地址的投票权重占比: {top_10_percent_share:.2f}%")





# WITH voter_address_table AS (
#     SELECT dv.voter_address,
#            COUNT(*) AS vote_count
#     FROM dao.votes AS dv
#     where token_address = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
#     GROUP BY dv.voter_address
#     ORDER BY dv.voter_address
# ),
# voter_hold_table AS (
#     SELECT address,MAX_BY(balance, block_time) AS dao_latest_balance
#     FROM tokens_ethereum.balances AS teb
#     where token_address = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
#     GROUP BY address
# )
# SELECT vat.voter_address as voter_address,
#     vht.dao_latest_balance as dao_balance
# from voter_address_table as vat
# left join voter_hold_table as vht
# on vat.voter_address = vht.address
# order by dao_balance desc
32000